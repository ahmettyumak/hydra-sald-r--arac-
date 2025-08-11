from .base import BruteForceBase

class HTTPBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=80):
        super().__init__(hedef_ip, hedef_port, "HTTP")

    def _hydra_tipi(self):
        # Form parametreleri sağlandıysa form brute kullan
        if hasattr(self, 'form_params') and self.form_params:
            return "http-post-form"
        return "http-get"