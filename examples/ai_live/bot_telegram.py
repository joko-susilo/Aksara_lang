#!/usr/bin/env python3
"""Bot Telegram 'Aksara' — AI Super Pintar, murni HTTP Bot API (requests).

Tanpa library telegram tambahan (hemat ruang). Pakai mesin AI Aksara
(asisten.ak + pipeline + hitung) lewat interpreter.

Cara: TELEGRAM_TOKEN=... python3 bot_telegram.py
Token dari @BotFather.
"""

import os
import sys
import time
import threading
import subprocess

import requests

TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
API = f"https://api.telegram.org/bot{TOKEN}"
DIR = "/root/projects/aksara_lang"

# Kode Aksara yang berisi logika jawab (balas via otak pintar + KB kaya).
PREP = r"""
impor "teks.ak" sbg t
impor "pintar.ak" sbg P
impor "pipeline.ak" sbg pl
impor "berkas.ak" sbg f
impor "belajar.ak" sbg B
impor "kb_rich.ak" sbg KBR
impor "kb_lookup.ak" sbg KBL
impor "bahasa_id.ak" sbg BID
impor "pakar.ak" sbg PKAR
impor "hitung.ak" sbg H

kb = ["_human_words": "admin petugas orang manusia",
    "_human_reply": "Baik, saya siapkan bantuan dari tim. Sebentar ya.",
    "_greet_words": "halo hai pagi siang malam assalamu",
    "_greet_reply": "Halo! Saya asisten Csoto. Tanya soal harga, paket, kuota, broadcast, cara daftar, atau koding/bug hunting.",
    "_default": "Hmm, saya belum paham. Coba tanya harga, paket, hitung, atau hal tentang coding/bug hunting ya 🙏"]

isi = f.baca_file("examples/ai_live/korpus_persona.txt")
pipe = pl.latih(isi, 100, 12, 24, 1, 1, 120, 0.02, 0, benar)
fun generator(pesan) { balik pl.ucap(pipe, pesan, 20, 0.4) }

fun jawab_bot(pesan) {
     rendah_bot = t.huruf_kecil(t.potong_teks(pesan))
     # perintah belajar dulu
     jika t.awalan(rendah_bot, "ingat ") {
         balik B.ingat("/root/projects/aksara_lang/examples/ai_live/belajar_ai.txt", pesan)
     }
     # cek fakta belajar
     fk = B.jawab_dari("/root/projects/aksara_lang/examples/ai_live/belajar_ai.txt", pesan)
     jika fk != nil {
         balik fk
     }
     # pakar (coding / bug hunting) — routing berdasar stack domain
     jelajah = PKAR.cari_stack(pesan)
     jika jelajah != nil {
         balik PKAR.jawab(pesan)
     }
     # hitung (angka jelas)
     hh = H.hitung(pesan)
     jika hh != nil {
         balik "Hasilnya " + hh[0] + " (" + hh[1] + ")"
     }
     # normalisasi & cari KB kaya
     norm = BID.normalisasi(pesan)
     cari_kb = KBL.cari(KBR.kb_rich, norm)
     jika cari_kb != nil {
         balik cari_kb[0]
     }
     # asisten pintar (fallback)
     hasil_p = P.jawab_pintar(kb, pesan, generator, "/root/projects/aksara_lang/examples/ai_live/belajar_ai.txt", "/root/projects/aksara_lang/examples/ai_live/korpus_persona.txt")
     jika hasil_p == nil {
         balik kb["_default"]
     }
     balik hasil_p
 }
 """

MEBELAJAR = "/root/projects/aksara_lang/examples/ai_live/belajar_ai.txt"
MEKORPUS = "/root/projects/aksara_lang/examples/ai_live/korpus_persona.txt"

# ---- GENERATOR v4 (opsional, auto) -------------------------------
# Kalau artifact model_v4.pkl + bpe_v4.pkl ada (hasil latih_pipeline_v4),
# generator bot beralih ke Mini-LM v4 (backprop lengkap, benar-benar belajar).
ARTEFAK_MODEL = "/root/projects/aksara_lang/examples/ai_live/artifak/model_v4.pkl"
ARTEFAK_BPE = "/root/projects/aksara_lang/examples/ai_live/artifak/bpe_v4.pkl"
_V4_AKTIF = os.path.exists(ARTEFAK_MODEL) and os.path.exists(ARTEFAK_BPE)

PREP_V4 = r"""
impor "model_v4.ak" sbg M4
model4 = M4.baca_serial("examples/ai_live/artifak/model_v4.pkl")
bpe4 = M4.baca_serial("examples/ai_live/artifak/bpe_v4.pkl")
""" + PREP.replace(
    'fun generator(pesan) { balik pl.ucap(pipe, pesan, 20, 0.4) }',
    """fun generator(pesan) {
     ids = M4.ubah_id(bpe4, pesan)
     out = M4.tulis(model4, ids[0..5], 24, 0.7, 0)
     balik M4.balik_teks(bpe4, out)
 }""")

def jawab(pesan):
    """Semua kecerdasan di Aksara; Python hanya saluran Telegram."""
    import tempfile
    pokok = PREP_V4 if _V4_AKTIF else PREP
    kode = (
        pokok + "\n"
        f'cetak jawab_bot("{_escape(pesan)}")\n'
    )
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".ak", delete=False) as f:
            f.write(kode)
            tmp = f.name
        r = subprocess.run(
            [sys.executable, "-m", "aksara", tmp],
            capture_output=True, text=True, timeout=60, cwd=DIR,
        )
        os.unlink(tmp)
        if r.returncode != 0:
            return f"(err) {r.stderr.strip()[-300:]}"
        return r.stdout.strip() or "(kosong)"
    except Exception as e:
        return f"(gagal) {e}"


def _escape(s):
    return s.replace('"', "'").replace("\n", " ")[:200]


def get_me():
    r = requests.get(f"{API}/getMe", timeout=10)
    return r.json()


def get_updates(offset):
    r = requests.get(f"{API}/getUpdates",
                     params={"offset": offset, "timeout": 20}, timeout=30)
    return r.json()


def send(chat_id, text):
    requests.post(f"{API}/sendMessage",
                  data={"chat_id": chat_id, "text": text[:4000]}, timeout=15)


def main():
    if not TOKEN:
        print("Set TELEGRAM_TOKEN dulu.")
        return
    me = get_me()
    print("Bot:", me.get("result", {}).get("username"))
    offset = 0
    while True:
        try:
            data = get_updates(offset)
        except Exception as e:
            print("updates err:", e)
            time.sleep(5)
            continue
        for upd in data.get("result", []):
            offset = upd["update_id"] + 1
            msg = upd.get("message") or upd.get("edited_message")
            if not msg or "text" not in msg:
                continue
            chat_id = msg["chat"]["id"]
            text = msg["text"]
            print(f"  <- {text[:60]}")
            threading.Thread(target=lambda: send(chat_id, jawab(text))).start()
        time.sleep(0.5)


if __name__ == "__main__":
    main()