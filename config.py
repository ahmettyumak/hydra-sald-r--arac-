import os

class Ayarlar:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Dosya yolları
    KULLANICI_ADI_LISTESI = os.path.join(BASE_DIR, "wordlists", "users.txt")
    PAROLA_LISTESI = os.path.join(BASE_DIR, "wordlists", "passwords.txt")
    RAPOR_DOSYASI = os.path.join(BASE_DIR, "reports", "sonuc_raporu.txt")
    
    # Nmap ayarları
    NMAP_PORT_ARALIGI = '1-1000'
    NMAP_ARGUMANLARI = '-sS -sV --script=banner -T4 --open'
    
    # Hydra ayarları
    HYDRA_TIMEOUT = 30
    HYDRA_THREADS = 4
    
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