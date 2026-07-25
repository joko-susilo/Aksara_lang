#!/bin/bash
echo "Memasang Aksara (Versi Tunggal) ke sistem..."

TARGET_DIR="/data/data/com.termux/files/usr/bin"

# Hanya menyalin file utama 'aksara' ke sistem
cp aksara "$TARGET_DIR/"
chmod +x "$TARGET_DIR/aksara"

echo "[OK] Aksara berhasil terpasang!"
echo "Sekarang file kamus sudah menyatu, dijamin tidak akan error modul hilang!"
