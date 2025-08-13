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
                    ports = sorted(self.nm[host][proto].keys())
                    for port in ports:
                        port_info = self.nm[host][proto][port]
                        servis_raw = port_info.get('name', '')
                        servis = self._normalize_servis(servis_raw, port_info, port)
                        versiyon = port_info.get('version', 'bilinmiyor')
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
        
        # Varsayılan argümanları al veya sıfırdan başla
        use_no_defaults = bool(nmap_parametreleri.get('__no_defaults__'))
        if use_no_defaults:
            # Özel anahtarı tüket
            nmap_parametreleri = {k: v for k, v in nmap_parametreleri.items() if k != '__no_defaults__'}
            args = []
        else:
            args = Ayarlar.NMAP_ARGUMANLARI.split()
        
        # Yeni parametreleri ekle (bazılarını override et)
        for param, value in nmap_parametreleri.items():
            if value is True:
                # Değer almayan parametreler (-sS, -sV, -A, -v, -Pn, -n, vb.)
                if param not in args:
                    args.append(param)
                continue
            
            # Değer alan parametreler (-p, -T, --script, -oN, -oX, -oG, vb.)
            if param == '-T':
                # Mevcut -T* tokenlarını kaldır ve -T4 formatında ekle
                args = [tok for tok in args if not (tok.startswith('-T') and len(tok) >= 2 and tok[2:])]
                args.append(f"-T{value}")
                continue
            if param == '--script':
                # --script=... biçimini normalize et, varsa eskisini sil
                args = [tok for tok in args if not tok.startswith('--script')]
                args.append(f"--script={value}")
                continue
            
            # Diğerleri için çiftli formatı koru
            if param in args:
                # Aynı param zaten varsa (örn: -p), mevcut değeri olduğu gibi bırakıp yenisini ekle
                # Nmap son değeri kullanacaktır
                pass
            args.append(param)
            args.append(str(value))
        
        return ' '.join(args)

    def _normalize_servis(self, name, port_info, port_number):
        """Nmap servis adını araç içinde kullanılan servis adına dönüştürür."""
        s = (name or '').lower()
        tunnel = (port_info.get('tunnel') or '').lower()
        # HTTPS tespiti: tunnel=ssl veya servis adında https ya da ssl/http benzeri
        if tunnel == 'ssl' or s.startswith('https') or s.startswith('ssl/http') or port_number in (443, 8443, 9443):
            return 'https'
        # HTTP varyasyonlarını http'ye indir
        if 'http' in s:
            return 'http'
        # Bazı yaygın eşleşmeler
        if s in ('ms-wbt-server', 'rdp'):
            return 'rdp'
        if s in ('microsoft-ds', 'smb'):
            return 'smb'
        if s in ('ms-sql-s', 'ms-sql', 'mssql'):
            return 'mssql'
        return s