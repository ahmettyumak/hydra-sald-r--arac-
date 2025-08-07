from .base import BruteForceBase

class RDPBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=3389):
        super().__init__(hedef_ip, hedef_port, "RDP")
    
    def _hydra_tipi(self):
        return "rdp"
    
    def _komut_olustur(self, kullanici_listesi, sifre_listesi):
        komut = super()._komut_olustur(kullanici_listesi, sifre_listesi)
        komut.insert(-1, "-V")  # RDP için verbose mod
        return komut