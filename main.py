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

def giris_ekrani():
    print("=" * 60)
    print("GELİŞMİŞ BRUTE-FORCE SALDIRI ARACI".center(60))
    print("=" * 60)
    print(f"Versiyon: 3.0 | Parametrik Giriş | Port Check | Console Output\n")
    print("💡 İpucu: -h yazarak yardım alabilirsiniz!")
    print("💡 Kullanım: Sadece IP ve parametreleri yazın!")
    print("💡 Örnekler:")
    print("   192.168.1.1 -h  (tüm servisler)")
    print("   192.168.1.1 -s ssh -t 8  (SSH, 8 thread)")
    print("   192.168.1.1 -s ftp -L users.txt -P pass.txt  (özel wordlist)")
    print("   192.168.1.1 -s http -V -f  (HTTP, verbose, first found)")
    print("   192.168.1.1 -s ssh -l admin -p password123  (tek kullanıcı/şifre)")
    print("   192.168.1.1 -n  (nmap taraması)")
    print("   192.168.1.1  (port check)")
    print("=" * 60)

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
    if giris.lower() in ['-h', '--help', 'help', 'yardım']:
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
        giris = input("Hedef IP ve parametreleri girin (örn: 192.168.1.1 -h): ").strip()
        
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
    
    for servis_adi, port in Ayarlar.PORTLAR.items():
        if servis_adi in servis_esleme:
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
            saldiri = servis_esleme[servis_adi](hedef_ip, port)
            saldiri.saldir(Ayarlar.KULLANICI_ADI_LISTESI, Ayarlar.PAROLA_LISTESI)
        except Exception as e:
            print(f"[!] {servis_adi.upper()} hatası: {str(e)}")

def parametrik_komut_isle(hedef_ip, parametreler):
    """Parametrik komut satırı girişini işler"""
    print(f"[+] Hedef: {hedef_ip}")
    print(f"[+] Parametreler: {' '.join(parametreler)}")
    
    # Parametreleri analiz et
    servisler = []
    hydra_parametreleri = {}
    
    i = 0
    while i < len(parametreler):
        param = parametreler[i]
        
        # Servis seçimi (-s)
        if param == "-s" and i + 1 < len(parametreler):
            servis = parametreler[i + 1].lower()
            if servis in Ayarlar.PORTLAR:
                servisler.append(servis)
            else:
                print(f"[!] Bilinmeyen servis: {servis}")
            i += 2
            
        # Tüm servisler (-h)
        elif param == "-h":
            servisler = list(Ayarlar.PORTLAR.keys())
            i += 1
            
        # Nmap taraması (-n)
        elif param == "-n":
            print(f"[+] Nmap taraması başlatılıyor...")
            raporlayici = Raporlayici()
            nmap_tarama_ve_saldiri(hedef_ip, raporlayici)
            return
            
        # Hydra parametreleri
        elif param in ["-L", "-P", "-l", "-p", "-t", "-W", "-s", "-o", "-b", "-R", "-F", "-C", "-M", "-m"]:
            if i + 1 < len(parametreler):
                hydra_parametreleri[param] = parametreler[i + 1]
                print(f"[+] Hydra parametresi: {param} {parametreler[i + 1]}")
                i += 2
            else:
                print(f"[!] {param} parametresi için değer eksik")
                i += 1
                
        # Boolean parametreler
        elif param in ["-V", "-d", "-f", "-R", "-x"]:
            hydra_parametreleri[param] = True
            print(f"[+] Hydra parametresi: {param}")
            i += 1
            
        # Özel parametreler (-- ile başlayan)
        elif param.startswith("--"):
            if i + 1 < len(parametreler) and not parametreler[i + 1].startswith("-"):
                hydra_parametreleri[param] = parametreler[i + 1]
                print(f"[+] Özel parametre: {param} {parametreler[i + 1]}")
                i += 2
            else:
                hydra_parametreleri[param] = True
                print(f"[+] Özel parametre: {param}")
                i += 1
                
        # Bilinmeyen parametreler
        else:
            print(f"[!] Bilinmeyen parametre: {param}")
            i += 1
    
    # Eğer servis belirtilmemişse port check yap
    if not servisler:
        print(f"[+] Port check ile servis tespiti yapılıyor...")
        port_checker = PortChecker(hedef_ip)
        acik_portlar = port_checker.servis_portlarini_tara()
        acik_servisler = port_checker.acik_servisleri_getir()
        servisler = list(acik_servisler.keys())
        
        if not servisler:
            print("[-] Açık servis bulunamadı!")
            return
    
    print(f"[+] Saldırılacak servisler: {', '.join(servisler).upper()}")
    
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
    
    # Varsayılan değerler
    kullanici_listesi = hydra_parametreleri.get('-L', Ayarlar.KULLANICI_ADI_LISTESI)
    sifre_listesi = hydra_parametreleri.get('-P', Ayarlar.PAROLA_LISTESI)
    
    # Saldırıları başlat
    raporlayici = Raporlayici()
    for servis_adi in servisler:
        if servis_adi in servis_esleme:
            try:
                port = Ayarlar.PORTLAR[servis_adi]
                saldiri = servis_esleme[servis_adi](hedef_ip, port)
                
                # Hydra parametrelerini uygula
                for param, value in hydra_parametreleri.items():
                    if param == '-t':
                        saldiri.thread_sayisi = int(value)
                    elif param == '-W':
                        saldiri.timeout = int(value)
                    elif param == '-L':
                        saldiri.kullanici_listesi = value
                    elif param == '-P':
                        saldiri.sifre_listesi = value
                    elif param == '-l':
                        saldiri.tek_kullanici = value
                    elif param == '-p':
                        saldiri.tek_sifre = value
                    elif param == '-s':
                        saldiri.port = int(value)
                    elif param == '-V':
                        saldiri.verbose = True
                    elif param == '-d':
                        saldiri.debug = True
                    elif param == '-f':
                        saldiri.first_found = True
                    elif param == '-R':
                        saldiri.restore = True
                    elif param == '-o':
                        saldiri.output_file = value
                    elif param == '-b':
                        saldiri.log_file = value
                    elif param == '-x':
                        saldiri.xml_output = True
                    elif param == '-F':
                        saldiri.form_params = value
                    elif param == '-C':
                        saldiri.custom_params = value
                    elif param == '-M':
                        saldiri.module_path = value
                    elif param == '-m':
                        saldiri.service_name = value
                
                saldiri.saldir(kullanici_listesi, sifre_listesi)
            except Exception as e:
                print(f"[!] {servis_adi.upper()} hatası: {str(e)}")
                continue

def main():
    # Dizinleri oluştur
    for dir in ["wordlists", "reports", "sonuclar"]:
        os.makedirs(dir, exist_ok=True)
    
    giris_ekrani()
    
    # Komut satırı parametreleri kontrolü
    if len(sys.argv) > 1:
        hedef_ip = sys.argv[1]
        
        # Tek argüman verilmiş ama içinde parametreler var ise (örn: "192.168.1.1 -h") ayrıştır
        if len(sys.argv) == 2 and (' ' in hedef_ip):
            try:
                tokens = shlex.split(hedef_ip)
            except Exception:
                tokens = hedef_ip.split()
            if len(tokens) >= 2:
                hedef_ip, parametreler = tokens[0], tokens[1:]
                print(f"[+] Hedef: {hedef_ip}")
                print(f"[+] Parametreler: {' '.join(parametreler)}")
                parametrik_komut_isle(hedef_ip, parametreler)
                return
        
        # Eğer sadece IP verilmişse parametrik komut işle
        if len(sys.argv) > 2:
            parametreler = sys.argv[2:]
            parametrik_komut_isle(hedef_ip, parametreler)
        else:
            # Sadece IP verilmişse port check yap
            print(f"[+] Hedef: {hedef_ip}")
            print(f"[+] Port check ile saldırı başlatılıyor...")
            raporlayici = Raporlayici()
            port_check_ve_saldiri(hedef_ip, raporlayici)
            
    else:
        # Etkileşimli mod
        hedef_giris = hedef_ip_al()
        
        # Interaktif modda birleşik giriş verilmişse (örn: "192.168.1.1 -h") doğrudan işle ve çık
        if isinstance(hedef_giris, tuple):
            hedef_ip, parametreler = hedef_giris
            print(f"\n[+] Hedef: {hedef_ip}")
            parametrik_komut_isle(hedef_ip, parametreler)
            return
        else:
            hedef_ip = hedef_giris
        
        print(f"\n[+] Hedef: {hedef_ip}")
        print("\nMod seçimi:")
        print("1. Port Check ile saldırı (varsayılan)")
        print("2. Nmap ile detaylı tarama")
        print("3. Tüm servislere saldırı")
        print("4. Belirli servis seçimi")
        
        secim = input("\nMod seçin (1-4, varsayılan: 1): ").strip() or "1"
        
        raporlayici = Raporlayici()
        
        if secim == "2":
            nmap_tarama_ve_saldiri(hedef_ip, raporlayici)
        elif secim == "3":
            tum_servislere_saldiri(hedef_ip, raporlayici)
        elif secim == "4":
            servis_adi = input("Servis adı girin (örn: ssh): ").strip().lower()
            belirli_servise_saldiri(hedef_ip, servis_adi, raporlayici)
        else:
            port_check_ve_saldiri(hedef_ip, raporlayici)

if __name__ == "__main__":
    main()