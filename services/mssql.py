from .base import BruteForceBase
from config import Ayarlar

class MSSQLBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=1433):
        super().__init__(hedef_ip, hedef_port, "MSSQL")
        # MSSQL için özel ayarlar
        self.thread_sayisi = Ayarlar.MSSQL_THREADS
        self.timeout = Ayarlar.MSSQL_TIMEOUT
        
    def _hydra_tipi(self):
        return "mssql"
        
    def _komut_olustur(self, kullanici_listesi, sifre_listesi):
        komut = super()._komut_olustur(kullanici_listesi, sifre_listesi)
        # MSSQL için ek parametreler (üst sınıf zaten uygular)
        return komut
        
    # Bağlantı kontrolü üst sınıfta kaldırıldı; burada ek kontrol yok