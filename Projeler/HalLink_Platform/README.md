# 🚀 HalLink Platform

Mersin Hal Kompleksi için dijital ticaret ve eşleştirme platformu. Komisyoncular ve tüccarların ürün ilanı verip birbirleriyle iletişime geçmesini sağlar.

## ✨ Özellikler
- **Rol Tabanlı Kayıt:** Komisyoncu veya Tüccar olarak profil oluşturma.
- **Pazaryeri:** Aktif ürün ilanlarının listelenmesi ve filtrelenmesi.
- **WhatsApp Entegrasyonu:** Tek tıkla satıcıya ulaşma.
- **Admin Dashboard:** İstatistiklerin takibi ve ilan yönetimi.
- **Kalıcı Veritabanı:** Supabase ile güvenli ve hızlı veri depolama.

## 🛠️ Teknik Altyapı
- **Frontend:** React + Vite
- **Styling:** Vanilla CSS (Glassmorphism UI)
- **Animasyon:** Framer Motion
- **Veritabanı:** Supabase
- **Hosting:** Netlify

## 🚀 Kurulum

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/cengo33/HalLink-Platform.git
   ```
2. Bağımlılıkları yükleyin:
   ```bash
   npm install
   ```
3. `.env` dosyasını oluşturun:
   ```env
   VITE_SUPABASE_URL=your_supabase_url
   VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
   ```
4. Geliştirme modunda çalıştırın:
   ```bash
   npm run dev
   ```

## 🔐 Güvenlik Notu
Admin paneline erişim şifresi: `8888` (Admin arayüzünden değiştirilebilir).
