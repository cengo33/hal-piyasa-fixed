"""
WhatsApp Resim İzleyici — Ana Modül

WhatsApp Web'i Playwright ile açar, belirtilen kişi veya grubu izler,
yeni resim geldiğinde indirir ve e-posta ile bildirim gönderir.

Kullanım:
    python watcher.py              # Normal çalıştırma
    python watcher.py --headless   # Arka planda çalıştırma (ilk QR sonrası)

İlk Çalıştırma:
    İlk seferde WhatsApp Web'de QR kod taratmanız gerekecek.
    Oturum bilgileri kaydedilir, sonraki çalışmalarda tekrar taratmanız gerekmez.
"""

import os
import sys
import time
import hashlib
import json
import argparse
import base64
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

from email_sender import send_image_email
from facebook_poster import post_image_to_facebook

# ═══════════════════════════════════════════════════════
# Yapılandırma
# ═══════════════════════════════════════════════════════

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.yandex.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_EMAIL = os.getenv("SMTP_EMAIL", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", "")
WHATSAPP_PHONE = os.getenv("WHATSAPP_PHONE", "").strip()
GROUP_NAME = os.getenv("WHATSAPP_GROUP_NAME", "").strip()
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "10"))
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "./downloads")

# Facebook ayarlari
FB_PAGE_ID = os.getenv("FB_PAGE_ID", "")
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN", "")
FB_CAPTION = os.getenv("FB_CAPTION", "")

SESSION_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "whatsapp_session")
SEEN_HASHES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seen_hashes.json")

# İzlenecek hedefin adı (log ve e-posta için)
TARGET_LABEL = WHATSAPP_PHONE if WHATSAPP_PHONE else GROUP_NAME


def load_seen_hashes() -> set:
    if os.path.exists(SEEN_HASHES_FILE):
        with open(SEEN_HASHES_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_seen_hashes(hashes: set):
    with open(SEEN_HASHES_FILE, "w") as f:
        json.dump(list(hashes), f)


def file_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def ensure_download_dir():
    Path(DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)


def log(msg: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] {msg}"
    try:
        print(line)
    except UnicodeEncodeError:
        print(line.encode("ascii", errors="replace").decode("ascii"))


def validate_config():
    errors = []
    if not SMTP_EMAIL:
        errors.append("SMTP_EMAIL tanımlı değil")
    if not SMTP_PASSWORD:
        errors.append("SMTP_PASSWORD tanımlı değil")
    if not NOTIFY_EMAIL:
        errors.append("NOTIFY_EMAIL tanımlı değil")
    if not WHATSAPP_PHONE and not GROUP_NAME:
        errors.append("WHATSAPP_PHONE veya WHATSAPP_GROUP_NAME'den en az biri tanımlı olmalı")

    if errors:
        print("❌ Yapılandırma hataları:")
        for e in errors:
            print(f"   • {e}")
        print("\n💡 .env.example dosyasını .env olarak kopyalayıp değerleri doldurun.")
        sys.exit(1)


def wait_for_whatsapp_load(page, timeout=300000):
    """WhatsApp Web'in tamamen yuklenmesini bekler. QR taratmayi da bekler. 5 dakika timeout."""
    log("WhatsApp Web yukleniyor...")
    log("Ilk calistirmaysa telefonunuzdan QR kodu tarayin.")
    log(f"QR tarama icin {timeout // 1000} saniye bekleniyor...")

    # Tek bir combined selector ile bekle (hepsi ayni anda denenir)
    combined = ', '.join([
        'div[contenteditable="true"][data-tab="3"]',
        'div[title="Search input textbox"]',
        'header span[data-icon="search"]',
        '#side',
    ])

    try:
        page.wait_for_selector(combined, timeout=timeout)
        log("WhatsApp Web yuklendi!")
        return True
    except PlaywrightTimeout:
        log("WhatsApp Web yuklenemedi. QR kodu taradiginizdan emin olun.")
        return False


def open_search_box(page):
    """Arama kutusunu acar ve dondurur."""
    search_selectors = [
        'input[data-tab="3"]',
        'input[role="textbox"][data-tab="3"]',
        'div[contenteditable="true"][data-tab="3"]',
        'p.selectable-text[data-tab="3"]',
    ]

    # Side panel icindeki arama kutusunu bul
    for sel in search_selectors:
        try:
            box = page.wait_for_selector(sel, timeout=3000)
            if box:
                log(f"Arama kutusu bulundu: {sel}")
                return box
        except PlaywrightTimeout:
            continue

    # Yeni sohbet butonuna tikla ve arama yap
    new_chat = page.query_selector('button[aria-label="Yeni sohbet"]')
    if new_chat:
        new_chat.click()
        time.sleep(1)
        for sel in search_selectors:
            try:
                box = page.wait_for_selector(sel, timeout=3000)
                if box:
                    return box
            except PlaywrightTimeout:
                continue

    return None


def navigate_to_chat(page, search_term: str, max_retries=3) -> bool:
    """
    Belirtilen kisi veya gruba gider.
    Telefon numarasi icin birden fazla format dener.
    """
    # Telefon numarasi formatlarini hazirla
    search_variants = [search_term]
    if any(c.isdigit() for c in search_term):
        clean = search_term.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if clean not in search_variants:
            search_variants.append(clean)
        # Son 10 hane (ulke kodu olmadan)
        if len(clean) > 10:
            last10 = clean[-10:]
            if last10 not in search_variants:
                search_variants.append(last10)
        # 0 ile baslayan format
        if len(clean) > 10 and not clean[-10:].startswith("0"):
            with_zero = "0" + clean[-10:]
            if with_zero not in search_variants:
                search_variants.append(with_zero)

    for variant in search_variants:
        for attempt in range(max_retries):
            log(f"Araniyor: '{variant}' (deneme {attempt + 1}/{max_retries})")

            try:
                search_box = open_search_box(page)
                if not search_box:
                    log("Arama kutusu bulunamadi, tekrar deneniyor...")
                    time.sleep(3)
                    continue

                # Kutuyu temizle
                search_box.click()
                time.sleep(0.5)
                # Triple click ile tumu sec
                search_box.click(click_count=3)
                time.sleep(0.2)

                # type() kullan — fill() WhatsApp'in arama event'ini tetiklemiyor
                search_box.fill("")
                time.sleep(0.3)
                page.keyboard.type(variant, delay=50)
                time.sleep(3)  # Arama sonuclarinin gelmesini bekle

                # Sonuclarda bul ve tikla
                result_el = None

                # 1) span[title] ile dene
                title_selectors = [
                    f'span[title*="{variant}"]',
                ]
                if variant != search_term:
                    title_selectors.append(f'span[title*="{search_term}"]')

                for sel in title_selectors:
                    try:
                        result_el = page.wait_for_selector(sel, timeout=2000)
                        if result_el:
                            log(f"Sonuc bulundu: {sel}")
                            break
                    except PlaywrightTimeout:
                        continue

                # 2) Arama sonuc listesinden ilk ogeyi dene
                if not result_el:
                    list_selectors = [
                        'div[aria-label="Arama sonuçları."] > div > div:first-child',
                        'div[aria-label="Search results."] > div > div:first-child',
                        '#search-result-list > div > div:first-child',
                    ]
                    for sel in list_selectors:
                        try:
                            result_el = page.wait_for_selector(sel, timeout=2000)
                            if result_el:
                                log(f"Ilk arama sonucu secildi")
                                break
                        except PlaywrightTimeout:
                            continue

                # 3) Sohbet listesinden dene (arama sonucu yerine)
                if not result_el:
                    try:
                        result_el = page.wait_for_selector(
                            'div[aria-label="Sohbet listesi"] > div > div:first-child',
                            timeout=2000
                        )
                        if result_el:
                            log("Sohbet listesinden ilk sonuc secildi")
                    except PlaywrightTimeout:
                        pass

                if result_el:
                    result_el.click()
                    time.sleep(2)
                    page.keyboard.press("Escape")
                    time.sleep(0.5)
                    log(f"'{search_term}' sohbetine girildi!")
                    return True
                else:
                    log(f"'{variant}' bulunamadi.")
                    page.keyboard.press("Escape")
                    time.sleep(1)

            except Exception as e:
                log(f"Navigasyon hatasi: {e}")
                time.sleep(3)

    log(f"'{search_term}' sohbetine girilemedi.")
    return False


def get_image_elements(page) -> list:
    """Mevcut sohbetteki resim mesajlarını bulur."""
    images = []
    selectors = [
        'div[data-testid="image-thumb"] img',
        'img[src*="blob:https://web.whatsapp.com"]',
        'div[data-testid="msg-container"] img[src*="blob"]',
        'div[class*="message"] img[src*="blob:"]',
    ]

    for selector in selectors:
        elements = page.query_selector_all(selector)
        if elements:
            for el in elements:
                src = el.get_attribute("src")
                if src and "blob:" in src:
                    # Mesaj ID'si al (deduplikasyon)
                    msg_id = None
                    try:
                        msg_id = el.evaluate("""
                            (img) => {
                                let node = img;
                                for (let i = 0; i < 15; i++) {
                                    node = node.parentElement;
                                    if (!node) break;
                                    const id = node.getAttribute('data-id');
                                    if (id) return id;
                                }
                                return null;
                            }
                        """)
                    except:
                        pass

                    images.append({"src": src, "msg_id": msg_id, "element": el})
            break
    return images


def download_image(page, img_element, save_path: str) -> bool:
    """Resmi indirir — önce WhatsApp indirme butonu, sonra canvas yöntemi."""

    # ── Yöntem 1: WhatsApp indirme butonu ──
    try:
        img_element.click()
        time.sleep(2)

        dl_btn = None
        for sel in ['span[data-icon="download"]', 'div[data-testid="download"]', 'button[aria-label="Download"]']:
            try:
                dl_btn = page.wait_for_selector(sel, timeout=3000)
                if dl_btn:
                    break
            except PlaywrightTimeout:
                continue

        if dl_btn:
            with page.expect_download(timeout=15000) as dl_info:
                dl_btn.click()
            dl_info.value.save_as(save_path)
            page.keyboard.press("Escape")
            time.sleep(0.5)
            return True

        page.keyboard.press("Escape")
        time.sleep(0.5)
    except Exception:
        try:
            page.keyboard.press("Escape")
        except:
            pass

    # ── Yöntem 2: Canvas ile çıkarma ──
    try:
        data_url = page.evaluate("""
            (img) => {
                const c = document.createElement('canvas');
                c.width = img.naturalWidth || img.width;
                c.height = img.naturalHeight || img.height;
                c.getContext('2d').drawImage(img, 0, 0);
                return c.toDataURL('image/png');
            }
        """, img_element)

        if data_url and data_url.startswith("data:image"):
            b64 = data_url.split(",", 1)[1]
            with open(save_path, "wb") as f:
                f.write(base64.b64decode(b64))
            return True
    except Exception:
        pass

    # ── Yöntem 3: Element ekran görüntüsü ──
    try:
        img_element.screenshot(path=save_path)
        return True
    except Exception:
        pass

    return False


def process_new_images(page, seen_hashes: set) -> int:
    """Yeni resimleri tespit et → indir → mail gönder. Yeni resim sayısı döner."""
    ensure_download_dir()
    images = get_image_elements(page)
    if not images:
        return 0

    new_count = 0
    for i, img in enumerate(images):
        try:
            # Hash hesapla (deduplikasyon)
            key = img.get("msg_id") or img.get("src", "")
            h = hashlib.sha256(key.encode()).hexdigest()
            if h in seen_hashes:
                continue

            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(DOWNLOAD_DIR, f"wa_{ts}_{i}.png")

            log("📥 Yeni resim tespit edildi, indiriliyor...")
            ok = download_image(page, img["element"], save_path)

            if ok and os.path.exists(save_path):
                size = os.path.getsize(save_path)
                log(f"  💾 Kaydedildi: {os.path.basename(save_path)} ({size:,} bytes)")

                # İçerik hash'i
                with open(save_path, "rb") as f:
                    ch = file_hash(f.read())
                if ch in seen_hashes:
                    log("  ⏭️ Aynı içerik daha önce işlenmiş, atlanıyor.")
                    os.remove(save_path)
                    seen_hashes.add(h)
                    save_seen_hashes(seen_hashes)
                    continue

                log(f"  📧 E-posta gönderiliyor → {NOTIFY_EMAIL}...")
                email_ok = send_image_email(
                    smtp_email=SMTP_EMAIL,
                    smtp_password=SMTP_PASSWORD,
                    to_email=NOTIFY_EMAIL,
                    image_path=save_path,
                    group_name=TARGET_LABEL,
                    smtp_host=SMTP_HOST,
                    smtp_port=SMTP_PORT,
                )

                # Facebook'a paylas
                if FB_ACCESS_TOKEN:
                    log(f"  [FB] Facebook sayfasina paylasiliyor...")
                    caption = FB_CAPTION if FB_CAPTION else f"Piyasa guncelleme - {datetime.now().strftime('%d.%m.%Y %H:%M')}"
                    post_image_to_facebook(
                        page_id=FB_PAGE_ID,
                        access_token=FB_ACCESS_TOKEN,
                        image_path=save_path,
                        caption=caption,
                        user_token=FB_ACCESS_TOKEN,
                    )

                if email_ok:
                    new_count += 1

                seen_hashes.update([h, ch])
                save_seen_hashes(seen_hashes)
            else:
                log("  ❌ Resim indirilemedi.")
                seen_hashes.add(h)
                save_seen_hashes(seen_hashes)

        except Exception as e:
            log(f"  ❌ Hata: {e}")

    return new_count


def scroll_to_bottom(page):
    try:
        page.evaluate("""
            () => {
                const p = document.querySelector('#main div[role="application"]')
                       || document.querySelector('div[data-tab="8"]');
                if (p) p.scrollTop = p.scrollHeight;
            }
        """)
    except:
        pass


def main():
    parser = argparse.ArgumentParser(description="WhatsApp Resim İzleyici")
    parser.add_argument("--headless", action="store_true",
                        help="Tarayıcıyı arka planda çalıştır (ilk QR sonrası)")
    args = parser.parse_args()

    validate_config()
    ensure_download_dir()

    search_term = WHATSAPP_PHONE if WHATSAPP_PHONE else GROUP_NAME

    print()
    print("=" * 52)
    print("  WhatsApp Resim Izleyici")
    print("=" * 52)
    print(f"  Hedef:     {search_term}")
    print(f"  Bildirim:  {NOTIFY_EMAIL}")
    print(f"  Aralik:    {CHECK_INTERVAL} saniye")
    print(f"  Headless:  {'Evet' if args.headless else 'Hayir'}")
    print("=" * 52)
    print()

    seen_hashes = load_seen_hashes()
    log(f"📂 {len(seen_hashes)} daha önce işlenmiş hash yüklendi.")

    with sync_playwright() as p:
        log("🌐 Tarayıcı başlatılıyor...")
        browser = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=args.headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
            viewport={"width": 1400, "height": 900},
            locale="tr-TR",
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        log("📱 WhatsApp Web açılıyor...")
        page.goto("https://web.whatsapp.com", wait_until="domcontentloaded")

        if not wait_for_whatsapp_load(page, timeout=120000):
            browser.close()
            sys.exit(1)

        time.sleep(3)
        if not navigate_to_chat(page, search_term):
            browser.close()
            sys.exit(1)

        # Mevcut resimleri "görülmüş" işaretle (spam önleme)
        log("🔄 Mevcut resimler taranıyor...")
        existing = get_image_elements(page)
        for img in existing:
            key = img.get("msg_id") or img.get("src", "")
            seen_hashes.add(hashlib.sha256(key.encode()).hexdigest())
        save_seen_hashes(seen_hashes)
        log(f"  ✅ {len(existing)} mevcut resim işaretlendi (bunlar için mail gitmeyecek).")

        log(f"👁️ İzleme başladı — her {CHECK_INTERVAL} saniyede kontrol.")
        log("   Ctrl+C ile durdurabilirsiniz.")
        print()

        total_sent = 0
        checks = 0

        try:
            while True:
                checks += 1
                scroll_to_bottom(page)
                time.sleep(1)

                n = process_new_images(page, seen_hashes)
                if n > 0:
                    total_sent += n
                    log(f"📊 {n} yeni resim gönderildi. (Toplam: {total_sent})")

                if checks % 30 == 0:
                    log(f"💤 İzleme devam ediyor... ({checks} kontrol, {total_sent} gönderim)")

                time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print()
            log(f"🛑 Durduruldu. Toplam gönderim: {total_sent}")
        finally:
            browser.close()
            log("🌐 Tarayıcı kapatıldı.")


if __name__ == "__main__":
    main()
