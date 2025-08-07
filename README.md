# BruteForce Security Tool

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Çoklu servis brute-force saldırı aracı (Ethical Hacking ve penetrasyon testleri için)

## 📌 Özellikler

- 10+ farklı servis desteği (SSH, FTP, HTTP, MySQL vb.)
- Hydra entegrasyonu ile yüksek performans
- Detaylı raporlama sistemi
- Modüler yapı (yeni servisler kolayca eklenebilir)
- Kullanıcı dostu arayüz

## 🚀 Kurulum

### Önkoşullar
- Python 3.6+
- THC-Hydra (`sudo apt install hydra` veya `brew install hydra`)

### Adım Adım Kurulum
```bash
# 1. Repoyu klonla
git clone https://github.com/kullaniciadiniz/bruteforce-tool.git
cd bruteforce-tool

# 2. Gerekli dizinleri oluştur
mkdir -p wordlists reports sonuclar

# 3. Örnek wordlistleri oluştur
echo -e "admin\nroot\nuser\ntest" > wordlists/users.txt
echo -e "123456\npassword\nadmin\n12345" > wordlists/passwords.txt

# 4. Programı çalıştır
python main.py

⚠️ Sorumluluk Reddi
Bu araç sadece yasal etik hackleme ve penetrasyon testleri için geliştirilmiştir. Kullanımından kullanıcı sorumludur. Yasa dışı faaliyetlerde kullanımı kesinlikle yasaktır.
