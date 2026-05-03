# TikTok to Facebook Page Auto-Poster (Tarım İçerikleri)

Bu proje, TikTok'tan (özellikle tarım ile ilgili) videoları filigransız (watermark olmadan) indirip otomatik olarak bir Facebook Sayfasına yüklemenizi sağlar.

## Kurulum

1. Python yüklü olduğundan emin olun.
2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. `.env.example` dosyasının adını `.env` olarak değiştirin ve içine Facebook Page bilgilerinizi girin:
   - `FACEBOOK_PAGE_ID`: Facebook sayfanızın ID'si.
   - `FACEBOOK_PAGE_ACCESS_TOKEN`: Sayfanızı yönetmek için oluşturduğunuz Graph API erişim belirteci (Access Token).

## Kullanım

Projeyi başlatmak için ana betiği çalıştırın:
```bash
python main.py
```

Sizden bir TikTok URL'si isteyecektir. İlgili videonun URL'sini yapıştırın. İsteğe bağlı olarak Facebook'ta paylaşılırken kullanılacak özel bir açıklama girebilirsiniz (boş bırakırsanız videonun kendi başlığı ve varsayılan tarım etiketleri kullanılır).

## Nasıl Çalışır?
1. **tiktok_downloader.py**: `yt-dlp` kütüphanesini kullanarak TikTok videosunu filigransız olarak en yüksek kalitede indirir ve `downloads/` klasörüne kaydeder.
2. **facebook_poster.py**: Facebook Graph API (v19.0) kullanarak indirilen videoyu sayfanıza yükler.
3. **main.py**: Tüm bu süreci yönetir ve konsol üzerinden kolay kullanım sağlar.

## Notlar
- `yt-dlp` sürekli güncellenen bir araçtır. TikTok tarafında bir değişiklik olursa ve indirmeler hata verirse, `pip install -U yt-dlp` komutuyla güncelleyebilirsiniz.
- Facebook Graph API üzerinden video yükleyebilmek için uygulamanızın `pages_manage_posts`, `pages_read_engagement` ve `pages_show_list` izinlerine sahip olması gerekmektedir.
