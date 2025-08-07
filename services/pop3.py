from .base import BruteForceBase

class POP3BruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=110):
        super().__init__(hedef_ip, hedef_port, "POP3")
    
    def _hydra_tipi(self):
        return "pop3"