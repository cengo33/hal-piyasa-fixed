"""Facebook Playwright post testi."""
from facebook_poster import post_image_to_facebook

result = post_image_to_facebook(
    page_id="halkompleksi33",
    image_path="downloads/wa_20260419_133606_8.png",
    caption="Piyasa guncelleme",
)
print(f"\nSonuc: {'BASARILI' if result else 'BASARISIZ'}")
