from .base import BruteForceBase

class HTTPSBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=443):
        super().__init__(hedef_ip, hedef_port, "HTTPS")

    def _hydra_tipi(self):
        # Form parametreleri sağlandıysa form brute kullan
        if hasattr(self, 'form_params') and self.form_params:
            return "https-post-form"
        return "https-get"