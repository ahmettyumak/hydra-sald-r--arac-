import subprocess
from utils.raporlayici import Raporlayici
from config import Ayarlar

class BruteForceBase:
    VNC_ONLY_PASSWORD = ["vnc", "redis", "snmp", "adam6500", "oracle-listener", "s7-300", "cisco"]
    HTTP_TYPES = ["http-get", "https-get", "http-post-form", "https-post-form"]

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
        # FTP bağlantı kontrolü
        elif self._hydra_tipi() == "ftp":
            pass  # Bağlantı kontrolü kaldırıldı; bazı FTP'ler anonim girişi kapalı tutuyor
        # MySQL bağlantı kontrolü
        elif self._hydra_tipi() == "mysql":
            pass  # Bağlantı kontrolü kaldırıldı
        # PostgreSQL bağlantı kontrolü
        elif self._hydra_tipi() == "postgres":
            pass  # Bağlantı kontrolü kaldırıldı; bazı PG ayarları ilk SYN'e cevap geciktirebilir
        # MongoDB bağlantı kontrolü
        elif self._hydra_tipi() == "mongodb":
            pass  # Bağlantı kontrolü kaldırıldı
        # MSSQL bağlantı kontrolü
        elif self._hydra_tipi() == "mssql":
            pass  # Bağlantı kontrolü kaldırıldı
        # HTTP Basic Auth kontrolü (yanlış pozitifleri azaltmak için)
        hydra_type = self._hydra_tipi()
        if hydra_type in ("http-get", "https-get") and not getattr(self, 'form_params', None):
            # Basic Auth kontrolünü daha esnek yap - sadece uyarı ver, engelleme
            if not self._http_basic_auth_kontrol():
                print("[!] HTTP Basic Auth tespit edilmedi. http-get/https-get deneniyor ama yanlış pozitif olabilir.")
                print("[!] Form tabanlı giriş için -F ile form spesifikasyonu sağlayın.")
                # Kontrolü geç, brute'u dene ama uyarı ver
            else:
                print("[+] HTTP Basic Auth tespit edildi. http-get/https-get güvenli şekilde çalıştırılıyor.")
        komut = self._komut_olustur(kullanici_listesi, sifre_listesi)
        print(f"[*] {self.servis_adi.upper()} saldırısı başlatılıyor...")
        print(f"[*] Hedef: {self.hedef_ip}:{self.hedef_port}")
        try:
            # Büyük wordlistlerde process'in erken kesilmemesi için yüksek timeout
            sonuc = subprocess.run(komut, capture_output=True, text=True, timeout=Ayarlar.HYDRA_TIMEOUT)
            print(f"[*] {self.servis_adi.upper()} sonuçları:")
            print("-" * 50)
            stdout_text = sonuc.stdout or ""
            stderr_text = sonuc.stderr or ""
            if stdout_text:
                print(stdout_text)
            if stderr_text:
                print(f"[!] Hata çıktısı: {stderr_text}")

            import re
            satirlar = stdout_text.splitlines()
            basarili_satirlar = []

            if hydra_type in self.VNC_ONLY_PASSWORD:
                # Yalnızca parola ile doğrulanan modüller (ör. vnc)
                pass_regex = re.compile(r"\bpassword\s*:\s*\S+", re.IGNORECASE)
                basarili_satirlar = [s for s in satirlar if pass_regex.search(s)]
                if not basarili_satirlar and re.search(r"valid (pair|password) found", stdout_text, re.IGNORECASE):
                    # Başarı mesajı var ama tek satır yoksa, status mesajını kaydet
                    basarili_satirlar = ["[INFO] valid password found"]
            else:
                # login ve password aynı satırda olmalı
                lp_regex = re.compile(r"\b(login|user)\s*:\s*\S+.*\bpass(?:word)?\s*:\s*\S+", re.IGNORECASE)
                basarili_satirlar = [s for s in satirlar if lp_regex.search(s)]
                # Bilinen yanlış pozitif mesajlarını hariç tut
                exclude_regex = re.compile(r"might be valid but account not active|continuing attacking the account|can not connect|error|invalid|failed|denied", re.IGNORECASE)
                basarili_satirlar = [s for s in basarili_satirlar if not exclude_regex.search(s)]
                
                # HTTP için ek filtreleme - sadece gerçek başarı satırlarını kabul et
                if hydra_type in ("http-get", "https-get"):
                    # HTTP'de genellikle "login: user password: pass" formatında olur
                    # Ayrıca Hydra'nın özet bilgisini kontrol et
                    if "valid password found" not in stdout_text.lower():
                        basarili_satirlar = []  # Özet yoksa başarı yok

            if basarili_satirlar:
                print(f"\n[+] {self.servis_adi.upper()} için başarılı girişler:")
                for s in basarili_satirlar:
                    print(f"    {s.strip()}")
                    self.raporlayici.rapor_ekle(self.servis_adi, self.hedef_ip, self.hedef_port, "BAŞARILI", s.strip())
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
        # HTTP/HTTPS için path veya form parametreleri
        if hydra_type in ("http-get", "https-get"):
            komut.extend(["-m", getattr(self, 'http_path', "/")])
        elif hydra_type in ("http-post-form", "https-post-form"):
            form_spec = getattr(self, 'form_params', None)
            if not form_spec:
                raise ValueError("HTTP form brute-force için 'form_params' gereklidir (örn: /login:username=^USER^&password=^PASS^:F=Hatalı giriş)")
            komut.append(form_spec)
        # Port
        if hasattr(self, 'port') and self.port:
            komut.extend(["-s", str(self.port)])
        else:
            komut.extend(["-s", str(self.hedef_port)])
        # Thread ve timeout ayarları
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

    def _ftp_baglanti_kontrol(self):
        # FTP bağlantısını test etmek için basit bir kontrol
        try:
            import ftplib
            ftp = ftplib.FTP()
            ftp.connect(self.hedef_ip, self.hedef_port, timeout=5)
            ftp.login("anonymous", "anonymous") # FTP sunucusuna anonim giriş denemesi
            ftp.quit()
            return True
        except Exception:
            return False

    def _mysql_baglanti_kontrol(self):
        # MySQL bağlantısını test etmek için basit bir kontrol
        try:
            import mysql.connector
            conn = mysql.connector.connect(
                host=self.hedef_ip,
                port=self.hedef_port,
                user="root",
                password="",
                connection_timeout=5,
                auth_plugin='mysql_native_password'
            )
            conn.close()
            return True
        except Exception:
            # mysql.connector yoksa socket ile basit kontrol
            try:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((self.hedef_ip, self.hedef_port))
                sock.close()
                return result == 0
            except:
                return False

    def _postgresql_baglanti_kontrol(self):
        # PostgreSQL bağlantısını test etmek için basit bir kontrol
        try:
            import psycopg2
            conn = psycopg2.connect(
                host=self.hedef_ip,
                port=self.hedef_port,
                user="postgres",
                password="",
                connect_timeout=5
            )
            conn.close()
            return True
        except Exception:
            # psycopg2 yoksa socket ile basit kontrol
            try:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((self.hedef_ip, self.hedef_port))
                sock.close()
                return result == 0
            except:
                return False

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

    def _mssql_baglanti_kontrol(self):
        # MSSQL bağlantısını test etmek için basit bir kontrol
        try:
            import pyodbc
            # MSSQL için connection string
            conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.hedef_ip},{self.hedef_port};UID=sa;PWD=;Connection Timeout=5;"
            conn = pyodbc.connect(conn_str)
            conn.close()
            return True
        except Exception:
            # pyodbc yoksa socket ile basit kontrol
            try:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((self.hedef_ip, self.hedef_port))
                sock.close()
                return result == 0
            except:
                return False

    def _http_basic_auth_kontrol(self):
        # Basic Auth gereksinimi var mı? 401 ve WWW-Authenticate başlığı beklenir
        try:
            path = getattr(self, 'http_path', '/') or '/'
            if self._hydra_tipi() == 'https-get':
                from http.client import HTTPSConnection
                conn = HTTPSConnection(self.hedef_ip, self.hedef_port, timeout=5)
            else:
                from http.client import HTTPConnection
                conn = HTTPConnection(self.hedef_ip, self.hedef_port, timeout=5)
            conn.request('HEAD', path)
            resp = conn.getresponse()
            headers = {k.lower(): v for k, v in resp.getheaders()}
            conn.close()
            if resp.status == 401 and 'www-authenticate' in headers:
                return True
            return False
        except Exception:
            # Erişilemiyorsa, hydra zaten başarısız olacaktır; yanlış pozitif üretmemek için False dön
            return False