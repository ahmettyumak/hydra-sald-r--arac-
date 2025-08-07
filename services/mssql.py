from .base import BruteForceBase

class MSSQLBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=1433):
        super().__init__(hedef_ip, hedef_port, "MSSQL")
    
    def _hydra_tipi(self):
        return "mssql"