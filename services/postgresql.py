# services/postgresql.py
from .base import BruteForceBase

class PostgreSQLBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=5432):
        super().__init__(hedef_ip, hedef_port, "postgresql")  # Küçük harfle tutarlı olun
    
    def _hydra_tipi(self):
        return "postgres"
    
    def saldir(self, kullanici_listesi, parola_listesi):
        # PostgreSQL'e özel saldırı metodunu implemente edin
        komut = f"hydra -L {kullanici_listesi} -P {parola_listesi} {self.hedef_ip} postgres -s {self.hedef_port}"
        return self._komut_calistir(komut)