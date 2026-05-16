import os
import subprocess
import sys
import json

def get_live_url(username):
    # Method 1: yt-dlp (Daha hızlı ve güvenilir)
    try:
        # print(f"yt-dlp ile deniniyor: @{username}", file=sys.stderr)
        result = subprocess.run(
            [sys.executable, "-m", "yt_dlp", "--print", "urls", f"https://www.tiktok.com/@{username}/live"],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        if result.returncode == 0 and result.stdout.strip():
            urls = result.stdout.strip().split('\n')
            # İlk m3u8 URL'sini al
            m3u8_url = next((u for u in urls if ".m3u8" in u), urls[0])
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
                "Referer": "https://www.tiktok.com/",
                "Origin": "https://www.tiktok.com"
            }
            print(json.dumps({"url": m3u8_url, "headers": headers}))
            return
    except Exception as e:
        pass
        # print(f"yt-dlp hatası: {e}", file=sys.stderr)

    # Method 2: Playwright Fallback (Eğer yt-dlp başarısız olursa)
    from playwright.sync_api import sync_playwright
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SESSION_DIR = os.path.join(BASE_DIR, "tiktok_session")
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=SESSION_DIR,
                headless=True,
                args=["--disable-blink-features=AutomationControlled"],
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
            )
            page = browser.pages[0] if browser.pages else browser.new_page()
            
            live_url = None
            headers = {}
            
            def handle_request(request):
                nonlocal live_url, headers
                if ".m3u8" in request.url and live_url is None:
                    live_url = request.url
                    headers = request.headers

            page.on("request", handle_request)
            page.goto(f"https://www.tiktok.com/@{username}/live", timeout=60000)
            page.wait_for_timeout(10000)
            
            if not live_url:
                page.mouse.click(640, 360)
                page.wait_for_timeout(10000)

            if live_url:
                print(json.dumps({"url": live_url, "headers": headers}))
            else:
                page.screenshot(path="live_status.png")
                print(json.dumps({"error": "No .m3u8 URL found via any method."}))
        except Exception as e:
            print(json.dumps({"error": str(e)}))
        finally:
            browser.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        get_live_url(sys.argv[1])
    else:
        print(json.dumps({"error": "No username provided"}))
