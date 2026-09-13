# ==========================================
# SERVER - Pustaka Standar Aksara: HTTP server mini
# ==========================================
# Handler = skrip .ak yang membaca file request JSON & menulis file response.
# Skrip handler terima 2 argumen baris-perintah: jalur_req, jalur_res.
# Contoh handler (balasan.ak):
#   impor "json.ak" sbg j
#   req = j.urai(proses.baca_file(arg[1]))
#   baca res: tulis_file(arg[2], "halo")
# jalankan utk server: python3 -m aksara server_loader.ak, ATAU mulai().

impor "aksara._ffi.sistem" sbg S

fun mulai(port = 8080, jalan_handler = "", jalan_stop = "/tmp/ak_http") {
    jika jalan_handler == "" {
        galat "server.mulai butuh jalan_handler (skrip .ak)"
    }
    # jalankan blokir (serve_forever) — panggil dari proses/thread tersendiri
    balik S.mulai_server(port, jalan_handler, jalan_stop)
}