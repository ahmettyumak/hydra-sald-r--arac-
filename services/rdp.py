from .base import BruteForceBase

class RDPBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=3389):
        super().__init__(hedef_ip, hedef_port, "RDP")

    def _hydra_tipi(self):
        return "rdp"