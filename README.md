# BruteForce Security Tool

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Çoklu servis brute-force saldırı aracı (Ethical Hacking ve penetrasyon testleri için)

## 📌 Özellikler

- 15+ farklı servis desteği (SSH, FTP, HTTP, MySQL, MongoDB vb.)
- Parametrik giriş sistemi (-h, -p, -n, -s)
- Port check ile otomatik servis tespiti
- Nmap entegrasyonu ile detaylı tarama
- Console output ile gerçek zamanlı sonuçlar
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

## 🚀 Kullanım Örnekleri

```bash
# Tüm servislere saldırı
python main.py 192.168.1.1 -h

# Belirli servise saldırı
python main.py 192.168.1.1 -s ssh

# Çoklu servis saldırısı
python main.py 192.168.1.1 -s ftp -s ssh -s http

# Thread sayısı ve timeout ile
python main.py 192.168.1.1 -s ssh -t 8 -W 60

# Özel wordlist ile
python main.py 192.168.1.1 -s ssh -L users.txt -P passwords.txt

# Verbose ve debug mod ile
python main.py 192.168.1.1 -s http -V -d

# Tek kullanıcı/şifre ile
python main.py 192.168.1.1 -s ssh -l admin -p password123

# İlk bulunanı durdur
python main.py 192.168.1.1 -s ftp -f

# Nmap ile detaylı tarama
python main.py 192.168.1.1 -n

# Port check ile saldırı (varsayılan)
python main.py 192.168.1.1

# Etkileşimli mod
python main.py
```

## 📋 Parametreler

### Temel Parametreler
- `-h`: Tüm servislere saldırı
- `-s [servis]`: Belirli servis seçimi (örn: ssh, ftp, http)
- `-n`: Nmap ile detaylı tarama

### Hydra Parametreleri
- `-L [dosya]`: Kullanıcı listesi dosyası
- `-P [dosya]`: Şifre listesi dosyası
- `-l [kullanıcı]`: Tek kullanıcı
- `-p [şifre]`: Tek şifre
- `-t [sayı]`: Thread sayısı (varsayılan: 4)
- `-W [saniye]`: Timeout süresi (varsayılan: 30)
- `-s [port]`: Port numarası
- `-V`: Verbose mod
- `-d`: Debug mod
- `-f`: İlk bulunanı durdur
- `-R`: Restore session
- `-o [dosya]`: Çıktı dosyası
- `-b [dosya]`: Log dosyası
- `-x`: XML çıktı
- `-F [parametreler]`: Form parametreleri
- `-C [dosya]`: Özel parametre dosyası
- `-M [dosya]`: Modül dosyası
- `-m [servis]`: Servis adı
⚠️ Sorumluluk Reddi
Bu araç sadece yasal etik hackleme ve penetrasyon testleri için geliştirilmiştir.
Kullanımından kullanıcı sorumludur. Yasa dışı faaliyetlerde kullanımı kesinlikle yasaktır.
