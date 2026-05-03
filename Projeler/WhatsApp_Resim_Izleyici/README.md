# 📸 WhatsApp Resim İzleyici

WhatsApp Web'deki belirtilen grubu izler, yeni resim geldiğinde otomatik indirir ve e-posta ile bildirim gönderir.

## 🏗️ Nasıl Çalışır

```
WhatsApp Web (Tarayıcı)
    ↓ Playwright ile otomatik kontrol
"piyasa grubu" grubunu izle
    ↓ Yeni resim tespit et
Resmi indir (canvas / download butonu)
    ↓ SHA-256 hash ile deduplikasyon
Gmail SMTP ile e-posta gönder
    ↓ Resim ek olarak eklenir
📧 Bildirim e-postası alıcıya ulaşır
```

## ⚡ Kurulum

### 1. Bağımlılıkları kur
```bash
cd Projeler/WhatsApp_Resim_Izleyici
pip install -r requirements.txt
playwright install chromium
```

### 2. Yapılandırma
```bash
# .env dosyasını oluştur
copy .env.example .env
# Değerleri düzenle (aşağıya bak)
```

### 3. Gmail App Password oluştur
1. **Google Hesabınız** → myaccount.google.com
2. **Güvenlik** → **2 Adımlı Doğrulama** açık olmalı
3. **Uygulama Şifreleri** → Yeni şifre oluştur (Mail - Windows Computer)
4. 16 haneli şifreyi `.env` dosyasındaki `SMTP_PASSWORD` alanına yapıştırın

### 4. `.env` dosyası örneği
```env
SMTP_EMAIL=benimmail@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop
NOTIFY_EMAIL=bildirim@email.com
WHATSAPP_GROUP_NAME=piyasa grubu
CHECK_INTERVAL=10
DOWNLOAD_DIR=./downloads
```

## 🚀 Çalıştırma

### İlk Çalıştırma (QR taratma gerekli)
```bash
python watcher.py
```
- Tarayıcı açılacak ve WhatsApp Web yüklenecek
- Telefonunuzdan QR kodu tarayın
- Oturum bilgileri `whatsapp_session/` klasörüne kaydedilir
- Sonraki çalışmalarda QR taratmanız gerekmez

### Sonraki Çalıştırmalar
```bash
# Normal (tarayıcı görünür)
python watcher.py

# Arka planda (headless — QR taratıldıktan sonra)
python watcher.py --headless
```

## 📂 Dosya Yapısı

```
WhatsApp_Resim_Izleyici/
├── watcher.py           ← Ana izleyici script
├── email_sender.py      ← Gmail SMTP ile e-posta gönderim
├── requirements.txt     ← Python bağımlılıkları
├── .env.example         ← Yapılandırma şablonu
├── .env                 ← Gerçek yapılandırma (gitignore)
├── .gitignore
├── downloads/           ← İndirilen resimler (otomatik oluşur)
├── whatsapp_session/    ← Tarayıcı oturum verileri (gitignore)
└── seen_hashes.json     ← İşlenmiş resim hash'leri
```

## 🔄 Çalışma Mantığı

1. **Başlangıç:** Playwright ile Chromium açılır, WhatsApp Web'e gidilir
2. **Oturum:** Kaydedilmiş session varsa direkt giriş, yoksa QR kodu bekler
3. **Navigasyon:** Arama kutusuna grup adı yazılır, grup bulunup tıklanır
4. **İlk Tarama:** Mevcut tüm resimler "görülmüş" olarak işaretlenir (spam önleme)
5. **İzleme Döngüsü:** Her X saniyede:
   - Sohbetin en altına scroll edilir
   - Yeni resim mesajları taranır
   - Yeni resim varsa indirilir
   - SHA-256 hash ile deduplikasyon yapılır
   - E-posta ile gönderilir
6. **Ctrl+C** ile durdurulur

## ❌ Sorun Giderme

| Sorun | Çözüm |
|-------|-------|
| QR kodu tarayamıyorum | `whatsapp_session/` klasörünü silin, tekrar çalıştırın |
| Grup bulunamıyor | `.env`'deki `WHATSAPP_GROUP_NAME` tam eşleşmeli olmalı |
| E-posta gönderilemiyor | Gmail App Password'u kontrol edin, 2FA açık olmalı |
| Resim indirilemedi | WhatsApp Web güncelleme yapmış olabilir, selectors güncellenebilir |
| Headless çalışmıyor | Önce normal modda QR taratın, sonra headless kullanın |
