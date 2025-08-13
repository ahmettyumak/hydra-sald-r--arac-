from .base import BruteForceBase

class TelnetBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=23):
        super().__init__(hedef_ip, hedef_port, "Telnet")
        # Telnet modülü için daha güvenilir varsayılanlar
        self.additional_params = ["-4"]  # IPv4 zorla (çözünürlük/bağlantı sorunlarını azaltır)
        self.thread_sayisi = 1            # Telnet doğası gereği eşzamanlılık sorunlu
        self.timeout = 15                 # Aşırı beklemeyi önlemek için makul timeout
    
    def _hydra_tipi(self):
        return "telnet"