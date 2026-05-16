# ğŸš€ Deploy Registry â€” Deployment KayÄ±t Defteri

Bu dosya, Railway'e deploy edilmiÅŸ projelerin kayÄ±t defteridir.

---

## Aktif Deployment'lar

| Proje | Railway Proje ID | Service ID | Ortam | Tip | Durum |
|-------|-----------------|------------|-------|-----|-------|
| _(Ä°lk deploy'unuzda buraya ekleyin)_ | | | production | | |

---

## Deploy Bilgileri NasÄ±l Eklenir?

Her baÅŸarÄ±lÄ± deploy sonrasÄ±nda ÅŸu bilgileri ekleyin:

```markdown
| Proje_AdÄ± | prj_xxxxx | srv_xxxxx | production | Worker/Cron | âœ… Aktif |
```

### Gerekli Bilgiler:
- **Railway Proje ID:** GraphQL API'den veya Railway dashboard'dan alÄ±nÄ±r
- **Service ID:** AynÄ± projede birden fazla servis olabilir
- **Ortam:** `production` veya `staging`
- **Tip:** `Worker` (7/24), `Cron` (zamanlanmÄ±ÅŸ), `Web` (HTTP)
- **Durum:** ⏸️ Durduruldu, â¸ï¸ Durduruldu, âŒ KapatÄ±ldÄ±

---

## ArÅŸiv (KapatÄ±lmÄ±ÅŸ/TaÅŸÄ±nmÄ±ÅŸ)

| Proje | KapatÄ±lma Tarihi | Neden |
|-------|-----------------|-------|
| _(GerektiÄŸinde buraya taÅŸÄ±yÄ±n)_ | | |

### Tiktok_Facebook_Poster
- **Platform:** railway
- **Railway Project ID:** 1ec5d195-23bd-4af7-a784-c4fa7952521b
- **Service ID:** b03e168f-1c6a-4563-867b-1388f8c0da8b
- **Environment ID:** 0ae38f4b-61dc-4d31-8d1a-0b37f11d0717
- **GitHub Repo:** Yok (Railway CLI ile Lokalden Upload)
- **Lokal Klasör:** Projeler/Tiktok_Facebook_Poster/
- **Start Komutu:** python worker.py
- **Son Deploy:** 2026-05-03
- **Durum:** ⏸️ Durduruldu

