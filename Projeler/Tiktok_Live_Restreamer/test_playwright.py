from playwright.sync_api import sync_playwright
import json
import re

def get_stream_url(username):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print(f"Navigating to TikTok @{username}...")
        try:
            page.goto(f"https://www.tiktok.com/@{username}/live", timeout=30000)
            page.wait_for_timeout(3000)
            html = page.content()
            
            # Extract SIGI_STATE
            match = re.search(r'window\["SIGI_STATE"\]=(.*?);window\["SIGI_RETRY"\]', html)
            if match:
                sigi_state = json.loads(match.group(1))
                live_room = sigi_state.get('LiveRoom', {})
                live_room_user = live_room.get('liveRoomUserInfo', {})
                user = live_room_user.get('user', {})
                status = user.get('status', 0)
                
                if status != 2:
                    print(f"Kullanıcı {username} şu anda canlı yayında değil. (status: {status})")
                    return None
                    
                live_url = user.get('streamUrl', {})
                rtmp_pull_url = live_url.get('rtmp_pull_url')
                flv_pull_url = live_url.get('flv_pull_url')
                hls_pull_url = live_url.get('hls_pull_url_map')
                
                print("Found urls:", rtmp_pull_url, flv_pull_url)
                # Genelde flv en iyisidir
                url_to_return = flv_pull_url.get('FULL_HD1') if flv_pull_url else None
                if not url_to_return and rtmp_pull_url:
                    url_to_return = rtmp_pull_url
                if not url_to_return and flv_pull_url:
                    url_to_return = list(flv_pull_url.values())[0]
                if not url_to_return and hls_pull_url:
                    url_to_return = list(hls_pull_url.values())[0]
                    
                return url_to_return
            else:
                print("SIGI_STATE bulunamadı. Sayfa yapısı değişmiş olabilir.")
        except Exception as e:
            print(f"Hata: {e}")
        finally:
            browser.close()
    return None

if __name__ == '__main__':
    url = get_stream_url('hakimpolat8')
    print(f"Stream URL: {url}")
