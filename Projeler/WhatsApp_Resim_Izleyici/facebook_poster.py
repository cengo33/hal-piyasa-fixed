"""
Facebook Sayfa Paylasim Modulu — Graph API ile.
Playwright yerine HTTP API kullanir, boylece watcher.py icinden sorunsuz calisir.
"""

import os
import requests


def post_image_to_facebook(page_id: str = "", access_token: str = "",
                           image_path: str = "", caption: str = "",
                           user_token: str = "") -> bool:
    """
    Facebook sayfasina Graph API ile resim paylasir.
    
    Args:
        page_id: Facebook sayfa ID'si veya kullanici adi
        access_token: Page Access Token
        image_path: Yuklenecek resmin yolu
        caption: Paylasim metni
        user_token: (kullanilmiyor, geriye uyumluluk icin)
    """
    if not image_path or not os.path.exists(image_path):
        print(f"  [FB] Resim bulunamadi: {image_path}")
        return False

    if not access_token:
        print("  [FB] FB_ACCESS_TOKEN tanimli degil!")
        return False

    if not page_id:
        print("  [FB] FB_PAGE_ID tanimli degil!")
        return False

    abs_image = os.path.abspath(image_path)

    # ── Adim 1: page_id numerik degilse, sayfa ID'sini bul ──
    numeric_page_id = page_id
    if not page_id.isdigit():
        try:
            print(f"  [FB] Sayfa ID'si aliniyor ({page_id})...")
            resp = requests.get(
                f"https://graph.facebook.com/v21.0/{page_id}",
                params={"access_token": access_token, "fields": "id,name"}
            )
            data = resp.json()
            if "id" in data:
                numeric_page_id = data["id"]
                print(f"  [FB] Sayfa: {data.get('name', page_id)} (ID: {numeric_page_id})")
            else:
                error = data.get("error", {})
                print(f"  [FB] Sayfa bilgisi alinamadi: {error.get('message', data)}")
                return False
        except Exception as e:
            print(f"  [FB] Sayfa ID alma hatasi: {e}")
            return False

    # ── Adim 2: Page Access Token al (user token ile) ──
    page_token = access_token
    try:
        resp = requests.get(
            f"https://graph.facebook.com/v21.0/{numeric_page_id}",
            params={"access_token": access_token, "fields": "access_token"}
        )
        data = resp.json()
        if "access_token" in data:
            page_token = data["access_token"]
            print("  [FB] Page Access Token alindi.")
    except Exception:
        # User token ile devam et
        pass

    # ── Adim 3: Resmi yukle ve paylas ──
    url = f"https://graph.facebook.com/v21.0/{numeric_page_id}/photos"

    try:
        print(f"  [FB] Resim yukleniyor... ({os.path.basename(abs_image)})")
        with open(abs_image, "rb") as img_file:
            files = {"source": (os.path.basename(abs_image), img_file, "image/png")}
            payload = {
                "access_token": page_token,
                "published": "true",
            }
            if caption:
                payload["message"] = caption

            resp = requests.post(url, data=payload, files=files, timeout=60)

        data = resp.json()

        if "id" in data or "post_id" in data:
            post_id = data.get("post_id") or data.get("id")
            print(f"  [FB] BASARILI! Post ID: {post_id}")
            return True
        else:
            error = data.get("error", {})
            error_msg = error.get("message", str(data))
            error_code = error.get("code", "?")
            error_subcode = error.get("error_subcode", "")
            
            print(f"  [FB] HATA [{error_code}]: {error_msg}")
            
            # Yaygin hata kodlari icin rehber
            if error_code == 190:
                print("  [FB] Token suresi dolmus. Yeni token alin:")
                print("       developers.facebook.com → Graph API Explorer → Generate Token")
            elif error_code == 200:
                print("  [FB] Yetki eksik. pages_manage_posts izni gerekli.")
            elif error_code == 10:
                print("  [FB] Uygulama izni eksik veya app review gerekli.")
            
            return False

    except requests.exceptions.Timeout:
        print("  [FB] HATA: Istek zaman asimina ugradi (60s)")
        return False
    except requests.exceptions.ConnectionError:
        print("  [FB] HATA: Baglanti hatasi - internet baglantisinizi kontrol edin.")
        return False
    except Exception as e:
        print(f"  [FB] HATA: Beklenmeyen hata: {e}")
        return False
