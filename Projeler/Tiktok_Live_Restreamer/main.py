import os
import subprocess
import sys
import time
from dotenv import load_dotenv
import yt_dlp
import imageio_ffmpeg

load_dotenv()

TIKTOK_USERNAME = os.getenv("TIKTOK_USERNAME", "").strip("@")
FB_RTMP_URL = os.getenv("FACEBOOK_RTMP_URL", "rtmps://live-api-s.facebook.com:443/rtmp/")
FB_STREAM_KEY = os.getenv("FACEBOOK_STREAM_KEY", "")

from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_DIR = os.path.join(BASE_DIR, "tiktok_session")

def get_tiktok_live_url(username):
    stream_url = None
    print(f"Tarayıcı açılıyor ve @{username} yayını aranıyor...")
    
    with sync_playwright() as p:
        is_production = os.getenv("RAILWAY_ENVIRONMENT") is not None
        browser = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=is_production,
            args=["--disable-blink-features=AutomationControlled", "--mute-audio"],
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
            viewport={"width": 390, "height": 844},
            is_mobile=True,
            has_touch=True
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        
        def handle_response(response):
            nonlocal stream_url
            url = response.url
            if stream_url is None:
                # Mobil cihaz olduğu için TikTok kesinlikle .m3u8 (HLS) vermek zorunda
                if '.m3u8' in url and 'pull' in url:
                    stream_url = url
                    print(f"\n[+] Yayın bağlantısı yakalandı (HLS)! ({stream_url[:60]}...)\n")
                        
        page.on('response', handle_response)
        
        try:
            page.goto(f"https://www.tiktok.com/@{username}/live", timeout=60000)
            
            print("\n*** DİKKAT ***")
            print("Tarayıcı açıldı. Eğer ekranda 'Play' tuşu, Çerez onayı veya 18+ uyarısı varsa LÜTFEN ELİNİZLE TIKLAYIN.")
            print("Yayının başlaması için 60 saniye bekleniyor...")
            
            for i in range(60):
                if stream_url:
                    break
                page.wait_for_timeout(1000)
                
        except Exception as e:
            print(f"Sayfa yüklenirken hata oluştu: {e}")
            
        browser.close()
        
    return stream_url

def start_restream():
    if not TIKTOK_USERNAME or not FB_STREAM_KEY or FB_STREAM_KEY == "buraya_facebook_yayin_anahtari_gelecek":
        print("HATA: Lütfen .env dosyasından FACEBOOK_STREAM_KEY ayarını yapın.")
        sys.exit(1)

    try:
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as e:
        print(f"FFmpeg bulunamadı: {e}")
        sys.exit(1)

    while True:
        stream_url = get_tiktok_live_url(TIKTOK_USERNAME)
        
        if not stream_url:
            print("Yayın bağlantısı BULUNAMADI! 60 saniye sonra tekrar denenecek...")
            time.sleep(60)
            continue
            
        print("Canlı yayın bulundu! Facebook'a aktarım başlatılıyor...")
        
        facebook_target = f"{FB_RTMP_URL}{FB_STREAM_KEY}"
        
        command = [
            ffmpeg_exe,
            '-re',
            '-i', stream_url,
            '-c:v', 'libx264',
            '-preset', 'veryfast',
            '-b:v', '2500k',
            '-maxrate', '2500k',
            '-bufsize', '5000k',
            '-pix_fmt', 'yuv420p',
            '-g', '60',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-ar', '44100',
            '-f', 'flv',
            facebook_target
        ]
        
        print("\n======================================================")
        print("YAYIN AKTARIMI BAŞLADI!")
        print("Durdurmak için CTRL+C tuşlarına basabilirsiniz.")
        print("======================================================\n")
        
        process = subprocess.Popen(command)
        try:
            process.wait()
            print("\nYayın koptu veya sonlandı. 10 saniye sonra tekrar denenecek...")
            time.sleep(10)
        except KeyboardInterrupt:
            print("\nYayın aktarımı kullanıcı tarafından durduruldu.")
            process.terminate()
            sys.exit(0)
        except Exception as e:
            print(f"\nAktarım sırasında hata: {e}")
            process.terminate()
            time.sleep(10)

if __name__ == '__main__':
    start_restream()
