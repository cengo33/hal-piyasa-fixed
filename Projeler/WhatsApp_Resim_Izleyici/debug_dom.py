"""WhatsApp Web arayuzunun DOM yapisini incelemek icin debug scripti."""
import os, time
from playwright.sync_api import sync_playwright

SESSION_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "whatsapp_session")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=SESSION_DIR,
        headless=False,
        args=["--disable-blink-features=AutomationControlled"],
        viewport={"width": 1400, "height": 900},
        locale="tr-TR",
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto("https://web.whatsapp.com", wait_until="domcontentloaded")
    
    # Bekle
    time.sleep(15)
    
    # Side panel'i incele
    print("=== #side panel var mi? ===")
    side = page.query_selector('#side')
    print(f"#side: {side is not None}")
    
    print("\n=== #pane-side var mi? ===")
    pane = page.query_selector('#pane-side')
    print(f"#pane-side: {pane is not None}")
    
    print("\n=== Tum contenteditable elementler ===")
    editables = page.query_selector_all('div[contenteditable="true"]')
    for i, el in enumerate(editables):
        attrs = page.evaluate("""
            (el) => {
                const a = {};
                for (let attr of el.attributes) a[attr.name] = attr.value;
                return JSON.stringify(a);
            }
        """, el)
        print(f"  [{i}] {attrs}")
    
    print("\n=== Tum role=textbox elementler ===")
    textboxes = page.query_selector_all('[role="textbox"]')
    for i, el in enumerate(textboxes):
        attrs = page.evaluate("""
            (el) => {
                const a = {};
                for (let attr of el.attributes) a[attr.name] = attr.value;
                a['_tag'] = el.tagName;
                a['_parentId'] = el.parentElement?.id || '';
                return JSON.stringify(a);
            }
        """, el)
        print(f"  [{i}] {attrs}")
    
    print("\n=== data-icon elementler (ilk 10) ===")
    icons = page.query_selector_all('span[data-icon]')
    for i, el in enumerate(icons[:10]):
        icon_name = el.get_attribute('data-icon')
        print(f"  [{i}] data-icon=\"{icon_name}\"")
    
    print("\n=== aria-label iceren butonlar (ilk 10) ===")
    buttons = page.query_selector_all('button[aria-label], div[aria-label]')
    for i, el in enumerate(buttons[:15]):
        label = el.get_attribute('aria-label')
        tag = el.evaluate("el => el.tagName")
        print(f"  [{i}] <{tag}> aria-label=\"{label}\"")
    
    browser.close()
    print("\nBitti!")
