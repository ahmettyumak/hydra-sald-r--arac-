# Hydra Brute Force Saldırı Aracı

## Basit Kullanım

Artık `python main.py` yazmaya gerek yok! Sadece IP ve parametreleri yazın:

### Etkileşimli Mod
```bash
python main.py
# Program açıldıktan sonra:
192.168.1.1 -h
192.168.1.1 -s ssh
192.168.1.1 -n
```

### Komut Satırı Modu
```bash
python main.py 192.168.1.1 -h
python main.py 192.168.1.1 -s ssh -t 8
python main.py 192.168.1.1 -s ftp -L users.txt -P pass.txt
```

## Parametreler

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
