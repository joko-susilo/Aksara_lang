#!/usr/bin/env python3
"""
Ekspansi KORPUS Aksara — jemur teks Indonesia legal dari sumber publik.

Sumber:
  [1] Wikipedia bahasa Indonesia (CC BY-SA) via API — artikel acak, teks
      polos (prop=extracts&explaintext), politeness delay 1s, dedup judul.
      Link: https://id.wikipedia.org

Target: membantu Mini-LM v4 — model butuh data dulu sebelum parameter naik
(journal: 137KB-> target MB, 10MB ke atas wajar).

Cara pakai:
  python3 ekspansi_korpus.py --tujuan korpus_baru.txt --target 5000000 --arti 500
  python3 ekspansi_korpus.py --uji-arti 5     # tes cepat tanpa nulis file

Hanya stdlib (urllib/json/re/time) — jalan di Termux HP & PC.
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse

API = "https://id.wikipedia.org/w/api.php"

UA = "aksara-korpus/0.2 (riset mini-lm; source CC BY-SA on Wikipedia)"


def _req(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)


def ambil_artikel(n=20):
    """Ambil n artikel acak Wikipedia id -> [(judul, teks), ...]."""
    d = _req({
        "action": "query", "generator": "random", "grnnamespace": 0,
        "grnlimit": min(n, 20), "grnfilterredir": "nonredirects",
        "prop": "extracts",
        "explaintext": 1, "exlimit": "max", "format": "json",
        "utf8": 1,
    })
    out = []
    # artikel ekstensi kedua dari API: better coverage
    d2 = _req({
        "action": "query", "generator": "random", "grnnamespace": 0,
        "grnlimit": min(n, 20), "grnfilterredir": "nonredirects",
        "prop": "extracts",
        "explaintext": 1, "exlimit": "max", "format": "json",
        "utf8": 1,
    })
    pages = (d.get("query", {}).get("pages", {}) or {})
    if d2.get("query"):
        pages.update(d2["query"].get("pages", {}))
    for pg in pages.values():
        t = pg.get("extract", "")
        if t and len(t) > 200:
            out.append((pg.get("title", ""), t))
    return out


CITASI = re.compile(r"\[\d+\]|\[[a-z]+\]|<!--.*?-->", re.S)
MARKUP = re.compile(r"[{\}\[\]]")
SEP = re.compile(r"[ \t]+")
BOILER = ("disunting oleh", "rujukan", "referensi", "kategori:", "tautan luar",
          "pranala luar", "sunting sumber", "bagian ini kosong")


def bersihkan(teks, judul):
    """Bersihkan ekstrak wiki -> paragraf kalimat wajar."""
    t = CITASI.sub(" ", teks)
    t = MARKUP.sub(" ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    par = []
    for p in t.split("\n"):
        p = SEP.sub(" ", p).strip()
        if len(p) > 40 and not any(b in p.lower()[:60] for b in BOILER):
            par.append(p)
    if len(par) < 2:
        return ""
    body = "\n".join(par)
    if len(body) > 4000:                      # potong artikel raksasa
        body = body[:4000]
    return f"\n=== {judul} ===\n{body}\n"


def uji_arti(n, tujuan="-"):
    """Tes cepat: ambil n artikel, tampilkan + hitung yield."""
    total = 0
    seen = set()
    t0 = time.time()
    for _ in range(max(1, (n + 20 - 1) // 20)):
        for judul, teks in ambil_artikel(n=20):
            if judul in seen:
                continue
            seen.add(judul)
            bersih = bersihkan(teks, judul)
            total += len(bersih)
            print(f"[{len(seen):>3}] ({len(bersih):>5} chr) {judul[:60]}")
        time.sleep(1.0)
    print(f"\nARTIKEL: {len(seen)} | bersih: {total} chr | {time.time()-t0:.0f}s")
    return total


def jemur(tujuan, target, arti_max, resume_judul=None):
    """Loop penjemuran sampai target/sahih habis."""
    seen = set()
    if resume_judul and os.path.exists(resume_judul):
        try:
            seen.update(open(resume_judul, encoding="utf-8").read().splitlines())
        except Exception:
            pass
    total = 0
    if os.path.exists(tujuan):
        total = os.path.getsize(tujuan)
    print(f"Korpus awal: {total} byte | judul{len(seen)} | target {target}")
    t0 = time.time()
    loop = 0
    while total < target and (arti_max <= 0 or len(seen) < arti_max):
        batch = 20
        try:
            items = ambil_artikel(batch)
        except Exception as e:
            print(f"  batas API {e}; jeda 5s")
            time.sleep(5)
            continue
        for judul, teks in items:
            if judul in seen:
                continue
            seen.add(judul)
            bersih = bersihkan(teks, judul)
            if bersih:
                with open(tujuan, "a", encoding="utf-8") as fh:
                    fh.write(bersih)
                total += len(bersih)
            if resume_judul:
                with open(resume_judul, "a", encoding="utf-8") as f:
                    f.write(judul + "\n")
        loop += 1
        if loop % 10 == 0:
            dt = time.time() - t0
            print(f"  [{len(seen)} judul | {total:,} byte | {total/(dt+1e-9):,.0f} b/s]")
        time.sleep(1.2)                          # sopan santun API
    dt = time.time() - t0
    print(f"\nSELESAI: {len(seen)} judul | {total:,} byte | {dt/60:.1f} mnt | {target-total} byte kurang" if total < target else f"\nTARGET TERCAPAI: {total:,} byte")
    return total


def ambil_titles_kat(kategori, maks=2000):
    """Kumpulkan judul page dalam satu kategori (paginated)."""
    titles = []
    cont = {}
    while len(titles) < maks:
        p = {"action": "query", "generator": "categorymembers",
             "gcmtitle": kategori, "gcmnamespace": 0, "gcmtype": "page",
             "gcmlimit": "500", "format": "json", **cont}
        d = _req(p)
        q = d.get("query", {}).get("pages", {}) or {}
        titles.extend(list(q.keys()))
        cont = d.get("continue", {})
        if not cont:
            break
        time.sleep(0.8)
    return list(dict.fromkeys(titles))


def ambil_teks_by_id(pageids):
    """Ambil extract teks polos utk pageids (batch <=50)."""
    out = []
    for i in range(0, len(pageids), 50):
        chunk = pageids[i:i + 50]
        d = _req({"action": "query", "pageids": "|".join(chunk),
                  "prop": "extracts", "explaintext": 1, "exlimit": "max",
                  "format": "json", "utf8": 1})
        for pg in (d.get("query", {}).get("pages", {}) or {}).values():
            t = pg.get("extract", "")
            if t:
                out.append((pg.get("title", ""), t))
        time.sleep(0.8)
    return out


def jemur_kategori(kategori, tujuan, target, arti_max):
    """Kualitas > kuantitas: seluruh page dari BEBERAPA kategori (koma)."""
    kats = [k.strip() for k in kategori.split(",") if k.strip()]
    print(f"Kategori: {kats}")
    pgids = []
    for kat in kats:
        got = ambil_titles_kat(kat, arti_max or 2000)
        pgids += [p for p in got if p not in pgids]
    print(f"  {len(pgids)} page unik. Ambil teks...")
    total = os.path.getsize(tujuan) if os.path.exists(tujuan) else 0
    seen = set()
    t0 = time.time()
    items = ambil_teks_by_id(pgids)
    for judul, teks in items:
        if judul in seen or total >= target:
            break
        seen.add(judul)
        bersih = bersihkan(teks, judul)
        if bersih:
            with open(tujuan, "a", encoding="utf-8") as fh:
                fh.write(bersih)
            total += len(bersih)
    print(f"  {len(seen)} artikel. TOTAL {tujuan}: {total:,} byte "
          f"({time.time()-t0:.0f}s)")
    return total


def gabung(sumber, tujuan, max_baris_duplikat=1_000_000):
    """Gabung korpus lokal + dedup baris -> satu file bersih. Langsung jalan
    di HP tanpa internet. `sumber` = daftar path (koma/pola glob)."""
    import glob as _glob
    files = []
    for s in sumber.split(","):
        s = s.strip()
        files += _glob.glob(s) if _glob.has_magic(s) else [s]
    total_in = 0
    lines = []
    for f in files:
        if not os.path.exists(f):
            print(f"  skip (tidak ada): {f}")
            continue
        n = os.path.getsize(f)
        total_in += n
        try:
            lines += open(f, encoding="utf-8", errors="replace").read().splitlines()
        except Exception as e:
            print(f"  skip {f}: {e}")
            continue
    dedup = list(dict.fromkeys(lines))
    with open(tujuan, "w", encoding="utf-8") as fh:
        fh.write("\n".join(dedup) + "\n")
    print(f"GABUNG: {len(files)} file, {total_in:,} byte in -> "
          f"{len(dedup):,} baris unik -> {os.path.getsize(tujuan):,} byte ({tujuan})")
    return total_in


def main():
    ap = argparse.ArgumentParser(description="Ekspansi korpus Wikipedia id (CC BY-SA)")
    ap.add_argument("--tujuan", default="korpus_besar.txt")
    ap.add_argument("--target", type=int, default=10_000_000)
    ap.add_argument("--arti", type=int, default=0, help="batas jumlah artikel (0=infinite)")
    ap.add_argument("--kategori", default="",
                    help="mode kualitas: kategori dipisah koma (mis. Kategori:Artikel pilihan,Kategori:Artikel bagus)")
    ap.add_argument("--gabung", default="",
                    help="mode lokal: gabung korpus existing (koma/glob) + dedup, tanpa internet")
    ap.add_argument("--resume", default="", help="file daftar judul utk dedup antar run")
    ap.add_argument("--uji-arti", type=int, default=0, help="mode tes: ambil N artikel, tampilkan")
    args = ap.parse_args()

    if args.uji_arti:
        uji_arti(args.uji_arti)
    elif args.gabung:
        gabung(args.gabung, args.tujuan)
    elif args.kategori:
        jemur_kategori(args.kategori, args.tujuan, args.target, args.arti)
    else:
        jemur(args.tujuan, args.target, args.arti, args.resume or (args.tujuan + ".judul"))


if __name__ == "__main__":
    main()