# Facebook Earnings Tracker

Bu proje, Facebook Professional Dashboard üzerinden kazanç bilgilerinizi çekerek günde 4 kez Telegram'a bildirim gönderen bir otomasyondur.

## Özellikler
- **Playwright Otomasyonu:** Facebook üzerinden kazanç sayfasına tarayıcı ile bağlanır ve veriyi çeker.
- **Telegram Entegrasyonu:** Çekilen veriyi tanımlı Telegram botunuz aracılığıyla size mesaj atar.
- **Zamanlayıcı (Scheduler):** Script arka planda çalışarak günde 4 defa (örneğin 06:00, 12:00, 18:00, 23:59 gibi) bu işlemi otomatik yapar.
- **Session (Oturum) Kaydı:** Her seferinde tekrar şifre girmemek için tarayıcı oturumu kaydedilir.

## Kurulum
1. `pip install -r requirements.txt`
2. İlk kurulumda `.env` dosyasını yapılandırın.
3. Telegram bot bilgilerinizi `.env` içerisine yazın.
