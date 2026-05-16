import os
import time
import pandas as pd
from playwright.sync_api import sync_playwright

SESSION_DIR = r"c:\Users\1\Desktop\Antigravity\Projeler\WhatsApp_Resim_Izleyici\whatsapp_session"
GROUP_NAME = "halder mersin komisyoncuları"
OUTPUT_FILE = r"c:\Users\1\Desktop\Antigravity\Projeler\WhatsApp_Resim_Izleyici\komisyoncular.xlsx"

def main():
    print("Script başlatıldı...")
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=False,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox", "--disable-dev-shm-usage"],
            viewport={"width": 1400, "height": 900},
            locale="tr-TR",
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://web.whatsapp.com", wait_until="domcontentloaded")
        
        print("WhatsApp Web yükleniyor... Eğer ekranda QR kod görürseniz lütfen telefonunuzdan okutun.")
        try:
            page.wait_for_selector('#side', timeout=300000)
            print("WhatsApp başarıyla açıldı!")
        except Exception:
            print("WhatsApp Web yüklenemedi veya karekod taranmadı.")
            browser.close()
            return
            
        print("\n=======================================================")
        print("*** DİKKAT: WHATSAPP GÜNCELLEMESİ NEDENİYLE OTOMATİK ARAMA DEVRE DIŞI ***")
        print(f"1. Lütfen WhatsApp üzerinden '{GROUP_NAME}' grubunu KENDİNİZ BULUP TIKLAYIN.")
        print("2. Grubun üst kısmına (isim kısmına) tıklayarak sağ taraftaki GRUP BİLGİSİ panelini açın.")
        print("3. Üyeler listesinde 'Tümünü gör' (View all) varsa tıklayın.")
        print("4. Çıkan listeyi yavaşça aşağıya doğru kaydırın.")
        print("\nScript 60 saniye boyunca ekranda gördüğü tüm numaraları toplayacaktır!")
        print("=======================================================\n")
        print("Script 45 saniye boyunca ekrandaki tüm numaraları toplayacaktır.\n")
        
        numbers = set()
        for i in range(45):
            elements = page.query_selector_all('span[dir="auto"], span[title], div[role="gridcell"] span')
            for el in elements:
                text = el.inner_text().strip()
                if text.startswith("+") or text.startswith("05") or text.startswith("90"):
                    numbers.add(text)
            time.sleep(1)
            print(f"Kalan süre: {45-i} saniye | Toplanan numara sayısı: {len(numbers)}", end='\r')
            
        print(f"\nToplam {len(numbers)} numara bulundu.")
        
        if numbers:
            df = pd.DataFrame(list(numbers), columns=["Telefon"])
            df.to_excel(OUTPUT_FILE, index=False)
            print(f"Excel dosyası başarıyla oluşturuldu: {OUTPUT_FILE}")
        else:
            print("Hiç numara bulunamadı. Lütfen kaydırma işlemini doğru yaptığınızdan emin olun.")
        
        browser.close()

if __name__ == "__main__":
    main()
