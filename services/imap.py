from .base import BruteForceBase

class IMAPBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=143):
        super().__init__(hedef_ip, hedef_port, "IMAP")
    
    def _hydra_tipi(self):
        return "imap"