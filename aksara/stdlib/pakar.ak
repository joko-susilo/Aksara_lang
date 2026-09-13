# ==========================================
# PAKAR - Pustaka Standar Aksara: AI ahli (Aksara/Python/Kotlin/JS/Android/BugHunt)
# ==========================================

impor "aksara.ai.pakar" sbg pk

fun jawab(teks) {
    # balikan teks jawaban dari pakar
    balik pk.jawab(teks)
}

fun cari_stack(teks) {
    # balik [stack, kamus fitur] atau nil bila stack None
    r = pk.cari_stack(teks)
    jika r == nil {
        balik nil
    }
    jika r[0] == nil atau r[0] == "None" {
        balik nil
    }
    balik r
}

fun bahasa(teks) {
    balik pk.cek_bahasa(teks)
}