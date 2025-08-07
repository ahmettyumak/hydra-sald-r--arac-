import os

class Ayarlar:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Dosya yolları
    KULLANICI_ADI_LISTESI = os.path.join(BASE_DIR, "wordlists", "users.txt")
    PAROLA_LISTESI = os.path.join(BASE_DIR, "wordlists", "passwords.txt")
    RAPOR_DOSYASI = os.path.join(BASE_DIR, "reports", "sonuc_raporu.txt")
    

    # Port ayarları
    PORTLAR = {
        "ftp": 21,
        "ssh": 22,
        "http": 80,
        "https": 443,
        "mysql": 3306,
        "postgresql": 5432,
        "smtp": 25,
        "pop3": 110,
        "imap": 143,
        "rdp": 3389,
        "smb": 445,
        "telnet": 23,
        "vnc": 5900,
        "mssql": 1433
    }
    
    # Hydra ayarları
    HYDRA_TIMEOUT = 30
    HYDRA_THREADS = 4