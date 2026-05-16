import os
import time
import requests
from dotenv import load_dotenv
from main import process_tiktok_to_facebook

load_dotenv()

LINKS_FILE = "links.txt"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram notification skipped: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set.")
        return
        
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Failed to send Telegram message. Status: {response.status_code}")
    except Exception as e:
        print(f"Exception while sending Telegram message: {e}")

def run_auto_post():
    print("=== Auto Post Started ===")
    
    if not os.path.exists(LINKS_FILE):
        error_msg = f"❌ Hata: {LINKS_FILE} bulunamadı. Lütfen paylaşılacak linkleri bu dosyaya ekleyin."
        print(error_msg)
        send_telegram_message(error_msg)
        return

    with open(LINKS_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    if not lines:
        empty_msg = f"⚠️ Bilgi: {LINKS_FILE} boş. Paylaşılacak yeni video yok."
        print(empty_msg)
        send_telegram_message(empty_msg)
        return

    # Take the first line
    first_line = lines[0]
    
    # Parse URL and optional description (separated by comma or pipe)
    parts = first_line.split('|', 1)
    url = parts[0].strip()
    desc = parts[1].strip() if len(parts) > 1 else None

    print(f"Processing URL: {url}")
    success = process_tiktok_to_facebook(url, desc)

    if success:
        # Remove the processed line from the file
        with open(LINKS_FILE, "w", encoding="utf-8") as f:
            for line in lines[1:]:
                f.write(line + "\n")
        
        remaining = len(lines) - 1
        success_msg = f"✅ <b>Başarılı!</b>\n\nVideo başarıyla Facebook'a yüklendi.\nLink: {url}\nKuyrukta kalan video sayısı: {remaining}"
        print(success_msg)
        send_telegram_message(success_msg)
    else:
        fail_msg = f"❌ <b>Hata!</b>\n\nVideo Facebook'a yüklenemedi.\nLink: {url}\nVideo kuyrukta tutuluyor, bir sonraki seferde tekrar denenecek."
        print(fail_msg)
        send_telegram_message(fail_msg)

if __name__ == "__main__":
    run_auto_post()

