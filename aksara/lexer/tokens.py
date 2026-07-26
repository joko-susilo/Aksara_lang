from dataclasses import dataclass

@dataclass
class Token:
    """Representasi token dengan informasi posisi di kode sumber."""
    tipe: str       # Jenis token: 'KATA_KUNCI', 'NAMA', 'ANGKA', 'STRING', 'OPERATOR', 'KURUNG', 'KURUNG_KUWAL', 'EOF'
    nilai: str      # Teks asli token
    baris: int      # Nomor baris (mulai dari 1)
    kolom: int      # Posisi kolom (mulai dari 1)

    def __repr__(self):
        return f"Token({self.tipe!r}, {self.nilai!r}, baris={self.baris}, kolom={self.kolom})"

# Daftar kata kunci resmi Aksara (versi pendek)
KATA_KUNCI = [
    # Kontrol alur
    "jika", "atau_jika", "lain",
    # Perulangan
    "ulang", "untuk", "dalam", "selama",
    # Fungsi
    "fun", "balik",
    # Output
    "cetak",
    # Kontrol loop
    "henti", "lanjut",
    # Boolean dan null
    "benar", "salah", "nil",
    # Modul
    "impor", "sbg",
    "dan","atau","bukan",
    # Error
    "coba","kecuali","akhirnya",
    "sebagai","galat"
]
