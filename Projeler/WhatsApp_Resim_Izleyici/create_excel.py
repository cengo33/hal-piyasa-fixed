import pandas as pd
import os

data = [
    {
        "Firma Adı": "Yağız Yaş Meyve Sebze İthalat İhracat",
        "Telefon": "+90 545 549 77 44 / +90 542 422 43 38",
        "E-posta": "info@yagizexport.com",
        "Web Sitesi": "yagizexport.com",
        "Adres": "İhsaniye Mah. Zeytinlibahçe Cad. Kapı No:120 Daire No:12, Akdeniz / Mersin"
    },
    {
        "Firma Adı": "ALN Narenciye",
        "Telefon": "+90 544 455 64 10",
        "E-posta": "ekselansce.cml@gmail.com",
        "Web Sitesi": "alnnarenciye.com",
        "Adres": "Cami Şerif Mah. 5232 Sk. Buğdaycı İş Merkezi No:14 İç Kapı No:18, Akdeniz / Mersin"
    },
    {
        "Firma Adı": "Asi Fruit Vegetables",
        "Telefon": "+90 530 065 10 18 / +90 535 500 87 38",
        "E-posta": "export@asifruit.com",
        "Web Sitesi": "asifruit.com",
        "Adres": "Çay Mah. Abdi İpekçi Cad. No:98, Akdeniz / Mersin"
    },
    {
        "Firma Adı": "Akkeser Ltd. Şti.",
        "Telefon": "+90 536 543 66 77",
        "E-posta": "oguzhan@akkeser.com",
        "Web Sitesi": "akkeser.com",
        "Adres": "Limonluk Mah. Ali Kaya Mutlu Cad. Arma Plaza No:9/A Kat:11/23 Yenişehir/Mersin"
    },
    {
        "Firma Adı": "Biberciler Narenciye & Yaş Meyve, Sebze İhracatı",
        "Telefon": "+90 324 646 33 42",
        "E-posta": "export@biberciler.com.tr",
        "Web Sitesi": "biberciler.com.tr",
        "Adres": "Adnan Menderes Mah., İnönü Blv., Akdeniz/Mersin"
    },
    {
        "Firma Adı": "Deha Tarım",
        "Telefon": "-",
        "E-posta": "-",
        "Web Sitesi": "dehatarim.com",
        "Adres": "Mersin"
    },
    {
        "Firma Adı": "Polat Narenciye",
        "Telefon": "+90 324 235 2716 / +90 324 646 41 00",
        "E-posta": "info@polatnarenciye.com",
        "Web Sitesi": "polatnarenciye.com.tr",
        "Adres": "Toptancı Hal Kompleksi Komisyoncular Bölümü F-1 Blok No:21, Akdeniz / Mersin"
    },
    {
        "Firma Adı": "Kılıç Tarım Gıda Hafriyat Petrol",
        "Telefon": "+90 532 760 56 72",
        "E-posta": "kilic@kilictarim.com",
        "Web Sitesi": "-",
        "Adres": "Ören Mh. Kadirler Cad. No:6, Anamur / Mersin"
    },
    {
        "Firma Adı": "Karanlar Petrol Ürünleri (Tarım/İhracat)",
        "Telefon": "+90 532 635 88 41",
        "E-posta": "karanlarpetrol@hotmail.com",
        "Web Sitesi": "-",
        "Adres": "Ören Beldesi Kuzeyyurt Mah. Mersin Antalya Bulvarı No:19, Anamur / Mersin"
    }
]

df = pd.DataFrame(data)
output_file = "mersin_sebze_meyve_ihracatcilari_guncel.xlsx"
df.to_excel(output_file, index=False)

print(f"Excel dosyası başarıyla oluşturuldu: {output_file}")
