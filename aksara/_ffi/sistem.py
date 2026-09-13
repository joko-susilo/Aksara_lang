# Copyright 2026 Joko Susilo
# Licensed under the Apache License, Version 2.0 (the "License");
"""FFI Aksara -> Python (backend sah: logika di .ak, mesin di sini).

Menyediakan: subprocess, lingkungan, CLI args, regex, server HTTP mini,
paralel task (subprocess). Konsep: Aksara = logika; modul ini = pekerja berat.
"""

import os
import sys
import re as _re
import subprocess
import json
import glob as _glob


# ======================================================================
# SUBPROCESS + LINGKUNGAN + CLI
# ======================================================================
def jalankan(perintah, cwd="", timelimit=60, tangkap=True):
    """Jalankan perintah (list) -> {kode, keluar, kesalahan}."""
    try:
        r = subprocess.run(
            perintah, capture_output=tangkap, text=True, timeout=timelimit,
            cwd=cwd or None)
        return {"kode": r.returncode, "keluar": r.stdout or "",
                "kesalahan": r.stderr or ""}
    except subprocess.TimeoutExpired as e:
        return {"kode": -99, "keluar": e.stdout or "",
                "kesalahan": f"timeout {timelimit}s"}
    except Exception as e:
        return {"kode": -1, "keluar": "", "kesalahan": str(e)}


def lingkungan():
    """Kamus env saat ini (semua string)."""
    return dict(os.environ)


def env_ambil(nama, bawa_default=""):
    return os.environ.get(nama, bawa_default)


def env_setel(nama, nilai):
    os.environ[nama] = str(nilai)
    return True


def argumen_cli():
    """Argumen baris-perintah proses ini (list)."""
    return list(sys.argv)


# ======================================================================
# REGEX (re asli)
# ======================================================================
def regex_cari(pola, teks):
    m = _re.search(pola, teks)
    if not m:
        return []
    return [{"mulai": m.start(), "akhir": m.end(), "cocok": m.group(0),
             "kelompok": list(m.groups())}]


def regex_semua(pola, teks):
    return [{"cocok": m.group(0), "kelompok": list(m.groups())}
            for m in _re.finditer(pola, teks)]


def regex_ganti(pola, pengganti, teks):
    return _re.sub(pola, pengganti, teks)


def regex_pisah(pola, teks):
    return _re.split(pola, teks)


# ======================================================================
# HTTP SERVER MINI (hook: satu skrip .ak per request)
# ======================================================================
def _server_harus_berhenti():
    return not os.path.exists(os.environ.get("AKSARA_SERVER_STOP", "/tmp/ak_stop"))


def mulai_server(port, jalan_handler="", jalan_stop="", host="0.0.0.0"):
    """Server HTTP sederhana. Tiap request:
      - tulis reques json ke {jalan_stop}-req.json
      - jalankan `python3 -m aksara {jalan_handler} {jalan_stop}-req.json {jalan_stop}-res.json`
      - kembalikan isi -res.json (atau teks polos)
    jalan_stop: prefix file request/response. Aman: tanpa handler -> 404."""
    from http.server import BaseHTTPRequestHandler, HTTPServer
    import threading

    if not jalan_handler:
        raise ValueError("butuh jalan_handler (skrip .ak)")

    class Penangan(BaseHTTPRequestHandler):
        def _tanggap(self):
            try:
                panjang = int(self.headers.get("Content-Length") or 0)
                badan = self.rfile.read(panjang).decode("utf-8", "replace") if panjang else ""
                req_f = f"{jalan_stop}-req.json"
                res_f = f"{jalan_stop}-res.json"
                payload = {"metode": self.command,
                           "jalan": self.path,
                           "badan": badan,
                           "header": dict(self.headers)}
                with open(req_f, "w") as f:
                    json.dump(payload, f, ensure_ascii=False)
                if os.path.exists(res_f):
                    os.remove(res_f)
                env = dict(os.environ)
                env["AKSARA_REQ_JSON"] = req_f
                env["AKSARA_RES_JSON"] = res_f
                subprocess.run(
                    [sys.executable, "-m", "aksara", jalan_handler],
                    timeout=30, capture_output=True, env=env)
                if os.path.exists(res_f):
                    keluar = open(res_f, encoding="utf-8").read()
                else:
                    keluar = "server aksara: tidak ada respons\n"
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(keluar.encode("utf-8"))
            except Exception as e:
                try:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(str(e).encode("utf-8", "replace"))
                except Exception:
                    pass

        def do_GET(self): self._tanggap()
        def do_POST(self): self._tanggap()

    server = HTTPServer((host, int(port)), Penangan)
    server.serve_forever()


# ======================================================================
# PARALEL (subprocess + thread pool)
# ======================================================================
def jalan_paralel(tugas, concurrency=3, cwd=""):
    """tugas: daftar perintah (list). Balik list hasil utk tiap tugas.
    Benar-benar paralel via subprocess (GIL tak membatasi)."""
    import concurrent.futures
    hasil = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(concurrency)) as ex:
        futs = [ex.submit(jalankan, t, cwd) for t in tugas]
        for f in futs:
            try:
                hasil.append(f.result())
            except Exception as e:
                hasil.append({"kode": -1, "keluar": "", "kesalahan": str(e)})
    return hasil


# ======================================================================
# GLOB / PATH (buat tooling)
# ======================================================================
def glob_list(pola):
    return sorted(_glob.glob(pola))


def jalur_ada(jalur):
    return os.path.exists(jalur)

# ======================================================================
# FILE SYSTEM (buat paket.ak)
# ======================================================================
def salin_file(sumber, tujuan):
    import shutil
    os.makedirs(os.path.dirname(tujuan), exist_ok=True)
    shutil.copyfile(sumber, tujuan)
    return True


def daftar_dir(jalur, akhiran=""):
    if not os.path.isdir(jalur):
        return []
    return sorted(f for f in os.listdir(jalur) if f.endswith(akhiran))
