from .base import BruteForceBase

class HTTPSBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=443):
        super().__init__(hedef_ip, hedef_port, "HTTPS")

    def _hydra_tipi(self):
        return "https-get"