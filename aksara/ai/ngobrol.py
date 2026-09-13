# Copyright 2026 Joko Susilo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Ngobrol — percakapan generatif ringan (tanpa LLM besar).

Klasifikasikan pertanyaan terbuka ke kelas kecil, lalu jawab dengan kalimat
templat yang alami. Hemat: tabel kecil, nol model besar.

Kelas:
  opini    : "gimana pendapatmu", "apa pendapat"
  alasan   : "kenapa", "mengapa"
  perasaan : "senang", "sedih", kesan, dsb
  saran    : "saran", "tips", "sebaiknya"
  definisi : "itu apa", "apa itu"
  smalltalk: lainnya (perkenalan/umum)
"""

import re


def _norm(teks):
    return teks.lower().strip()


def klasifikasi(teks):
    t = _norm(teks)
    if re.search(r"(pendapat|menurutmu|menurut anda|opini)", t):
        return "opini"
    if re.search(r"(kenapa|mengapa|alasan)", t):
        return "alasan"
    if re.search(r"(senang|sedih|marah|capek|stress|kesan|bagus|hebat)", t):
        return "perasaan"
    if re.search(r"(saran|tips|sebaiknya|seharusnya|caranya agar)", t):
        return "saran"
    if re.search(r"(apa itu|itu apa|definis)", t):
        return "definisi"
    if re.search(r"(siapa kamu|namamu|kamu apa|asal)", t):
        return "perkenalan"
    return "smalltalk"


BALASAN = {
    "opini": [
        "Menarik! Menurutku, lebih baik lihat dari sisi manfaatnya dulu.",
        "Pandangan saya sederhana: kalau benar untuk banyak orang, layak dipertimbangkan.",
        "Aku pikir ada beberapa sudut — yang penting dampaknya positif.",
    ],
    "alasan": [
        "Alasannya biasanya karena manfaat yang jelas buat banyak orang.",
        "Bisa jadi karena kebutuhan, atau karena memang sudah jadi polanya.",
        "Hmm, kemungkinan besar karena itu lebih masuk akal dalam praktiknya.",
    ],
    "perasaan": [
        "Wajar kalau kamu merasa begitu. Yang penting kamu tetap tenang dan jernih.",
        "Terima kasih sudah berbagi. Setiap perasaan itu valid, ya.",
        "Semoga hari-harimu makin baik. Jangan ragu dukung dirimu sendiri.",
    ],
    "saran": [
        "Saran ku: mulai dari yang kecil dulu, konsisten, lalu naik bertahap.",
        "Coba pikirkan hasil yang kamu mau, lalu pecah jadi langkah-langkah sederhana.",
        "Tips: jangan terlalu keras dengan diri sendiri — proses itu penting.",
    ],
    "definisi": [
        "Secara sederhana, itu adalah konsep yang menjelaskan sesuatu secara jelas.",
        "Definisinya bisa singkat: sesuatu yang punya arti dan fungsi tertentu.",
        "Kalau diartikan umum, itu adalah hal yang mudah dipahami siapa pun.",
    ],
    "perkenalan": [
        "Aku Asisten Aksara — AI teks kecil yang offline dan hemat daya.",
        "Aku model bahasa mini buatan sendiri, jalan di perangkat tanpa internet.",
        "Namaku Aksara. Aku bantu kamu tanya-jawab, hitung, dan ngobrol ringan.",
    ],
    "smalltalk": [
        "Menarik, ceritakan lebih lanjut dong.",
        "Hmm, itu bisa jadi topik yang seru. Apa yang membuatmu bertanya begitu?",
        "Saya mendengarkan. Ada hal tertentu yang ingin kamu bahas?",
    ],
}


def jawab(teks, benih=0):
    kls = klasifikasi(teks)
    pilihan = BALASAN.get(kls, BALASAN["smalltalk"])
    idx = len(_norm(teks)) % len(pilihan)  # deterministik & ringan
    return pilihan[idx]