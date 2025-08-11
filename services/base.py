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
        print(f"[*] {self.servis_adi.upper()} saldırısı başlatılıyor...")
        print(f"[*] Hedef: {self.hedef_ip}:{self.hedef_port}")
        
        try:
            sonuc = subprocess.run(komut, capture_output=True, text=True, timeout=Ayarlar.HYDRA_TIMEOUT)
            
            # Console output
            print(f"[*] {self.servis_adi.upper()} sonuçları:")
            print("-" * 50)
            
            if sonuc.stdout:
                print(sonuc.stdout)
            
            if sonuc.stderr:
                print(f"[!] Hata çıktısı: {sonuc.stderr}")
            
            if sonuc.returncode == 0 and "login:" in sonuc.stdout.lower():
                basarili_satirlar = [satir for satir in sonuc.stdout.splitlines() 
                                    if "login:" in satir.lower()]
                
                print(f"\n[+] {self.servis_adi.upper()} için başarılı girişler:")
                for satir in basarili_satirlar:
                    print(f"    {satir.strip()}")
                    self.raporlayici.rapor_ekle(
                        self.servis_adi, 
                        self.hedef_ip, 
                        self.hedef_port, 
                        "BAŞARILI",
                        satir.strip()
                    )
                print("-" * 50)
                return True
            else:
                print(f"[-] {self.servis_adi.upper()} için başarılı giriş bulunamadı.")
                self.raporlayici.rapor_ekle(
                    self.servis_adi,
                    self.hedef_ip,
                    self.hedef_port,
                    "BAŞARISIZ",
                    "Başarılı giriş bulunamadı"
                )
                print("-" * 50)
                return False
            
        except subprocess.TimeoutExpired:
            print(f"[!] {self.servis_adi.upper()} zaman aşımı!")
            self.raporlayici.rapor_ekle(
                self.servis_adi,
                self.hedef_ip,
                self.hedef_port,
                "HATA",
                "Zaman aşımı"
            )
            return False
        except Exception as e:
            print(f"[!] {self.servis_adi.upper()} hatası: {str(e)}")
            self.raporlayici.rapor_ekle(
                self.servis_adi,
                self.hedef_ip,
                self.hedef_port,
                "HATA",
                str(e)
            )
            return False

    def _komut_olustur(self, kullanici_listesi, sifre_listesi):
        # Temel komut
        komut = ["hydra"]
        
        # Kullanıcı listesi (-L veya -l)
        if hasattr(self, 'kullanici_listesi') and self.kullanici_listesi:
            komut.extend(["-L", self.kullanici_listesi])
        else:
            komut.extend(["-L", kullanici_listesi])
        
        # Şifre listesi (-P veya -p)
        if hasattr(self, 'sifre_listesi') and self.sifre_listesi:
            komut.extend(["-P", self.sifre_listesi])
        else:
            komut.extend(["-P", sifre_listesi])
        
        # Tek kullanıcı (-l)
        if hasattr(self, 'tek_kullanici') and self.tek_kullanici:
            komut.extend(["-l", self.tek_kullanici])
        
        # Tek şifre (-p)
        if hasattr(self, 'tek_sifre') and self.tek_sifre:
            komut.extend(["-p", self.tek_sifre])
        
        # Hedef
        komut.append(self.hedef_ip)
        komut.append(self._hydra_tipi())
        
        # Port (-s)
        if hasattr(self, 'port') and self.port:
            komut.extend(["-s", str(self.port)])
        else:
            komut.extend(["-s", str(self.hedef_port)])
        
        # Thread sayısı (-t)
        thread_sayisi = getattr(self, 'thread_sayisi', Ayarlar.HYDRA_THREADS)
        komut.extend(["-t", str(thread_sayisi)])
        
        # Timeout (-W)
        timeout = getattr(self, 'timeout', Ayarlar.HYDRA_TIMEOUT)
        if timeout != Ayarlar.HYDRA_TIMEOUT:
            komut.extend(["-W", str(timeout)])
        
        # Verbose (-V)
        if hasattr(self, 'verbose') and self.verbose:
            komut.append("-V")
        
        # Debug (-d)
        if hasattr(self, 'debug') and self.debug:
            komut.append("-d")
        
        # First found (-f)
        if hasattr(self, 'first_found') and self.first_found:
            komut.append("-f")
        
        # Restore (-R)
        if hasattr(self, 'restore') and self.restore:
            komut.append("-R")
        
        # Restore file (-R dosya)
        if hasattr(self, 'restore_file') and self.restore_file:
            komut.extend(["-R", self.restore_file])
        
        # Output file (-o)
        if hasattr(self, 'output_file') and self.output_file:
            komut.extend(["-o", self.output_file])
        
        # Log file (-b)
        if hasattr(self, 'log_file') and self.log_file:
            komut.extend(["-b", self.log_file])
        
        # XML output (-x)
        if hasattr(self, 'xml_output') and self.xml_output:
            komut.append("-x")
        
        # Form parameters (-F)
        if hasattr(self, 'form_params') and self.form_params:
            komut.extend(["-F", self.form_params])
        
        # Custom parameters (-C)
        if hasattr(self, 'custom_params') and self.custom_params:
            komut.extend(["-C", self.custom_params])
        
        # Module path (-M)
        if hasattr(self, 'module_path') and self.module_path:
            komut.extend(["-M", self.module_path])
        
        # Service name (-m)
        if hasattr(self, 'service_name') and self.service_name:
            komut.extend(["-m", self.service_name])
        
        # Additional parameters (özel parametreler)
        if hasattr(self, 'additional_params') and self.additional_params:
            komut.extend(self.additional_params)
        
        return komut

    def _hydra_tipi(self):
        return self.servis_adi.lower()