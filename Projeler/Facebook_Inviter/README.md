# Facebook Inviter AI 🤖

Bu araç, Facebook sayfalarınızdaki paylaşımlara etkileşim veren (beğenen, kalp atan vb.) ancak sayfanızı henüz takip etmeyen kişileri otomatik olarak sayfanıza davet eder.

## Özellikler
- **Otomatik Davet**: Gönderi bazlı veya sayfa bazlı davet gönderme.
- **Modern Dashboard**: Şık, karanlık mod destekli ve canlı log takibi.
- **Playwright Entegrasyonu**: Gerçek tarayıcı simülasyonu ile güvenli işlem.
- **Oturum Yönetimi**: `fb_session` klasörü sayesinde her seferinde giriş yapmanıza gerek kalmaz.

## Kurulum
1. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

2. Uygulamayı başlatın:
   ```bash
   python main.py
   ```

3. Tarayıcıda `http://localhost:5000` adresine gidin.

## Nasıl Kullanılır?
1. Dashboard üzerindeki input alanına davet göndermek istediğiniz gönderinin URL'sini yapıştırın.
2. "Start Inviting" butonuna basın.
3. Eğer ilk kez kullanıyorsanız, açılan tarayıcı penceresinden Facebook girişinizi yapın.
4. Bot, etkileşim listesini açacak ve "Davet Et" (veya "Invite") butonlarını tek tek tıklayacaktır.

---
**Geliştiren:** Antigravity AI
