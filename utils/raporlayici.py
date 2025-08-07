from datetime import datetime
import os

class Raporlayici:
    def __init__(self):
        self.raporlar = []
        if not os.path.exists("sonuclar"):
            os.makedirs("sonuclar")

    def rapor_ekle(self, servis_adi, hedef_ip, hedef_port, durum, mesaj):
        zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rapor = {
            "zaman": zaman,
            "servis": servis_adi,
            "hedef_ip": hedef_ip,
            "hedef_port": hedef_port,
            "durum": durum,
            "mesaj": mesaj
        }
        self.raporlar.append(rapor)

    def rapor_yazdir(self):
        print("\n" + "="*60)
        print("BRUTE-FORCE SONUÇ RAPORU".center(60))
        print("="*60)
        for r in self.raporlar:
            print(f"[{r['zaman']}] {r['servis']} ({r['hedef_ip']}:{r['hedef_port']}) → {r['durum']}")
            print(f"    Detay: {r['mesaj']}\n")

    def raporu_dosyaya_kaydet(self, dosya_adi):
        with open(dosya_adi, "w", encoding="utf-8") as dosya:
            dosya.write("="*60 + "\n")
            dosya.write("BRUTE-FORCE SONUÇ RAPORU\n".center(60))
            dosya.write("="*60 + "\n\n")
            for r in self.raporlar:
                dosya.write(f"[{r['zaman']}] {r['servis']} ({r['hedef_ip']}:{r['hedef_port']}) → {r['durum']}\n")
                dosya.write(f"    Detay: {r['mesaj']}\n\n")