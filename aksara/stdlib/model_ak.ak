# ==========================================
# MODEL_AK - Mini-LM DITULIS MURNI di Aksara (tanpa backend .py)
# ==========================================
# Filosofi: seluruh logika model (forward, backward, update) ditulis
# dalam bahasa Aksara. NumPy hanya kalkulator (impor langsung),
# BUKAN backend buatan kita yang menyimpan logika.

impor "numpy" sbg np

# ---------- fungsi dasar (Aksara) ----------
fun softmax(x) {
    # x: 2D (T,V) -> softmax per baris
    mx = np.max(x, 1, benar)          # (T,1) keepdim via axis
    # Aksara: np.max(x, axis=1, keepdims=True)
    e = np.exp(x - mx)
    balik e / np.sum(e, 1, benar)
}

fun relu(x) {
    balik np.maximum(0, x)
}

fun layer_norm(x, g, b) {
    mu = np.mean(x, 1, benar)
    var = np.var(x, 1, benar)
    balik g * (x - mu) / np.sqrt(var + 0.00001) + b
}

# ---------- forward 1-lapisan (murni Aksara) ----------
fun forward(model, ids, blok) {
    Wte = model["Wte"]
    Wpe = model["Wpe"]

    # 1) embedding + posisi
    ix = np.array(ids)
    x = Wte[ix] + Wpe[0 .. panjang(ids) - 1]

    d = panjang(Wte[0])

    # 2) attention (1 kepala utk kesederhanaan)
    Wq = model["Wq"]
    Wk = model["Wk"]
    Wv = model["Wv"]
    Wo = model["Wo"]
    q = np.dot(x, Wq)
    k = np.dot(x, Wk)
    v = np.dot(x, Wv)

    # skor = q . k^T / sqrt(d)
    skor = np.dot(q, np.transpose(k)) / np.sqrt(d + 0.0)
    # mask causal (tiap posisi hanya lihat sebelumnya)
    # mask causal lewat matriks 2D eksplisit (hindari slicing [:,None])
    T = panjang(ids)
    # buat matriks perbandingan j>i pakai dua array 1D yang di-broadcast
    # (Aksara np bisa broadcast (T,)@(T,1) — kita bentuk (T,1) via reshape)
    baris_idx = np.arange(T)
    kolom_idx = np.arange(T).reshape(T, 1)
    mask = np.where(kolom_idx > baris_idx, -1000000000, 0)
    skor = skor + mask
    pr = softmax(skor)
    att = np.dot(pr, v)
    att_out = np.dot(att, Wo)

    # 3) residual + norm
    x2 = layer_norm(x + att_out, model["ln1g"], model["ln1b"])

    # 4) FFN (tanpa MoE dulu)
    hidden = relu(np.dot(x2, model["W1"]) + model["b1"])
    ffn = np.dot(hidden, model["W2"]) + model["b2"]
    x_out = layer_norm(x2 + ffn, model["ln2g"], model["ln2b"])

    # 5) proyeksi ke vocab
    logits = np.dot(x_out, model["Wlr"]) + model["blr"]

    simpan_model = ["x": x, "q": q, "k": k, "v": v, "skor": skor, "pr": pr,
        "att": att, "att_out": att_out, "x2": x2, "hidden": hidden,
        "ffn": ffn, "x_out": x_out, "logits": logits, "ids": ids]
    balik [logits, simpan_model]
}

# ---------- fungsi bantu Python bawa numpy ----------
fun uji_forward(model, ids, blok) {
    hasil = forward(model, ids, blok)
    balik hasil[0]
}