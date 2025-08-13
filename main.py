#!/usr/bin/env python3
import os
import socket
import sys
import shlex
from services.scanner import NmapTarayici
from services.port_checker import PortChecker
from services.ftp import FTPBruteForce
from services.ssh import SSHBruteForce
from services.http import HTTPBruteForce
from services.https import HTTPSBruteForce
from services.mysql import MySQLBruteForce
from services.postgresql import PostgreSQLBruteForce
from services.smtp import SMTPBruteForce
from services.pop3 import POP3BruteForce
from services.imap import IMAPBruteForce
from services.rdp import RDPBruteForce
from services.smb import SMBBruteForce
from services.telnet import TelnetBruteForce
from services.vnc import VNCBruteForce
from services.mssql import MSSQLBruteForce
from services.mongodb import MongoDBBruteForce
from utils.raporlayici import Raporlayici
from config import Ayarlar

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'

def giris_ekrani():
    print("=" * 60)
    print("GELİŞMİŞ BRUTE-FORCE SALDIRI ARACI".center(60))
    print("=" * 60)
    print(f"Versiyon: 4.0 | Parametrik Giriş | Port Check | Console Output\n")
    print("💡 İpucu: Yardım için --help yazabilirsiniz!")
    print("💡 Söz dizimi: [parametreler] <host>")
    print("💡 Örnekler:")
    print("   -h 192.168.1.1                    (tüm servislere saldırı)")
    print("   -s ssh -t 8 192.168.1.1           (SSH, 8 thread)")
    print("   -s ftp -L users.txt -P pass.txt 192.168.1.1")
    print("   -s http -V -f 192.168.1.1         (HTTP, verbose, first found)")
    print("   -s ssh -l admin -p pass 192.168.1.1")
    print("   -n 192.168.1.1                     (nmap taraması)")
    print("=" * 60)


def yazdir_yardim():
    print("\n" + "="*70)
    print("HYDRA SALDIRI ARACI - KULLANIM YARDIMI".center(70))
    print("="*70)
    
    print("\n📋 SÖZ DİZİMİ:")
    print("  [OPTIONS] target service")
    print("  [OPTIONS] -M targets.txt service")
    
    print("\n🚀 TEMEL KULLANIM:")
    print("  -h <target>                    # Tüm desteklenen servislere saldır")
    print("  -nmap <target>                 # Nmap taraması")
    print("  [OPTIONS] <target> <service>   # Belirli servise saldır")
    
    print("\n💡 ÖRNEKLER:")
    print("  -h 192.168.1.1")
    print("  -nmap 192.168.1.1")
    print("  -L users.txt -P pass.txt 192.168.1.1 ssh")
    print("  -t 8 -V 192.168.1.1 ftp")
    print("  -s 2222 192.168.1.1 ssh")
    print("  -L logins.txt -P pws.txt -M targets.txt ssh")
    
    print("\n⚙️  ANA PARAMETRELER:")
    print("  -h <target>     # Tüm desteklenen servislere saldır (port check ile)")
    print("  -nmap <target>  # Nmap ile detaylı tarama")
    print("  -M <file>       # Çoklu hedef dosyası (her satırda bir hedef)")
    print("  -s <port>       # Özel port numarası belirt (opsiyonel)")
    
    print("\n🔧 HYDRA PARAMETRELERİ:")
    print("  -L <file>       # Kullanıcı listesi dosyası")
    print("  -P <file>       # Şifre listesi dosyası")
    print("  -l <user>       # Tek kullanıcı")
    print("  -p <pass>       # Tek şifre")
    print("  -t <number>     # Thread sayısı")
    print("  -W <seconds>    # Timeout")
    print("  -V              # Verbose mod")
    print("  -d              # Debug mod")
    print("  -f              # İlk bulunanı durdur")
    print("  -R              # Restore session")
    print("  -o <file>       # Çıktı dosyası")
    print("  -b <file>       # Log dosyası")
    print("  -x              # XML çıktı")
    print("  -F <params>     # Form parametreleri (HTTP için)")
    print("  -C <file>       # Özel parametre dosyası")
    
    print("\n🌐 DESTEKLENEN SERVİSLER:")
    print("  FTP, SSH, HTTP, HTTPS, MySQL, PostgreSQL, MongoDB")
    print("  SMTP, POP3, IMAP, RDP, SMB, Telnet, VNC, MSSQL")
    
    print("\n📝 NOTLAR:")
    print("  • Hydra söz dizimi: [OPTIONS] target service")
    print("  • Çoklu hedef: -M targets.txt service")
    print("  • Port belirtimi: -s parametresi ile (örn: -s 2222)")
    print("  • -h modu: Açık servisler listelenir ve saldırı başlatılır")
    print("  • Belirli servis verildiğinde port check yapılmaz")
    print("  • Target: IP adresi, hostname veya ağ aralığı")
    
    print("\n📚 DOSYA FORMATLARI:")
    print("  • targets.txt: Her satırda bir hedef (IP, hostname)")
    print("  • users.txt: Her satırda bir kullanıcı adı")
    print("  • passwords.txt: Her satırda bir şifre")
    
    print("="*70)

def gecerli_ip_girisi(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def parametrik_giris_kontrol(giris):
    """Parametrik girişleri kontrol eder ve işler"""
    giris = giris.strip()
    
    # Yardım parametresi
    if giris.lower() in ['--help', 'help', 'yardım', '-?', '?']:
        print("\n" + "="*60)
        print("PARAMETRİK GİRİŞ YARDIMI".center(60))
        print("="*60)
        print("Kullanım örnekleri:")
        print("  IP Adresi: 192.168.1.1")
        print("  IP Aralığı: 192.168.1.1-10")
        print("  CIDR Notasyonu: 192.168.1.0/24")
        print("  Hostname: example.com")
        print("\nParametrik Kullanım:")
        print("  -h: Tüm servislere saldırı")
        print("  -s [servis]: Belirli servis (örn: -s ssh)")
        print("  -n: Nmap taraması")
        print("\nHydra Parametreleri:")
        print("  -L [dosya]: Kullanıcı listesi dosyası")
        print("  -P [dosya]: Şifre listesi dosyası")
        print("  -l [kullanıcı]: Tek kullanıcı")
        print("  -p [şifre]: Tek şifre")
        print("  -t [sayı]: Thread sayısı")
        print("  -W [saniye]: Timeout")
        print("  -s [port]: Port numarası")
        print("  -V: Verbose mod")
        print("  -d: Debug mod")
        print("  -f: İlk bulunanı durdur")
        print("  -R: Restore session")
        print("  -o [dosya]: Çıktı dosyası")
        print("  -b [dosya]: Log dosyası")
        print("  -x: XML çıktı")
        print("  -F [parametreler]: Form parametreleri (HTTP için)")
        print("  -C [dosya]: Özel parametre dosyası")
        print("  -M [dosya]: Modül dosyası")
        print("  -m [servis]: Servis adı")
        print("\nKullanım:")
        print("  Sadece IP ve parametreleri yazın:")
        print("  192.168.1.1 -h")
        print("  192.168.1.1 -s ssh")
        print("  192.168.1.1 -n")
        print("  Yardım: -h, --help, help, yardım")
        print("  Çıkış: exit, quit, çıkış")
        print("="*60)
        return None
    
    # Çıkış parametresi
    if giris.lower() in ['exit', 'quit', 'çıkış', 'q']:
        print("[!] Program sonlandırılıyor...")
        exit(0)
    
    # IP aralığı kontrolü (örn: 192.168.1.1-10)
    if '-' in giris and giris.count('.') == 3:
        try:
            base_ip, range_part = giris.rsplit('.', 1)
            start, end = range_part.split('-')
            base_ip = f"{base_ip}.{start}"
            if gecerli_ip_girisi(base_ip):
                return giris  # IP aralığı geçerli
        except:
            pass
    
    # CIDR notasyonu kontrolü (örn: 192.168.1.0/24)
    if '/' in giris:
        try:
            ip_part, cidr = giris.split('/')
            if gecerli_ip_girisi(ip_part) and 0 <= int(cidr) <= 32:
                return giris  # CIDR geçerli
        except:
            pass
    
    # Tek IP kontrolü
    if gecerli_ip_girisi(giris):
        return giris
    
    # Hostname kontrolü (basit)
    if '.' in giris and not giris.startswith('-'):
        return giris  # Hostname olarak kabul et
    
    return None

def hedef_ip_al():
    while True:
        giris = input("Hedef IP ve parametreleri girin (örn:-h 192.168.1.1): ").strip()
        
        # Birleşik giriş desteği: "192.168.1.1 -h" gibi
        if ' ' in giris:
            try:
                tokens = shlex.split(giris)
            except Exception:
                tokens = giris.split()
            if len(tokens) >= 2:
                hedef, parametreler = tokens[0], tokens[1:]
                # Hedef geçerli mi?
                if parametrik_giris_kontrol(hedef):
                    return (hedef, parametreler)
                else:
                    print("[!] Geçersiz hedef formatı. Örnek: 192.168.1.1, 192.168.1.0/24, example.com")
                    continue
        
        # Parametrik kontrol
        sonuc = parametrik_giris_kontrol(giris)
        if sonuc is None:
            continue  # Yardım gösterildi, tekrar sor
        elif sonuc:
            return sonuc
        
        print("[!] Geçersiz format! Örnekler:")
        print("  - IP: 192.168.1.1")
        print("  - IP + Parametre: 192.168.1.1 -h")
        print("  - IP + Servis: 192.168.1.1 -s ssh")
        print("  - Aralık: 192.168.1.1-10")
        print("  - CIDR: 192.168.1.0/24")
        print("  - Hostname: example.com")
        print("  - Yardım: -h")

def port_check_ve_saldiri(hedef_ip, raporlayici):
    """Port check ile açık portları bulup saldırı yapar"""
    print(f"\n[+] {hedef_ip} için port check başlatılıyor...")
    
    port_checker = PortChecker(hedef_ip)
    acik_portlar = port_checker.servis_portlarini_tara()
    acik_servisler = port_checker.acik_servisleri_getir()
    
    if not acik_servisler:
        print("[-] Açık servis bulunamadı!")
        return
    
    print(f"\n[+] Bulunan açık servisler:")
    for servis, port in acik_servisler.items():
        print(f"  - {servis.upper()} (Port {port})")
    
    # Servis sınıfları eşleme
    servis_esleme = {
        'ftp': FTPBruteForce,
        'ssh': SSHBruteForce,
        'http': HTTPBruteForce,
        'https': HTTPSBruteForce,
        'mysql': MySQLBruteForce,
        'postgresql': PostgreSQLBruteForce,
        'mongodb': MongoDBBruteForce,
        'smtp': SMTPBruteForce,
        'pop3': POP3BruteForce,
        'imap': IMAPBruteForce,
        'rdp': RDPBruteForce,
        'smb': SMBBruteForce,
        'telnet': TelnetBruteForce,
        'vnc': VNCBruteForce,
        'mssql': MSSQLBruteForce
    }
    
    print(f"\n[+] Brute force saldırıları başlatılıyor...")
    for servis_adi, port in acik_servisler.items():
        if servis_adi in servis_esleme:
            try:
                saldiri = servis_esleme[servis_adi](hedef_ip, port)
                saldiri.saldir(Ayarlar.KULLANICI_ADI_LISTESI, Ayarlar.PAROLA_LISTESI)
            except Exception as e:
                print(f"[!] {servis_adi.upper()} hatası: {str(e)}")
                continue

def nmap_tarama_ve_saldiri(hedef_ip, raporlayici):
    """Nmap ile detaylı tarama ve saldırı"""
    try:
        print(f"\n[+] {hedef_ip} için Nmap taraması başlatılıyor...")
        
        tarayici = NmapTarayici(hedef_ip)
        acik_servisler = tarayici.detayli_tarama()
        
        if not acik_servisler:
            print("[-] Açık port bulunamadı")
            return
        
        print(f"\n[+] Bulunan Servisler:")
        for servis in acik_servisler:
            host = servis.get('host', hedef_ip)
            print(f"  - {host}:{servis['port']}/{servis['protokol']}: {servis['servis']} ({servis['versiyon']})")
        
        servis_esleme = {
            'ftp': FTPBruteForce,
            'ssh': SSHBruteForce,
            'http': HTTPBruteForce,
            'https': HTTPSBruteForce,
            'mysql': MySQLBruteForce,
            'postgresql': PostgreSQLBruteForce,
            'mongodb': MongoDBBruteForce,
            'smtp': SMTPBruteForce,
            'pop3': POP3BruteForce,
            'imap': IMAPBruteForce,
            'rdp': RDPBruteForce,
            'smb': SMBBruteForce,
            'telnet': TelnetBruteForce,
            'vnc': VNCBruteForce,
            'mssql': MSSQLBruteForce
        }
        
        print(f"\n[+] Brute force saldırıları başlatılıyor...")
        for servis in acik_servisler:
            servis_adi = servis['servis']
            host = servis.get('host', hedef_ip)
            if servis_adi in servis_esleme:
                try:
                    saldiri = servis_esleme[servis_adi](host, servis['port'])
                    saldiri.saldir(Ayarlar.KULLANICI_ADI_LISTESI, Ayarlar.PAROLA_LISTESI)
                except Exception as e:
                    print(f"[!] {servis_adi.upper()} hatası: {str(e)}")
                    continue
    except Exception as e:
        print(f"[!] Nmap tarama hatası: {str(e)}")
        raporlayici.rapor_ekle("NMAP", hedef_ip, "N/A", "HATA", str(e))

def tum_servislere_saldiri(hedef_ip, raporlayici):
    """Tüm desteklenen servislere saldırı"""
    print(f"\n[+] {hedef_ip} için tüm servislere saldırı başlatılıyor...")
    
    servis_esleme = {
        'ftp': FTPBruteForce,
        'ssh': SSHBruteForce,
        'http': HTTPBruteForce,
        'https': HTTPSBruteForce,
        'mysql': MySQLBruteForce,
        'postgresql': PostgreSQLBruteForce,
        'mongodb': MongoDBBruteForce,
        'smtp': SMTPBruteForce,
        'pop3': POP3BruteForce,
        'imap': IMAPBruteForce,
        'rdp': RDPBruteForce,
        'smb': SMBBruteForce,
        'telnet': TelnetBruteForce,
        'vnc': VNCBruteForce,
        'mssql': MSSQLBruteForce
    }
    
    # Her servis için port check yap
    acik_servisler = {}
    for servis_adi, port in Ayarlar.PORTLAR.items():
        if servis_adi in servis_esleme:
            print(f"[*] {servis_adi.upper()} port {port} kontrol ediliyor...")
            
            # Port check yap
            try:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                result = sock.connect_ex((hedef_ip, port))
                sock.close()
                
                if result == 0:
                    print(f"[+] {servis_adi.upper()} port {port} açık")
                    acik_servisler[servis_adi] = port
                else:
                    print(f"[-] {servis_adi.upper()} port {port} kapalı - atlanıyor")
            except Exception as e:
                print(f"[!] {servis_adi.upper()} port {port} kontrol hatası: {str(e)}")
                continue
    
    if not acik_servisler:
        print("[-] Hiçbir servis portu açık değil!")
        return
    
    print(f"\n[+] Açık servisler: {', '.join(acik_servisler.keys()).upper()}")
    
    # Saldırıları başlat
    for servis_adi, port in acik_servisler.items():
        try:
            print(f"\n[+] {servis_adi.upper()} servisi deneniyor...")
            saldiri = servis_esleme[servis_adi](hedef_ip, port)
            saldiri.saldir(Ayarlar.KULLANICI_ADI_LISTESI, Ayarlar.PAROLA_LISTESI)
        except Exception as e:
            print(f"[!] {servis_adi.upper()} hatası: {str(e)}")
            continue

def belirli_servise_saldiri(hedef_ip, servis_adi, raporlayici):
    """Belirli bir servise saldırı"""
    if servis_adi not in Ayarlar.PORTLAR:
        print(f"[!] {servis_adi} servisi desteklenmiyor!")
        return
    
    port = Ayarlar.PORTLAR[servis_adi]
    print(f"[*] {servis_adi.upper()} port {port} kontrol ediliyor...")
    
    # Port check yap
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((hedef_ip, port))
        sock.close()
        
        if result == 0:
            print(f"[+] {servis_adi.upper()} port {port} açık")
        else:
            print(f"[-] {servis_adi.upper()} port {port} kapalı - saldırı yapılamıyor")
            return
    except Exception as e:
        print(f"[!] {servis_adi.upper()} port {port} kontrol hatası: {str(e)}")
        return
    
    servis_esleme = {
        'ftp': FTPBruteForce,
        'ssh': SSHBruteForce,
        'http': HTTPBruteForce,
        'https': HTTPSBruteForce,
        'mysql': MySQLBruteForce,
        'postgresql': PostgreSQLBruteForce,
        'mongodb': MongoDBBruteForce,
        'smtp': SMTPBruteForce,
        'pop3': POP3BruteForce,
        'imap': IMAPBruteForce,
        'rdp': RDPBruteForce,
        'smb': SMBBruteForce,
        'telnet': TelnetBruteForce,
        'vnc': VNCBruteForce,
        'mssql': MSSQLBruteForce
    }
    
    if servis_adi in servis_esleme:
        try:
            print(f"[+] {servis_adi.upper()} saldırısı başlatılıyor...")
            saldiri = servis_esleme[servis_adi](hedef_ip, port)
            saldiri.saldir(Ayarlar.KULLANICI_ADI_LISTESI, Ayarlar.PAROLA_LISTESI)
        except Exception as e:
            print(f"[!] {servis_adi.upper()} hatası: {str(e)}")

def parametrik_komut_isle(hedef_ip, parametreler, servis_arg=None):
    print(f"[+] Hedef: {hedef_ip}")
    if parametreler:
        print(f"[+] Parametreler: {' '.join(parametreler)}")
    if servis_arg:
        print(f"[+] Belirtilen Servis: {servis_arg.upper()}")

    servisler = []
    hydra_parametreleri = {}
    nmap_yapilacak = False
    servisler_explicit = False  # Servis belirtildi mi?
    tum_servisler = False       # -h ile tüm servisler mi istendi?
    custom_port = None          # -s ile özel port belirtildi mi?

    i = 0
    while i < len(parametreler):
        param = parametreler[i]

        # Port belirtimi (-s) - OPSİYONEL
        if param == "-s" and i + 1 < len(parametreler):
            port_value = parametreler[i + 1]
            
            # Sayısal değer ise port olarak kabul et
            if port_value.isdigit():
                custom_port = int(port_value)
                print(f"[+] Özel port belirtildi: {custom_port}")
                i += 2
            else:
                print(f"[!] -s sonrası port numarası bekleniyor: {port_value}")
                i += 2
            
        # Tüm servisler (-h)
        elif param == "-h":
            tum_servisler = True
            servisler = list(Ayarlar.PORTLAR.keys())
            i += 1

        # Nmap taraması (-nmap)
        elif param == "-nmap":
            nmap_yapilacak = True
            print(f"[+] Nmap taraması başlatılıyor...")
            raporlayici = Raporlayici()
            nmap_tarama_ve_saldiri(hedef_ip, raporlayici)
            return
        
        # Servis belirtimi (pozisyonel parametre olarak)
        elif not param.startswith('-') and param.lower() in Ayarlar.PORTLAR:
            servisler.append(param.lower())
            servisler_explicit = True
            i += 1
            
        # Hydra parametreleri
        elif param in ["-L", "-P", "-l", "-p", "-t", "-W", "-o", "-b", "-R", "-F", "-C", "-M", "-m"]:
            if param in ["-L", "-P", "-l", "-p", "-t", "-W", "-o", "-b", "-F", "-C", "-M", "-m"]: # Değer alan parametreler
                if i + 1 < len(parametreler):
                    hydra_parametreleri[param] = parametreler[i + 1]
                    i += 2
                else:
                    print(f"[!] Hata: {param} parametresi için değer eksik.")
                    i += 1 # Hatalı parametreyi atla
            else: # Değer almayan parametreler (-R)
                hydra_parametreleri[param] = True
                i += 1
        else:
            print(f"[!] Bilinmeyen veya geçersiz parametre atlanıyor: {param}")
            i += 1

    # Eğer servisler listesi boşsa ve -h veya -nmap de yoksa, parametreler listesinin ilk elemanını servis olarak dene
    if not servisler and not tum_servisler and not nmap_yapilacak and parametreler and parametreler[0].lower() in Ayarlar.PORTLAR:
        servisler.append(parametreler[0].lower())
        servisler_explicit = True

    # Eğer ne -h ne de servis belirtilmişse ve nmap de istenmiyorsa, port check yap
    if not servisler and not nmap_yapilacak and not tum_servisler:
        print(f"[+] Port check ile servis tespiti yapılıyor...")
        port_checker = PortChecker(hedef_ip)
        acik_portlar = port_checker.servis_portlarini_tara()
        acik_servisler = port_checker.acik_servisleri_getir()
        servisler = list(acik_servisler.keys())
        
        if not servisler:
            print("[-] Açık servis bulunamadı!")
            return
    
    # Eğer -h ile tüm servisler istendiyse, desteklenen tüm servisleri listele
    if tum_servisler:
        print(f"\n[*] Uygulama tarafından desteklenen toplam {len(Ayarlar.PORTLAR)} servis:")
        for s_name, s_port in Ayarlar.PORTLAR.items():
            print(f"    - {s_name.upper()} (Port {s_port})")
        print("-" * 50)

    if not servisler:
        print(f"[!] Saldırılacak servis bulunamadı. Lütfen target service formatında belirtin veya -h kullanın.")
        return

    print(f"[+] Saldırılacak servisler: {', '.join(servisler).upper()}")
    
    # Her servis için port check yap (Nmap modu hariç ve servis açıkça belirtilmediyse)
    acik_servisler = {}
    if not nmap_yapilacak and not servisler_explicit:
        for servis_adi in servisler:
            port = Ayarlar.PORTLAR.get(servis_adi) # Varsayılan port
            if custom_port is not None: # Eğer özel port belirtildiyse onu kullan
                port = custom_port
            
            if port is None: # Eğer servis adı bilinmiyorsa ve özel port da yoksa atla
                print(f"[!] {servis_adi.upper()} için varsayılan port bulunamadı ve özel port belirtilmedi. Atlanıyor.")
                continue
            
            print(f"[*] {servis_adi.upper()} port {port} kontrol ediliyor...")
            
            try:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(Ayarlar.PORT_CHECK_TIMEOUT)
                result = sock.connect_ex((hedef_ip, port))
                sock.close()
                
                if result == 0:
                    print(f"[+] {servis_adi.upper()} port {port} açık")
                    acik_servisler[servis_adi] = port
                else:
                    print(f"[-] {servis_adi.upper()} port {port} kapalı - atlanıyor")
            except Exception as e:
                print(f"[!] {servis_adi.upper()} port {port} kontrol hatası: {str(e)}")
                continue
    elif servisler_explicit: # Servis açıkça belirtildiyse (target service ile), port check yapma, doğrudan servis listesi ile devam et
        for servis_adi in servisler:
            # Özel port belirtildiyse onu kullan, yoksa varsayılan port
            if custom_port is not None:
                acik_servisler[servis_adi] = custom_port
            else:
                acik_servisler[servis_adi] = Ayarlar.PORTLAR[servis_adi]
    else: # Nmap yapılıyorsa, acik_servisler boş kalır, nmap_tarama_ve_saldiri zaten kendi içinde servisleri bulur
        pass

    if not acik_servisler and not nmap_yapilacak:
        print("[-] Hiçbir servis portu açık değil veya saldırı için uygun servis bulunamadı!")
        return
    
    if acik_servisler:
        print(f"\n[+] Brute-force yapılacak açık servisler ({len(acik_servisler)} adet):")
        for s_name, s_port in acik_servisler.items():
            print(f"    - {s_name.upper()} (Port {s_port})")
        print("-" * 50)

    # Servis sınıfları eşleme
    servis_esleme = {
        'ftp': FTPBruteForce, 'ssh': SSHBruteForce, 'http': HTTPBruteForce, 'https': HTTPSBruteForce,
        'mysql': MySQLBruteForce, 'postgresql': PostgreSQLBruteForce, 'mongodb': MongoDBBruteForce,
        'smtp': SMTPBruteForce, 'pop3': POP3BruteForce, 'imap': IMAPBruteForce, 'rdp': RDPBruteForce,
        'smb': SMBBruteForce, 'telnet': TelnetBruteForce, 'vnc': VNCBruteForce, 'mssql': MSSQLBruteForce
    }
    
    # Varsayılan değerler
    kullanici_listesi = hydra_parametreleri.get('-L', Ayarlar.KULLANICI_ADI_LISTESI)
    sifre_listesi = hydra_parametreleri.get('-P', Ayarlar.PAROLA_LISTESI)
    
    # Saldırıları başlat
    raporlayici = Raporlayici()
    for servis_adi, port in acik_servisler.items():
        if servis_adi in servis_esleme:
            try:
                print(f"\n[+] {servis_adi.upper()} saldırısı başlatılıyor...")
                saldiri = servis_esleme[servis_adi](hedef_ip, port)
                
                # Hydra parametrelerini uygula
                for param, value in hydra_parametreleri.items():
                    if param == '-t': saldiri.thread_sayisi = int(value)
                    elif param == '-W': saldiri.timeout = int(value)
                    elif param == '-L': saldiri.kullanici_listesi = value
                    elif param == '-P': saldiri.sifre_listesi = value
                    elif param == '-l': saldiri.tek_kullanici = value
                    elif param == '-p': saldiri.tek_sifre = value
                    elif param == '-s': saldiri.port = int(value)
                    elif param == '-V': saldiri.verbose = True
                    elif param == '-d': saldiri.debug = True
                    elif param == '-f': saldiri.first_found = True
                    elif param == '-R': saldiri.restore = True
                    elif param == '-o': saldiri.output_file = value
                    elif param == '-b': saldiri.log_file = value
                    elif param == '-x': saldiri.xml_output = True
                    elif param == '-F': saldiri.form_params = value
                    elif param == '-C': saldiri.custom_params = value
                    elif param == '-M': saldiri.module_path = value
                    elif param == '-m': saldiri.service_name = value
                
                saldiri.saldir(kullanici_listesi, sifre_listesi)
            except Exception as e:
                print(f"[!] {servis_adi.upper()} hatası: {str(e)}")
                continue


def main():
    # Dizinleri oluştur
    for dir in ["wordlists", "reports", "sonuclar"]:
        os.makedirs(dir, exist_ok=True)
    
    # Argüman yoksa örnekleri göster
    if len(sys.argv) == 1:
        print("Örnekler: ")
        print("  -L wordlists/users.txt -P wordlists/pass.txt 192.168.9.131 ssh")
        print("  -t 8 -V 192.168.1.1 ftp")
        print("  -h 192.168.1.1")
        print("  -nmap 192.168.1.1")
        print("  -s 2222 192.168.1.1 ssh")
        print("  -L logins.txt -P pws.txt -M targets.txt ssh")
        print("Yardım: --help")
        return
    
    # Yardım bayrakları
    if any(arg in ("--help", "-?", "help") for arg in sys.argv[1:]):
        yazdir_yardim()
        return
    
    tokens = sys.argv[1:]

    # Bayraklardan sonra değer bekleyen parametreler
    flags_with_values = {"-s", "-L", "-P", "-l", "-p", "-t", "-W", "-o", "-b", "-F", "-C", "-M", "-m"}

    # Tüm tokenları tarayarak hangi indekslerin değer olarak tüketildiğini işaretle
    consumed_value_indexes = set()
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok in flags_with_values and (i + 1) < len(tokens):
            consumed_value_indexes.add(i + 1)
            i += 2
        else:
            i += 1

    # Pozisyonel tokenlar: '-' ile başlamayan ve değer olarak tüketilmemişler
    positional = [idx for idx, tok in enumerate(tokens) if not tok.startswith('-') and idx not in consumed_value_indexes]

    # -M parametresi kontrolü (çoklu hedef dosyası)
    if '-M' in tokens:
        # -M targets.txt ssh formatı
        if len(positional) < 1:
            print("[!] Eksik parametre. Kullanım: -M targets.txt service")
            print("Örnek: -L logins.txt -P pws.txt -M targets.txt ssh")
            return
        
        service = tokens[positional[-1]].lower()
        targets_file = None
        
        # -M parametresinin değerini bul
        for i, token in enumerate(tokens):
            if token == '-M' and i + 1 < len(tokens):
                targets_file = tokens[i + 1]
                break
        
        if not targets_file:
            print("[!] -M parametresi için dosya belirtilmedi")
            return
        
        # Hedefleri dosyadan oku
        try:
            with open(targets_file, 'r') as f:
                targets = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"[!] Hedef dosyası bulunamadı: {targets_file}")
            return
        except Exception as e:
            print(f"[!] Hedef dosyası okuma hatası: {str(e)}")
            return
        
        if not targets:
            print(f"[!] Hedef dosyası boş: {targets_file}")
            return
        
        print(f"[+] {len(targets)} hedef bulundu: {targets_file}")
        
        # Her hedef için saldırı başlat
        option_tokens = [tok for idx, tok in enumerate(tokens) if idx not in positional and tok != '-M' and idx not in consumed_value_indexes]
        parametreler = [service] + option_tokens
        
        for target in targets:
            print(f"\n{'='*50}")
            print(f"[+] Hedef: {target}")
            print(f"{'='*50}")
            parametrik_komut_isle(target, parametreler)
        
        return

    # -h veya -nmap modu kontrolü (önce yapılmalı)
    if '-h' in tokens:
        if len(positional) < 1:
            print("[!] Eksik parametre. Kullanım: -h target")
            print("Örnek: -h 192.168.1.1")
            return
        target = tokens[positional[0]]
        parametrik_komut_isle(target, ['-h'])
        return

    if '-nmap' in tokens:
        if len(positional) < 1:
            print("[!] Eksik parametre. Kullanım: -nmap target")
            print("Örnek: -nmap 192.168.1.1")
            return
        target = tokens[positional[0]]
        parametrik_komut_isle(target, ['-nmap'])
        return

    # Hydra söz dizimi: [OPTIONS] target service
    # En az 2 pozisyonel token gerekli: target ve service
    if len(positional) < 2:
        print("[!] Eksik parametre. Kullanım: [OPTIONS] target service")
        print("Örnek: -L users.txt -P pass.txt 192.168.1.1 ssh")
        print("       -t 8 -V 192.168.1.1 ftp")
        print("       -s 2222 192.168.1.1 ssh")
        print("       -L logins.txt -P pws.txt -M targets.txt ssh")
        print("       -h 192.168.1.1")
        print("       -nmap 192.168.1.1")
        return

    # Pozisyonel tokenlar: target ve service
    target = tokens[positional[0]]
    service = tokens[positional[1]].lower()

    # Belirli servis modu: [OPTIONS] target service
    # Tüm bayrakları topla (target ve service hariç)
    option_tokens = [tok for idx, tok in enumerate(tokens) if idx not in positional]
    
    # Servis adını pozisyonel parametre olarak ekle
    parametreler = [service] + option_tokens
    parametrik_komut_isle(target, parametreler)

if __name__ == "__main__":
    main()