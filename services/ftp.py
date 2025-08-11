from .base import BruteForceBase

class FTPBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=21):
        super().__init__(hedef_ip, hedef_port, "FTP")
        
    def _hydra_tipi(self):
        return "ftp"