import nmap
from utils.raporlayici import Raporlayici

class NmapTarayici:
    def __init__(self, hedef_ip):
        self.hedef_ip = hedef_ip
        self.nm = nmap.PortScanner()
        self.rapor = Raporlayici()
    
    def detayli_tarama(self, port_araligi='1-10000'):
        """Nmap ile gelişmiş servis ve versiyon tespiti"""
        try:
            print(f"[*] {self.hedef_ip} Nmap taraması başlatılıyor (Portlar: {port_araligi})...")
            
            # Gelişmiş tarama parametreleri
            args = '-sS -sV --script=banner -T4 --open'
            self.nm.scan(hosts=self.hedef_ip, ports=port_araligi, arguments=args)
            
            if not self.nm.all_hosts():
                raise ValueError("Hedef taranamadı veya filtreli")
            
            sonuclar = []
            for host in self.nm.all_hosts():
                for proto in self.nm[host].all_protocols():
                    ports = self.nm[host][proto].keys()
                    for port in ports:
                        servis = self.nm[host][proto][port]['name']
                        versiyon = self.nm[host][proto][port].get('version', 'bilinmiyor')
                        sonuclar.append({
                            'port': port,
                            'servis': servis,
                            'versiyon': versiyon,
                            'protokol': proto
                        })
            return sonuclar
            
        except Exception as e:
            self.rapor.rapor_ekle("NMAP", self.hedef_ip, "N/A", "HATA", str(e))
            return []