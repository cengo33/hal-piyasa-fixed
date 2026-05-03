"""
Facebook paylasim testi — downloads klasorundan bir resim alip Facebook'a yukler.
"""
import os
from dotenv import load_dotenv
from facebook_poster import post_image_to_facebook

load_dotenv()

FB_PAGE_ID = os.getenv("FB_PAGE_ID", "halkompleksi33")
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN", "")

# downloads klasorundeki en son resmi bul
downloads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")
files = sorted([f for f in os.listdir(downloads_dir) if f.endswith(".png")])

if not files:
    print("Hic resim bulunamadi!")
    exit(1)

latest = os.path.join(downloads_dir, files[-1])
print(f"Test resmi: {latest}")
print(f"FB Page: {FB_PAGE_ID}")
print(f"Token: {FB_ACCESS_TOKEN[:20]}..." if FB_ACCESS_TOKEN else "Token YOK!")
print()

caption = "Piyasa guncelleme - Test"
result = post_image_to_facebook(
    page_id=FB_PAGE_ID,
    access_token=FB_ACCESS_TOKEN,
    image_path=latest,
    caption=caption,
    user_token=FB_ACCESS_TOKEN,
)

print(f"\nSonuc: {'BASARILI' if result else 'BASARISIZ'}")
