# Kie AI YouTube Otomasyonu

Bu proje, her gün otomatik olarak Kie AI üzerinden video üretir ve belirlenen YouTube kanalına yükler.

## 🚀 Kurulum

1. **Bağımlılıkları Yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

2. **API Anahtarlarını Ayarlayın:**
   - `.env.example` dosyasını `.env` olarak kopyalayın ve `KIE_AI_API_KEY` değerini girin.
   - [Google Cloud Console](https://console.cloud.google.com/) üzerinden bir proje oluşturun ve **YouTube Data API v3**'ü etkinleştirin.
   - OAuth 2.0 istemci kimliği oluşturun ve JSON dosyasını indirin. İsmini `credentials.json` yaparak bu klasöre koyun.

3. **Çalıştırın:**
   ```bash
   python main.py
   ```
   *İlk çalıştırmada tarayıcı üzerinden YouTube hesabınıza giriş yapmanız istenecektir. Giriş yaptıktan sonra `token.json` dosyası oluşacak ve sonraki çalıştırmalar otomatik olacaktır.*

## 📂 Yapı

- `main.py`: Ana orkestratör ve zamanlayıcı.
- `core/kie_client.py`: Kie AI API etkileşimi.
- `core/youtube_publisher.py`: YouTube API etkileşimi.
- `temp/`: Geçici olarak indirilen videoların tutulduğu yer.

## 📅 Zamanlama

Varsayılan olarak her gün saat **10:00**'da çalışacak şekilde ayarlanmıştır. `main.py` içindeki `schedule` ayarını değiştirerek saati güncelleyebilirsiniz.
