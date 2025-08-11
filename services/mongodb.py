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
        # MongoDB için ek parametreler
        komut.extend(["-W", str(self.timeout)])  # Bağlantı timeout
        komut.extend(["-t", str(self.thread_sayisi)])  # Thread sayısı
        return komut
        
    def _mongodb_baglanti_kontrol(self):
        # MongoDB bağlantısını test etmek için basit bir kontrol
        try:
            import pymongo
            client = pymongo.MongoClient(
                f"mongodb://{self.hedef_ip}:{self.hedef_port}/",
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000
            )
            client.admin.command('ping')
            client.close()
            return True
        except Exception:
            # pymongo yoksa socket ile basit kontrol
            try:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((self.hedef_ip, self.hedef_port))
                sock.close()
                return result == 0
            except:
                return False