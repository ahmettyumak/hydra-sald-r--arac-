from .base import BruteForceBase

class SSHBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=22):
        super().__init__(hedef_ip, hedef_port, "SSH")