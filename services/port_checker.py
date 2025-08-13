import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import Ayarlar

class PortChecker:
    def __init__(self, hedef_ip, timeout=None):
        self.hedef_ip = hedef_ip
        self.timeout = timeout or Ayarlar.PORT_CHECK_TIMEOUT
        self.acik_portlar = {}
        
    def port_kontrol(self, port):
        """Tek bir portu kontrol eder"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sonuc = sock.connect_ex((self.hedef_ip, port))
            sock.close()
            if sonuc == 0:
                return port, True
            return port, False
        except:
            return port, False
        
    def toplu_port_tarama(self, port_listesi):
        """Belirtilen portları paralel olarak tarar"""
        print(f"[*] {self.hedef_ip} için port taraması başlatılıyor...")
        print(f"[*] {len(port_listesi)} port kontrol edilecek...")
        
        self.acik_portlar = {}
        
        with ThreadPoolExecutor(max_workers=Ayarlar.PORT_CHECK_THREADS) as executor:
            future_to_port = {executor.submit(self.port_kontrol, port): port for port in port_listesi}
            
            for future in as_completed(future_to_port):
                port, acik = future.result()
                if acik:
                    self.acik_portlar[port] = True
                    print(f"[+] Port {port} açık")
        
        return self.acik_portlar
        
    def servis_portlarini_tara(self):
        """Desteklenen servislerin portlarını tarar"""
        from config import Ayarlar
        port_listesi = list(Ayarlar.PORTLAR.values())
        return self.toplu_port_tarama(port_listesi)
        
    def acik_servisleri_getir(self):
        """Açık portlara karşılık gelen servisleri döndürür"""
        from config import Ayarlar
        acik_servisler = {}
        
        for port, acik in self.acik_portlar.items():
            if acik:
                for servis_adi, servis_port in Ayarlar.PORTLAR.items():
                    if servis_port == port:
                        acik_servisler[servis_adi] = port
                        break
        
        return acik_servisler
