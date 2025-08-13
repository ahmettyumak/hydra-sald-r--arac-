#!/usr/bin/env python3
import os
import socket
import sys
from services.scanner import NmapTarayici
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
from services.port_checker import PortChecker






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
    
    print("\n🔍 NMAP PARAMETRELERİ:")
    print("  -sS              # TCP SYN scan")
    print("  -sT              # TCP connect scan")
    print("  -sU              # UDP scan")
    print("  -sA              # TCP ACK scan")
    print("  -sW              # TCP Window scan")
    print("  -sM              # TCP Maimon scan")
    print("  -sN              # TCP NULL scan")
    print("  -sF              # TCP FIN scan")
    print("  -sX              # TCP Xmas scan")
    print("  -p <ports>       # Port aralığı (örn: 1-1000)")
    print("  -p-              # Tüm portlar (1-65535)")
    print("  -F               # Hızlı tarama (top 100 port)")
    print("  -T<0-5>          # Timing template (0=paranoid, 5=insane) veya -T4 şeklinde")
    print("  -A               # Agresif tarama (OS detection, version)")
    print("  -O               # OS detection")
    print("  -sV              # Service/version detection")
    print("  -sC              # Default script scan")
    print("  -v/-vv/-vvv      # Verbose seviyeleri")
    print("  -d/-dd/-ddd      # Debug seviyeleri")
    print("  -Pn              # Host discovery atla")
    print("  -n               # DNS çözümlemesini kapat")
    print("  --script=<name>  # Özel script çalıştır veya --script=... şekli")
    print("  -oN <file>       # Normal output")
    print("  -oX <file>       # XML output")
    print("  -oG <file>       # Grepable output")
    
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
    print("  -u              # Kullanıcıları döngüye al")
    print("  -e <nsr>        # Null, same, reverse")
    print("  -4/-6           # IPv4/IPv6")
    print("  -S              # SSL bağlantısı")
    print("  -O              # Eski SSL v2/v3")
    print("  -K              # Başarısız denemeleri tekrarlama")
    print("  -q              # Bağlantı hata mesajlarını gösterme")
    print("  -U              # Servis modül detayları")
    print("  -I              # Restore dosyasını bekleme")
    
    print("\nDESTEKLENEN SERVİSLER:")
    print("  FTP, SSH, HTTP, HTTPS, MySQL, PostgreSQL, MongoDB")
    print("  SMTP, POP3, IMAP, RDP, SMB, Telnet, VNC, MSSQL")
    
    print("\nNOTLAR:")
    print("  • Hydra söz dizimi: [OPTIONS] target service")
    print("  • Çoklu hedef: -M targets.txt service")
    print("  • Port belirtimi: -s parametresi ile (örn: -s 2222)")
    print("  • -h modu: Açık servisler listelenir ve saldırı başlatılır")
    print("  • Belirli servis verildiğinde port check yapılmaz")
    print("  • Target: IP adresi, hostname veya ağ aralığı")
    
    print("\nDOSYA FORMATLARI:")
    print("  • targets.txt: Her satırda bir hedef (IP, hostname)")
    print("  • users.txt: Her satırda bir kullanıcı adı")
    print("  • passwords.txt: Her satırda bir şifre")
    
    print("="*70)







def nmap_tarama_ve_saldiri(hedef_ip, raporlayici, nmap_parametreleri=None):
    """Nmap ile detaylı tarama ve saldırı"""
    try:
        print(f"\n[+] {hedef_ip} için Nmap taraması başlatılıyor...")
        
        # Nmap parametrelerini göster
        if nmap_parametreleri:
            print(f"[*] Nmap parametreleri: {' '.join([f'{k} {v}' if v is not True else k for k, v in nmap_parametreleri.items()])}")
        
        tarayici = NmapTarayici(hedef_ip)
        acik_servisler = tarayici.detayli_tarama(nmap_parametreleri=nmap_parametreleri)
        
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
            # Nmap parametrelerini topla
            nmap_parametreleri = {}
            i += 1  # -nmap'i atla
            
            # Sonraki parametreleri Nmap parametresi olarak işle
            while i < len(parametreler):
                nmap_tok = parametreler[i]
                if not nmap_tok.startswith('-'):
                    break

                boolean_flags = {"-sS", "-sT", "-sU", "-sA", "-sW", "-sM", "-sN", "-sF", "-sX", "-F", "-A", "-O", "-sV", "-sC", "-Pn", "-n"}
                value_flags = {"-p", "-T", "--script", "-oN", "-oX", "-oG"}

                # -v/-vv/-vvv ve -d/-dd/-ddd desteği
                stripped = nmap_tok.lstrip('-')
                if stripped and set(stripped) <= {"v"}:
                    nmap_parametreleri[nmap_tok] = True
                    i += 1
                    continue
                if stripped and set(stripped) <= {"d"}:
                    nmap_parametreleri[nmap_tok] = True
                    i += 1
                    continue
                # -V'yi -v olarak kabul et (yaygın karışıklık için tolerans)
                if nmap_tok == "-V":
                    nmap_parametreleri["-v"] = True
                    i += 1
                    continue

                # -T4 gibi birleşik kullanım
                if nmap_tok.startswith('-T') and len(nmap_tok) > 2 and nmap_tok[2:].isdigit():
                    nmap_parametreleri['-T'] = nmap_tok[2:]
                    i += 1
                    continue
                # --script=xxx desteği
                if nmap_tok.startswith('--script='):
                    nmap_parametreleri['--script'] = nmap_tok.split('=', 1)[1]
                    i += 1
                    continue
                # -p- tüm portlar
                if nmap_tok == '-p-':
                    nmap_parametreleri['-p'] = '-'
                    i += 1
                    continue

                if nmap_tok in boolean_flags:
                    nmap_parametreleri[nmap_tok] = True
                    i += 1
                    continue
                if nmap_tok in value_flags and i + 1 < len(parametreler):
                    nmap_parametreleri[nmap_tok] = parametreler[i + 1]
                    i += 2
                    continue

                # Nmap parametresi değil, döngüyü kır
                break
            # Hız için: kullanıcı daraltma vermemişse varsayılan argümanları kaldır
            if not any(k in nmap_parametreleri for k in ('-p', '-F')):
                nmap_parametreleri['__no_defaults__'] = True
            
            print(f"[+] Nmap taraması başlatılıyor...")
            raporlayici = Raporlayici()
            nmap_tarama_ve_saldiri(hedef_ip, raporlayici, nmap_parametreleri)
            return
        
        # Servis belirtimi (pozisyonel parametre olarak)
        elif not param.startswith('-') and param.lower() in Ayarlar.PORTLAR:
            servisler.append(param.lower())
            servisler_explicit = True
            i += 1
            
        # Hydra parametreleri
        elif param in ["-L", "-P", "-l", "-p", "-t", "-W", "-o", "-b", "-R", "-F", "-C", "-M", "-m", "-V", "-d", "-f", "-x", "-u", "-e", "-4", "-6", "-S", "-O", "-K", "-q", "-U", "-I"]:
            if param in ["-L", "-P", "-l", "-p", "-t", "-W", "-o", "-b", "-F", "-C", "-M", "-m"]: # Değer alan parametreler
                if i + 1 < len(parametreler):
                    hydra_parametreleri[param] = parametreler[i + 1]
                    i += 2
                else:
                    print(f"[!] Hata: {param} parametresi için değer eksik.")
                    i += 1 # Hatalı parametreyi atla
            else: # Değer almayan parametreler (-R, -V, -d, -f, -x, -u, -e, -4, -6, -S, -O, -K, -q, -U, -I)
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
        # Servis->port eşlemesini hazırla (özel port verilmişse onu kullan)
        service_to_port = {}
        for servis_adi in servisler:
            port = Ayarlar.PORTLAR.get(servis_adi)
            if custom_port is not None:
                port = custom_port
            if port is None:
                print(f"[!] {servis_adi.upper()} için varsayılan port bulunamadı ve özel port belirtilmedi. Atlanıyor.")
                continue
            service_to_port[servis_adi] = port
        # Kullanıcıya bilgilendirme
        for s_name, s_port in service_to_port.items():
            print(f"[*] {s_name.upper()} port {s_port} kontrol ediliyor...")
        # Toplu tarama ile daha doğru sonuç alın (yeniden denemeli)
        try:
            port_checker = PortChecker(hedef_ip)
            unique_ports = sorted(set(service_to_port.values()))
            scanned = port_checker.toplu_port_tarama(unique_ports)
        except Exception as e:
            print(f"[!] Toplu port tarama hatası: {str(e)}")
            scanned = {}
        # Sonuçları servis bazında değerlendir
        for s_name, s_port in service_to_port.items():
            if scanned.get(s_port):
                print(f"[+] {s_name.upper()} port {s_port} açık")
                acik_servisler[s_name] = s_port
            else:
                print(f"[-] {s_name.upper()} port {s_port} kapalı - atlanıyor")
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
    from concurrent.futures import ThreadPoolExecutor, as_completed
    def run_attack(servis_adi, port):
        if servis_adi not in servis_esleme:
            return (servis_adi, False, "Desteklenmeyen servis")
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
            ok = saldiri.saldir(kullanici_listesi, sifre_listesi)
            return (servis_adi, bool(ok), None)
        except Exception as e:
            return (servis_adi, False, str(e))

    max_workers = getattr(Ayarlar, 'BRUTE_FORCE_MAX_PARALLEL', 3)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_attack, s, p): (s, p) for s, p in acik_servisler.items()}
        for future in as_completed(futures):
            s, p = futures[future]
            try:
                srv, ok, err = future.result()
                if err:
                    print(f"[!] {srv.upper()} hatası: {err}")
            except Exception as e:
                print(f"[!] {s.upper()} beklenmeyen hata: {str(e)}")


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
        
        # Nmap parametrelerini topla
        nmap_parametreleri = {}
        nmap_index = tokens.index('-nmap')
        
        # -nmap'den sonraki parametreleri kontrol et
        i = nmap_index + 1
        while i < len(tokens):
            tok = tokens[i]
            if not tok.startswith('-'):
                break

            boolean_flags = {"-sS", "-sT", "-sU", "-sA", "-sW", "-sM", "-sN", "-sF", "-sX", "-F", "-A", "-O", "-sV", "-sC", "-Pn", "-n"}
            value_flags = {"-p", "-T", "--script", "-oN", "-oX", "-oG"}

            stripped = tok.lstrip('-')
            if stripped and set(stripped) <= {"v"}:
                nmap_parametreleri[tok] = True
                i += 1
                continue
            if stripped and set(stripped) <= {"d"}:
                nmap_parametreleri[tok] = True
                i += 1
                continue
            if tok == "-V":
                nmap_parametreleri["-v"] = True
                i += 1
                continue

            if tok.startswith('-T') and len(tok) > 2 and tok[2:].isdigit():
                nmap_parametreleri['-T'] = tok[2:]
                i += 1
                continue
            if tok.startswith('--script='):
                nmap_parametreleri['--script'] = tok.split('=', 1)[1]
                i += 1
                continue
            if tok == '-p-':
                nmap_parametreleri['-p'] = '-'
                i += 1
                continue

            if tok in boolean_flags:
                nmap_parametreleri[tok] = True
                i += 1
                continue
            if tok in value_flags and i + 1 < len(tokens):
                nmap_parametreleri[tok] = tokens[i + 1]
                i += 2
                continue

            break
        
        # Nmap parametrelerini parametrik_komut_isle'ye gönder
        nmap_args = ['-nmap']
        # Kullanıcı -F (fast) veya -p ile daraltma vermediyse varsayılanları yüklemek yerine boş set kullan (hız için)
        if not any(k in nmap_parametreleri for k in ('-p', '-F')):
            nmap_parametreleri['__no_defaults__'] = True
        for param, value in nmap_parametreleri.items():
            nmap_args.append(param)
            if value is not True:
                nmap_args.append(str(value))
        
        parametrik_komut_isle(target, nmap_args)
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