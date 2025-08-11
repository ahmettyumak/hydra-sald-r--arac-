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
        # PostgreSQL için ek parametreler (üst sınıf zaten uygular)
        return komut
        
    # Bağlantı kontrolü üst sınıfta kaldırıldı; burada ek kontrol yok