from .base import BruteForceBase

class MongoDBBruteForce(BruteForceBase):
    def __init__(self, hedef_ip, hedef_port=27017):
        super().__init__(hedef_ip, hedef_port, "MongoDB")

    def _hydra_tipi(self):
        return "mongodb"