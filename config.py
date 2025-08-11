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
    HYDRA_TIMEOUT = 120  # FTP için yeterli süre
    HYDRA_THREADS = 4
    
    # FTP özel ayarları
    FTP_TIMEOUT = 60      # FTP bağlantı timeout
    FTP_THREADS = 1       # FTP tek thread (daha güvenilir)
    
    # Veritabanı servisleri özel ayarları
    DB_TIMEOUT = 90       # Veritabanı bağlantı timeout
    DB_THREADS = 2        # Veritabanı thread sayısı (daha düşük)
    
    # MySQL özel ayarları
    MYSQL_TIMEOUT = 60    # MySQL bağlantı timeout
    MYSQL_THREADS = 2     # MySQL thread sayısı
    
    # PostgreSQL özel ayarları
    POSTGRESQL_TIMEOUT = 75   # PostgreSQL bağlantı timeout
    POSTGRESQL_THREADS = 2    # PostgreSQL thread sayısı
    
    # MongoDB özel ayarları
    MONGODB_TIMEOUT = 80      # MongoDB bağlantı timeout
    MONGODB_THREADS = 1       # MongoDB tek thread (daha güvenilir)
    
    # MSSQL özel ayarları
    MSSQL_TIMEOUT = 70        # MSSQL bağlantı timeout
    MSSQL_THREADS = 2         # MSSQL thread sayısı
    
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