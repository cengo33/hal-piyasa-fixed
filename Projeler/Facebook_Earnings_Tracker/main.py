import os
import time
import requests
import schedule
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Env değişkenlerini yükle
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
FACEBOOK_URL = os.getenv("FACEBOOK_URL", "https://www.facebook.com/professional_dashboard/profile_insights/earnings/")

# Session dizini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_DIR = os.path.join(BASE_DIR, "fb_session")

def send_telegram_message(message: str):
    """Telegram üzerinden mesaj gönderir."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Hata: TELEGRAM_BOT_TOKEN veya TELEGRAM_CHAT_ID eksik!")
        return
        
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Telegram mesajı başarıyla gönderildi.")
        else:
            print(f"Telegram mesajı gönderilemedi. Hata Kodu: {response.status_code}")
    except Exception as e:
        print(f"Telegram API isteği sırasında hata oluştu: {e}")

def send_telegram_photo(photo_path: str, caption: str):
    """Telegram üzerinden fotoğraflı mesaj gönderir."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Hata: TELEGRAM_BOT_TOKEN veya TELEGRAM_CHAT_ID eksik!")
        return
        
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    data = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption, "parse_mode": "HTML"}
    
    try:
        with open(photo_path, "rb") as photo:
            files = {"photo": photo}
            response = requests.post(url, data=data, files=files)
            if response.status_code == 200:
                print("Telegram fotoğrafı başarıyla gönderildi.")
            else:
                print(f"Telegram fotoğrafı gönderilemedi. Hata Kodu: {response.status_code}")
    except Exception as e:
        print(f"Telegram API fotoğraf isteği sırasında hata oluştu: {e}")

def get_facebook_earnings():
    """Playwright ile Facebook'a bağlanıp kazancı çeker."""
    print("Facebook kazanç verileri alınıyor...")
    
    with sync_playwright() as p:
        if os.path.exists(os.path.join(BASE_DIR, "state.json")):
            browser = p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled", "--no-sandbox", "--disable-dev-shm-usage"]
            )
            context = browser.new_context(
                storage_state=os.path.join(BASE_DIR, "state.json"),
                viewport={"width": 1280, "height": 720},
                locale="tr-TR"
            )
            page = context.new_page()
            print("state.json üzerinden oturum başlatıldı (Railway modu).")
        else:
            browser_context = p.chromium.launch_persistent_context(
                user_data_dir=SESSION_DIR,
                headless=True,
                args=["--disable-blink-features=AutomationControlled", "--no-sandbox", "--disable-dev-shm-usage"],
                viewport={"width": 1280, "height": 720},
                locale="tr-TR",
            )
            page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()
            browser = browser_context
        
        try:
            page.goto(FACEBOOK_URL, wait_until="domcontentloaded", timeout=60000)
            print("Sayfa yüklendi, verilerin gelmesi için 10 saniye bekleniyor...")
            time.sleep(10)
            
            # Sayfanın ekran görüntüsünü al
            screenshot_path = os.path.join(BASE_DIR, "earnings_screenshot.png")
            page.screenshot(path=screenshot_path, full_page=False)
            print(f"Ekran görüntüsü kaydedildi: {screenshot_path}")
            
            # Telegram'a ekran görüntüsünü gönder
            caption = f"📈 <b>Facebook Kazanç Raporu</b>\nZaman: {time.strftime('%d.%m.%Y %H:%M')}\n\nKazanç tablonuz ekteki ekran görüntüsündedir."
            send_telegram_photo(screenshot_path, caption)

        except Exception as e:
            print(f"Hata oluştu: {e}")
            send_telegram_message(f"❌ <b>Sistem Hatası</b>\n\nFacebook verileri çekilirken bir hata oluştu:\n{str(e)}")
        
        finally:
            browser.close()

def login_mode():
    """Kullanıcının ilk defa giriş yapması için tarayıcıyı görünür açar."""
    print("GİRİŞ MODU BAŞLATILDI...")
    print("Açılan tarayıcıda Facebook hesabınıza giriş yapın.")
    print("Giriş yaptıktan sonra tarayıcıyı kapatabilirsiniz. Oturum kaydedilecektir.")
    
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=False,
            viewport={"width": 1280, "height": 720},
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://www.facebook.com/login", wait_until="domcontentloaded")
        
        print("\n--- 5 DAKİKA BEKLEME SÜRESİ BAŞLADI ---")
        print("Lütfen Facebook'ta 'halkompleksi33' sayfasına geçiş yapın.")
        print("İşleminiz bitince bu pencere kapanana kadar bekleyebilir veya kendiniz Chrome'u kapatabilirsiniz.")
        try:
            page.wait_for_timeout(300000) # Kullanıcının işlem yapması için 5 dakika tam bekle
        except:
            pass
            
        try:
            browser.close()
        except:
            pass
        print("Tarayıcı kapatıldı, oturum verisi kaydedildi.")

def schedule_jobs():
    """Günde 4 kez çalışacak şekilde zamanlayıcıyı kurar."""
    # Günde 4 kez çalışması için uygun saatleri belirliyoruz
    schedule.every().day.at("08:00").do(get_facebook_earnings)
    schedule.every().day.at("14:00").do(get_facebook_earnings)
    schedule.every().day.at("20:00").do(get_facebook_earnings)
    schedule.every().day.at("23:50").do(get_facebook_earnings)
    
    print("Zamanlayıcı başlatıldı. Günde 4 kere veri çekilecek (08:00, 14:00, 20:00, 23:50).")
    
    # Çalıştığını test etmek için script açıldığında bir kez hemen çalıştırıyoruz
    get_facebook_earnings()

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--login":
        login_mode()
    else:
        schedule_jobs()
