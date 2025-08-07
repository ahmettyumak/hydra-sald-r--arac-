from .base import BruteForceBase

class TelnetBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=23):
        super().__init__(hedef_ip, hedef_port, "Telnet")
    
    def _hydra_tipi(self):
        return "telnet"