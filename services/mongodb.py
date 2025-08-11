from .base import BruteForceBase
from config import Ayarlar

class MongoDBBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=27017):
        super().__init__(hedef_ip, hedef_port, "MongoDB")
        # MongoDB için özel ayarlar
        self.thread_sayisi = Ayarlar.MONGODB_THREADS
        self.timeout = Ayarlar.MONGODB_TIMEOUT
        
    def _hydra_tipi(self):
        return "mongodb"
        
    def _komut_olustur(self, kullanici_listesi, sifre_listesi):
        komut = super()._komut_olustur(kullanici_listesi, sifre_listesi)
        # MongoDB için ek parametreler (üst sınıf zaten uygular)
        return komut
        
    # Bağlantı kontrolü üst sınıfta kaldırıldı; burada ek kontrol yok