from .base import BruteForceBase

class MySQLBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=3306):
        super().__init__(hedef_ip, hedef_port, "MySQL")
        
    def _hydra_tipi(self):
        return "mysql"
        
    def _komut_olustur(self, kullanici_listesi, sifre_listesi):
        komut = super()._komut_olustur(kullanici_listesi, sifre_listesi)
        # MySQL için ek parametreler (üst sınıf zaten uygular, burada tekrar etmeyelim)
        return komut
        
    # Bağlantı kontrolü üst sınıfta kaldırıldı; burada ek kontrol yok