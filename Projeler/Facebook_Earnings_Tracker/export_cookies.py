import os
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_DIR = os.path.join(BASE_DIR, "fb_session")

def export_state():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=True
        )
        browser.storage_state(path="state.json")
        browser.close()
        print("Durum başarıyla state.json dosyasına aktarıldı!")

if __name__ == "__main__":
    export_state()
