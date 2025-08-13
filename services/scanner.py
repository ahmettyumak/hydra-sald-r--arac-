import nmap
from utils.raporlayici import Raporlayici
from config import Ayarlar

class NmapTarayici:
    def __init__(self, hedef_ip):
        self.hedef_ip = hedef_ip
        self.nm = nmap.PortScanner()
        self.rapor = Raporlayici()
    
    def detayli_tarama(self, port_araligi=None, nmap_parametreleri=None):
        """Nmap ile gelişmiş servis ve versiyon tespiti"""
        try:
            # Nmap parametrelerini işle
            nmap_args = self._nmap_parametreleri_isle(nmap_parametreleri)
            
            port_araligi = port_araligi if port_araligi is not None else Ayarlar.NMAP_PORT_ARALIGI
            if port_araligi:
                print(f"[*] {self.hedef_ip} Nmap taraması başlatılıyor (Portlar: {port_araligi})...")
            else:
                print(f"[*] {self.hedef_ip} Nmap taraması başlatılıyor (Varsayılan popüler portlar)...")
            
            # Parametrik hedef kontrolü
            hedef = self._hedef_kontrol(self.hedef_ip)
            if not hedef:
                raise ValueError(f"Geçersiz hedef formatı: {self.hedef_ip}")
            
            if port_araligi:
                self.nm.scan(hosts=hedef, ports=port_araligi, arguments=nmap_args)
            else:
                # ports parametresi None ise nmap'in varsayılan port listesini kullan
                self.nm.scan(hosts=hedef, arguments=nmap_args)
            
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
                            'host': host,
                            'port': port,
                            'servis': servis,
                            'versiyon': versiyon,
                            'protokol': proto
                        })
            return sonuclar
            
        except Exception as e:
            self.rapor.rapor_ekle("NMAP", self.hedef_ip, "N/A", "HATA", str(e))
            return []
    
    def _hedef_kontrol(self, hedef):
        """Hedef formatını kontrol eder ve Nmap için uygun hale getirir"""
        hedef = hedef.strip()
        
        # IP aralığı (192.168.1.1-10)
        if '-' in hedef and hedef.count('.') == 3:
            try:
                base_ip, range_part = hedef.rsplit('.', 1)
                start, end = range_part.split('-')
                # Nmap formatına çevir: 192.168.1.1-10
                return hedef
            except:
                pass
        
        # CIDR notasyonu (192.168.1.0/24)
        if '/' in hedef:
            try:
                ip_part, cidr = hedef.split('/')
                if 0 <= int(cidr) <= 32:
                    return hedef  # Nmap CIDR'ı destekler
            except:
                pass
        
        # Tek IP veya hostname
        return hedef
    
    def _nmap_parametreleri_isle(self, nmap_parametreleri):
        """Nmap parametrelerini işler ve arguments string'i oluşturur"""
        if not nmap_parametreleri:
            return Ayarlar.NMAP_ARGUMANLARI
        
        # Varsayılan argümanları al
        args = Ayarlar.NMAP_ARGUMANLARI.split()
        
        # Yeni parametreleri ekle
        for param, value in nmap_parametreleri.items():
            if value is True:
                # Değer almayan parametreler (-sS, -sV, -A, vb.)
                if param not in args:
                    args.append(param)
            else:
                # Değer alan parametreler (-p, -T, --script, vb.)
                if param not in args:
                    args.append(param)
                    args.append(str(value))
        
        return ' '.join(args)