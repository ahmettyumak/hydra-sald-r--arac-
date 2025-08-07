from .base import BruteForceBase

class MySQLBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=3306):
        super().__init__(hedef_ip, hedef_port, "MySQL")
    
    def _hydra_tipi(self):
        return "mysql"