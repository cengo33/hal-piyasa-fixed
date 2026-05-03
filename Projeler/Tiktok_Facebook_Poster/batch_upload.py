import time
from main import process_tiktok_to_facebook

urls_and_descriptions = [
    ("https://www.youtube.com/shorts/kjIazjSvTOg", "Tarımda Yeni Dönem 🌾✨ #tarım #ziraat"),
    ("https://www.youtube.com/shorts/GYdE9yIDR4Q", "Bereketli Topraklar, İnovatif Tarım 🚜🌱 #çiftçi #teknoloji"),
    ("https://www.youtube.com/shorts/D-Qk6C9buaQ", "Doğanın Bereketi 🌿🌻 #tarımsalteknoloji #hasat")
]

if __name__ == "__main__":
    for i, (url, desc) in enumerate(urls_and_descriptions):
        print(f"\n--- İşleniyor ({i+1}/3) ---")
        process_tiktok_to_facebook(url, desc)
        if i < 2:
            print("Sonraki video için 5 saniye bekleniyor...")
            time.sleep(5)
    print("\n--- Tüm videolar başarıyla gönderildi! ---")
