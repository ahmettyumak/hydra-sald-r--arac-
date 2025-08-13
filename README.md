# Hydra Brute Force Saldırı Aracı

## Gereksinimler

- Python 3 ve pip (Python bağımlılıkları için)
- Nmap (binary) ve Hydra (binary)
  - Debian/Ubuntu:
    - `sudo apt-get update && sudo apt-get install -y nmap hydra`
- Python paketleri:
  - `pip install -r requirements.txt`

Not: Nmap ve Hydra, sistem paketleri olarak kurulu olmalıdır. Python paketleri `python-nmap` vb. için `requirements.txt` yeterlidir.

## Hızlı Başlangıç

```bash
# Çalıştırma
python3 main.py --help

# Nmap taraması (varsayılan popüler portlar, versiyon tespiti)
python3 main.py -nmap -sV 192.168.9.131

# Nmap ileri seviye örnek (verbose, hız profili, port aralığı, script)
python3 main.py -nmap -vv -T4 -p 22,80 --script=banner 192.168.9.131

# Belirli servise brute-force (Hydra parametreleri desteklenir)
python3 main.py -L wordlists/users.txt -P wordlists/passwords.txt 192.168.9.131 ssh

# Tüm desteklenen servislere (port check ile) brute-force denemesi
python3 main.py -h 192.168.9.131

# Çoklu hedef dosyası ile (her satır bir hedef)
python3 main.py -L users.txt -P pass.txt -M targets.txt ssh
```

## Kullanım

- Söz dizimi:
  - `-nmap <target> [NMAP_OPTIONS...]`
  - `[OPTIONS] <target> <service>`
  - `[OPTIONS] -M <targets.txt> <service>`
  - `-h <target>` (desteklenen tüm servislere saldır)

- Desteklenen servisler: `FTP, SSH, HTTP, HTTPS, MySQL, PostgreSQL, MongoDB, SMTP, POP3, IMAP, RDP, SMB, Telnet, VNC, MSSQL`

### Nmap Seçenekleri (desteklenenler)
- Tarama türleri: `-sS, -sT, -sU, -sA, -sW, -sM, -sN, -sF, -sX`
- Portlar: `-p <aralık>`, `-p-` (tüm portlar)
- Hız/performans: `-F`, `-T<0-5>` veya `-T4`
- Keşif/detay: `-A`, `-O`, `-sV`, `-sC`, `--script <name>` veya `--script=<name>`
- Çıktı: `-oN <file>`, `-oX <file>`, `-oG <file>`
- Verbose/Debug: `-v, -vv, -vvv`, `-d, -dd, -ddd`
- Diğer: `-Pn` (host discovery atla), `-n` (DNS kapalı)

Varsayılan Nmap argümanları `config.py` içinde tanımlıdır: `-sS -sV --script=banner -T4 --open`

### Hydra Seçenekleri (desteklenenler)
- Listeler: `-L <file>`, `-P <file>`
- Tek kullanıcı/şifre: `-l <user>`, `-p <pass>`
- Performans: `-t <threads>`, `-W <timeout>`
- Çıktı/Log: `-o <file>`, `-b <file>`, `-x` (XML)
- Akış: `-f` (ilk başarılıda dur), `-R` (restore)
- HTTP form: `-F <form_params>` (örn: `/login:username=^USER^&password=^PASS^:F=Invalid`)
- Diğer: `-C <file>`, `-M <module>`, `-m <service>`, `-V` (verbose), `-d` (debug), `-u`, `-e <nsr>`, `-4/-6`, `-S`, `-O`, `-K`, `-q`, `-U`, `-I`
- Özel port: `-s <port>` (bizim araçta da desteklenir)

## HTTP/HTTPS Tespiti
- Araç, Nmap sonuçlarını normalize eder ve `HTTPS` ile `HTTP`’yi otomatik ayırt eder.
  - `tunnel=ssl`, servis adı `https`/`ssl/http` veya tipik portlar `443/8443/9443` → `https`
  - Diğer `http*` varyasyonları → `http`
- Böylece aynı hedefte HTTP/HTTPS çakışmaları ve tekrarlı denemeler önlenir.

## `python main.py` yazmadan çalıştırma

- Dosyayı çalıştırılabilir yapın:
```bash
chmod +x main.py
./main.py -nmap -v 192.168.9.131
```

- Veya global wrapper komutu oluşturun:
```bash
sudo tee /usr/local/bin/hydra-araci >/dev/null <<'EOF'
#!/usr/bin/env bash
python3 /full/path/to/main.py "$@"
EOF
sudo chmod +x /usr/local/bin/hydra-araci

hydra-araci -nmap -v 192.168.9.131
```

- Veya shell alias (geçerli kullanıcı için):
```bash
echo "alias hydra-araci='python3 /full/path/to/main.py'" >> ~/.bashrc
source ~/.bashrc
hydra-araci -h 192.168.9.131
```

## Wordlist ve Raporlama
- Varsayılan listeler: `wordlists/users.txt` ve `wordlists/passwords.txt`
- Sonuçlar konsola yazdırılır; ek olarak `utils/raporlayici.py` ile bellek içi rapor tutulur ve istenirse dosyaya aktarılabilir.

## Önemli Notlar
- Nmap/Hydra komutları sisteminizde yoksa kurulum gereklidir (`apt install nmap hydra`).
- Çoklu hedef için `-M targets.txt <service>` formatını kullanın (dosyada her satır bir hedef).
- Özel port için `-s <port>` parametresi verilebilir.

## Lisans
Bu proje eğitim amaçlıdır. Sadece yetkili/izinli ortamlarda kullanın.
