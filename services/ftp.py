from .base import BruteForceBase
from config import Ayarlar

class FTPBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=21):
        super().__init__(hedef_ip, hedef_port, "FTP")
        # FTP için özel ayarlar
        self.thread_sayisi = Ayarlar.FTP_THREADS
        self.timeout = Ayarlar.FTP_TIMEOUT
        
    def _hydra_tipi(self):
        return "ftp"
        
    def _komut_olustur(self, kullanici_listesi, sifre_listesi):
        komut = super()._komut_olustur(kullanici_listesi, sifre_listesi)
        # FTP için ek parametreler
        komut.extend(["-W", str(self.timeout)])  # Bağlantı timeout
        komut.extend(["-t", str(self.thread_sayisi)])  # Thread sayısı
        return komut