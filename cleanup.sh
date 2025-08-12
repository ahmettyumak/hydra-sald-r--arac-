#!/bin/bash

echo "Proje klasoru temizleniyor..."
echo ""

echo "[*] __pycache__ klasorleri siliniyor..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

echo "[*] .pyc dosyalari siliniyor..."
find . -name "*.pyc" -delete 2>/dev/null

echo "[*] .pyo dosyalari siliniyor..."
find . -name "*.pyo" -delete 2>/dev/null

echo "[*] .pyd dosyalari siliniyor..."
find . -name "*.pyd" -delete 2>/dev/null

echo "[*] Gecici dosyalar siliniyor..."
find . -name "*.tmp" -delete 2>/dev/null
find . -name "*.temp" -delete 2>/dev/null
find . -name "*.log" -delete 2>/dev/null

echo "[*] IDE dosyalari siliniyor..."
rm -rf .vscode 2>/dev/null
rm -rf .idea 2>/dev/null

echo ""
echo "[+] Temizlik tamamlandi!"
echo "[+] Proje klasoru temiz tutuldu."

read -p "Devam etmek icin Enter'a basin"
