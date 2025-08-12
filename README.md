# Hydra Brute Force Saldırı Aracı

## Basit Kullanım

Artık `python main.py` yazmaya gerek yok! Sadece IP ve parametreleri yazın:

### Etkileşimli Mod
```bash
python main.py
# Program açıldıktan sonra:
192.168.1.1        # Port check + brute force
192.168.1.1 -h     # Tüm servislere saldırı
192.168.1.1 -s ssh # SSH servisine saldırı
192.168.1.1 -n     # Nmap taraması
```

### Komut Satırı Modu
```bash
python main.py 192.168.1.1        # Port check + brute force
python main.py 192.168.1.1 -h     # Tüm servislere saldırı
python main.py 192.168.1.1 -s ssh -t 8
python main.py 192.168.1.1 -s ftp -L users.txt -P pass.txt
```

## Parametreler

- **Sadece IP**: Port check yapıp açık portlara brute force
- `-h`: Tüm servislere saldırı
- `-s [servis]`: Belirli servis (ssh, ftp, http, mysql, vb.)
- `-n`: Nmap taraması
- `-t [sayı]`: Thread sayısı
- `-W [saniye]`: Timeout
- `-L [dosya]`: Kullanıcı listesi dosyası
- `-P [dosya]`: Şifre listesi dosyası
- `-F [parametreler]`: HTTP form parametreleri

## Örnekler

```bash
# Sadece IP - Port check + brute force
192.168.1.1

# Tüm servislere saldırı
192.168.1.1 -h

# SSH brute force, 8 thread
192.168.1.1 -s ssh -t 8

# HTTP form brute force
192.168.1.1 -s http -F "/login:username=^USER^&password=^PASS^:F=Invalid login"

# Nmap taraması
192.168.1.1 -n

# FTP özel wordlist ile
192.168.1.1 -s ftp -L users.txt -P pass.txt
```

## Desteklenen Servisler

- FTP, SSH, HTTP, HTTPS
- MySQL, PostgreSQL, MongoDB
- SMTP, POP3, IMAP
- RDP, SMB, Telnet, VNC
- MSSQL

## Not

Program artık sadece IP ve parametreleri bekliyor. `main.py` yazmaya gerek yok!

**Yeni Özellik**: Mod seçimi kaldırıldı, sadece parametrelerle çalışıyor:
- Sadece IP → Port check + brute force
- IP + -h → Tüm servislere saldırı
- IP + -s [servis] → Belirli servise saldırı
- IP + -n → Nmap taraması
