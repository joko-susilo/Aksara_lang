# ==========================================
# DEMO: KB Kaya (pengayaan knowledge base)
# ==========================================

impor "kb_rich.ak" sbg KBR
impor "kb_lookup.ak" sbg KBL
impor "bahasa_id.ak" sbg BID

cetak "== KB KAYA — pengayaan multi-kategori =="
cetak ""
pertanyaan = [
    "csoto itu apa?",
    "berapa harga paket pro?",
    "gimana cara daftar?",
    "kuota gimana dihitung?",
    "cara broadcast promo di telegram?",
    "gak tau fitur apa aja",
    "biaya meta per pesan gimana?",
    "aktivasi whatsapp caranya?",
]
untuk i dalam 0 .. panjang(pertanyaan) - 1 {
    norm = BID.normalisasi(pertanyaan[i])
    cari = KBL.cari(KBR.kb_rich, norm)
    cetak "Tanya : " + pertanyaan[i]
    jika cari != nil {
        cetak "  (match: '" + cari[1] + "')"
        cetak "  AI  : " + cari[0]
    } lain {
        cetak "  AI  : (tidak ditemukan)"
    }
    cetak ""
}