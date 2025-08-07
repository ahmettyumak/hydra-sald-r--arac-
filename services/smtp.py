from .base import BruteForceBase

class SMTPBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=25):
        super().__init__(hedef_ip, hedef_port, "SMTP")
    
    def _hydra_tipi(self):
        return "smtp"