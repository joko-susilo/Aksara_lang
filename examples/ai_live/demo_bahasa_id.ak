# ==========================================
# DEMO: Parameter Bahasa Indonesia
# ==========================================
# Stemming afiks, normalisasi santai, deteksi tanya/negasi — semua Aksara.

impor "bahasa_id.ak" sbg BID

cetak "== PARAMETER BAHASA INDONESIA =="
cetak ""

cetak "1) Stemming afiks (hapus me-/ber-/ter-/di- + akhiran):"
stem_kata = ["membaca", "mengirim", "terbuka", "pembelajaran", "dipukuli"]
untuk i dalam 0 .. panjang(stem_kata) - 1 {
    akar = BID.stem_afiks(stem_kata[i])
    cetak "   '" + stem_kata[i] + "' -> " + akar[0] + " (akar: " + akar[panjang(akar) - 1] + ")"
}

cetak ""
cetak "2) Normalisasi santai (gak->tidak, aja->saja, banget->sangat):"
santai = "gak tau deh, cuma gini aja"
cetak "   '" + santai + "'"
cetak "   -> '" + BID.normalisasi(santai) + "'"

cetak ""
cetak "3) Deteksi jenis kalimat (tanya vs negasi):"
kalimat = ["apakah ini benar?", "nggak tau", "kenapa kamu pergi?", "jangan ke sana"]
untuk i dalam 0 .. panjang(kalimat) - 1 {
    tanya = BID.kata_tanya(kalimat[i])
    negas = BID.kata_negasi(kalimat[i])
    jenis = "netral"
    jika tanya {
        jenis = "tanya"
    } atau_jika negas {
        jenis = "negasi"
    }
    cetak "   '" + kalimat[i] + "' -> " + jenis
}