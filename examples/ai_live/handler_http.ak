# Handler HTTP Aksara — baca req JSON via env, tulis res ke AKSARA_RES_JSON.
# Dijalankan oleh server.ak (FFI) lewat env:
#   AKSARA_REQ_JSON = jalan file request ; AKSARA_RES_JSON = jalan file respons
impor "json.ak" sbg j
impor "berkas.ak" sbg b
impor "proses.ak" sbg P

req_j = P.env_ambil("AKSARA_REQ_JSON")
res_j = P.env_ambil("AKSARA_RES_JSON")
req = j.urai(b.baca_file(req_j))
cetak "handler dipanggil: " + teks(req["jalan"])

pesan = "Halo dari server Aksara! Jalan: " + teks(req["jalan"]) + " | metode: " + teks(req["metode"])
b.tulis_file(res_j, pesan)
cetak "respons ditulis"