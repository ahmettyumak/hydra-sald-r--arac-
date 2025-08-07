from .base import BruteForceBase

class SMBBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=445):
        super().__init__(hedef_ip, hedef_port, "SMB")
    
    def _hydra_tipi(self):
        return "smb"