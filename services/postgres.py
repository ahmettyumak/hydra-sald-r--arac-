from .base import BruteForceBase

class PostgreSQLBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=5432):
        super().__init__(hedef_ip, hedef_port, "PostgreSQL")
    
    def _hydra_tipi(self):
        return "postgres"