# ==========================================
# WEB - Pustaka Standar Aksara: HTTP
# ==========================================
# Perlu library eksternal 'requests' di Python.
#   pip install requests

impor "requests" sbg req

fun dapat(url, params = nil) {
    balik req.get(url)
}

fun dapat_teks(url, params = nil) {
    balik req.get(url).text
}

fun dapat_json(url, params = nil) {
    balik req.get(url).json()
}

fun kirim(url, data = nil) {
    balik req.post(url, json = data)
}

fun status(url) {
    balik req.get(url).status_code
}

fun header(url, nama) {
    balik req.get(url).headers.get(nama)
}