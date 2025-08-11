# services/postgresql.py
from .base import BruteForceBase
from config import Ayarlar

class PostgreSQLBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=5432):
        super().__init__(hedef_ip, hedef_port, "PostgreSQL")
        # PostgreSQL için özel ayarlar
        self.thread_sayisi = Ayarlar.POSTGRESQL_THREADS
        self.timeout = Ayarlar.POSTGRESQL_TIMEOUT
        
    def _hydra_tipi(self):
        return "postgres"
        
    def _komut_olustur(self, kullanici_listesi, sifre_listesi):
        komut = super()._komut_olustur(kullanici_listesi, sifre_listesi)
        # PostgreSQL için ek parametreler
        komut.extend(["-W", str(self.timeout)])  # Bağlantı timeout
        komut.extend(["-t", str(self.thread_sayisi)])  # Thread sayısı
        return komut
        
    def _postgresql_baglanti_kontrol(self):
        # PostgreSQL bağlantısını test etmek için basit bir kontrol
        try:
            import psycopg2
            conn = psycopg2.connect(
                host=self.hedef_ip,
                port=self.hedef_port,
                user="postgres",
                password="",
                connect_timeout=5
            )
            conn.close()
            return True
        except Exception:
            # psycopg2 yoksa socket ile basit kontrol
            try:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((self.hedef_ip, self.hedef_port))
                sock.close()
                return result == 0
            except:
                return False