import subprocess
from utils.raporlayici import Raporlayici
from config import Ayarlar

class BruteForceBase:
    VNC_ONLY_PASSWORD = ["vnc", "redis", "snmp", "adam6500", "oracle-listener", "s7-300", "cisco"]
    HTTP_TYPES = ["http-get", "http-post", "https-get", "https-post"]

    def __init__(self, hedef_ip, hedef_port, servis_adi):
        self.hedef_ip = hedef_ip
        self.hedef_port = hedef_port
        self.servis_adi = servis_adi
        self.raporlayici = Raporlayici()
        self.http_path = "/"  # Varsayılan path

    def saldir(self, kullanici_listesi, sifre_listesi):
        # SMTP AUTH kontrolü
        if self._hydra_tipi() == "smtp":
            if not self._smtp_auth_kontrol():
                print("[!] SMTP sunucusunda AUTH desteği yok, brute-force başlatılmadı.")
                self.raporlayici.rapor_ekle(self.servis_adi, self.hedef_ip, self.hedef_port, "HATA", "SMTP AUTH desteklenmiyor")
                return False
        komut = self._komut_olustur(kullanici_listesi, sifre_listesi)
        print(f"[*] {self.servis_adi.upper()} saldırısı başlatılıyor...")
        print(f"[*] Hedef: {self.hedef_ip}:{self.hedef_port}")
        try:
            sonuc = subprocess.run(komut, capture_output=True, text=True, timeout=Ayarlar.HYDRA_TIMEOUT)
            print(f"[*] {self.servis_adi.upper()} sonuçları:")
            print("-" * 50)
            if sonuc.stdout:
                print(sonuc.stdout)
            if sonuc.stderr:
                print(f"[!] Hata çıktısı: {sonuc.stderr}")
            if sonuc.returncode == 0 and "login:" in sonuc.stdout.lower():
                basarili_satirlar = [satir for satir in sonuc.stdout.splitlines() if "login:" in satir.lower()]
                print(f"\n[+] {self.servis_adi.upper()} için başarılı girişler:")
                for satir in basarili_satirlar:
                    print(f"    {satir.strip()}")
                    self.raporlayici.rapor_ekle(self.servis_adi, self.hedef_ip, self.hedef_port, "BAŞARILI", satir.strip())
                print("-" * 50)
                return True
            else:
                print(f"[-] {self.servis_adi.upper()} için başarılı giriş bulunamadı.")
                self.raporlayici.rapor_ekle(self.servis_adi, self.hedef_ip, self.hedef_port, "BAŞARISIZ", "Başarılı giriş bulunamadı")
                print("-" * 50)
                return False
        except subprocess.TimeoutExpired:
            print(f"[!] {self.servis_adi.upper()} zaman aşımı!")
            self.raporlayici.rapor_ekle(self.servis_adi, self.hedef_ip, self.hedef_port, "HATA", "Zaman aşımı")
            return False
        except Exception as e:
            print(f"[!] {self.servis_adi.upper()} hatası: {str(e)}")
            self.raporlayici.rapor_ekle(self.servis_adi, self.hedef_ip, self.hedef_port, "HATA", str(e))
            return False

    def _komut_olustur(self, kullanici_listesi, sifre_listesi):
        komut = ["hydra"]
        hydra_type = self._hydra_tipi()
        # VNC, Redis, SNMP, vb. için sadece şifre
        if hydra_type in self.VNC_ONLY_PASSWORD:
            komut.extend(["-P", sifre_listesi])
        else:
            komut.extend(["-L", kullanici_listesi, "-P", sifre_listesi])
        # Tek kullanıcı/şifre parametreleri
        if hasattr(self, 'tek_kullanici') and self.tek_kullanici:
            komut.extend(["-l", self.tek_kullanici])
        if hasattr(self, 'tek_sifre') and self.tek_sifre:
            komut.extend(["-p", self.tek_sifre])
        komut.append(self.hedef_ip)
        komut.append(hydra_type)
        # HTTP/HTTPS için path
        if hydra_type in self.HTTP_TYPES:
            komut.extend(["-m", getattr(self, 'http_path', "/")])
        # Port
        if hasattr(self, 'port') and self.port:
            komut.extend(["-s", str(self.port)])
        else:
            komut.extend(["-s", str(self.hedef_port)])
        # Thread
        thread_sayisi = getattr(self, 'thread_sayisi', Ayarlar.HYDRA_THREADS)
        komut.extend(["-t", str(thread_sayisi)])
        # Timeout
        timeout = getattr(self, 'timeout', Ayarlar.HYDRA_TIMEOUT)
        if timeout != Ayarlar.HYDRA_TIMEOUT:
            komut.extend(["-W", str(timeout)])
        # Diğer parametreler
        if hasattr(self, 'verbose') and self.verbose:
            komut.append("-V")
        if hasattr(self, 'debug') and self.debug:
            komut.append("-d")
        if hasattr(self, 'first_found') and self.first_found:
            komut.append("-f")
        if hasattr(self, 'restore') and self.restore:
            komut.append("-R")
        if hasattr(self, 'restore_file') and self.restore_file:
            komut.extend(["-R", self.restore_file])
        if hasattr(self, 'output_file') and self.output_file:
            komut.extend(["-o", self.output_file])
        if hasattr(self, 'log_file') and self.log_file:
            komut.extend(["-b", self.log_file])
        if hasattr(self, 'xml_output') and self.xml_output:
            komut.append("-x")
        if hasattr(self, 'form_params') and self.form_params:
            komut.extend(["-F", self.form_params])
        if hasattr(self, 'custom_params') and self.custom_params:
            komut.extend(["-C", self.custom_params])
        if hasattr(self, 'module_path') and self.module_path:
            komut.extend(["-M", self.module_path])
        if hasattr(self, 'service_name') and self.service_name:
            komut.extend(["-m", self.service_name])
        if hasattr(self, 'additional_params') and self.additional_params:
            komut.extend(self.additional_params)
        return komut

    def _hydra_tipi(self):
        return self.servis_adi.lower()

    def _smtp_auth_kontrol(self):
        # Basit kontrol: 25, 587, 465 portlarında AUTH desteği olup olmadığını kontrol et
        # Gerçek SMTP sunucusunda tam kontrol için smtplib ile denenebilir
        import smtplib
        try:
            server = smtplib.SMTP(self.hedef_ip, self.hedef_port, timeout=5)
            server.ehlo()
            if 'auth' in server.esmtp_features:
                server.quit()
                return True
            server.quit()
            return False
        except Exception:
            return False