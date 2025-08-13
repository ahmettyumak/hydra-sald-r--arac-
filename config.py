import os

class Ayarlar:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Dosya yolları
    KULLANICI_ADI_LISTESI = os.path.join(BASE_DIR, "wordlists", "users.txt")
    PAROLA_LISTESI = os.path.join(BASE_DIR, "wordlists", "passwords.txt")
    RAPOR_DOSYASI = os.path.join(BASE_DIR, "reports", "sonuc_raporu.txt")
    
    # Nmap ayarları (None -> Nmap varsayılanı: en yaygın 1000 TCP port)
    NMAP_PORT_ARALIGI = None
    NMAP_ARGUMANLARI = '-sS -sV --script=banner -T4 --open'
    
    # Hydra ayarları
    HYDRA_TIMEOUT = 180  # Daha hızlı geri dönüş için düşürüldü (kullanıcı -W ile artırabilir)
    HYDRA_THREADS = 6  # Varsayılanı biraz artırıldı; kullanıcı -t ile değiştirebilir
    
    # Özel servis ayarları kaldırıldı - manuel hydra komutlarıyla uyumlu olması için
    
    # Port check ayarları
    PORT_CHECK_TIMEOUT = 3
    PORT_CHECK_THREADS = 50
    
    # Port ayarları
    PORTLAR = {
        "ftp": 21,
        "ssh": 22,
        "http": 80,
        "https": 443,
        "mysql": 3306,
        "postgresql": 5432,
        "mongodb": 27017,
        "smtp": 25,
        "pop3": 110,
        "imap": 143,
        "rdp": 3389,
        "smb": 445,
        "telnet": 23,
        "vnc": 5900,
        "mssql": 1433
    }