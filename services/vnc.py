from .base import BruteForceBase

class VNCBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=5900):
        super().__init__(hedef_ip, hedef_port, "VNC")

    def _hydra_tipi(self):
        return "vnc"