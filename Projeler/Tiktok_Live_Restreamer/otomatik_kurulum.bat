@echo off
title TikTok Live Restreamer - Otomatik Kurulum
color 0A

echo ========================================================
echo        TIKTOK LIVE RESTREAMER - KURULUM SIHIRBAZI
echo ========================================================
echo.
echo Bu islem yeni bilgisayarda gerekli tum Python modullerini 
echo ve tarayici altyapisini otomatik olarak kuracaktir.
echo.

:: Python kontrolü
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [HATA] Python bu bilgisayarda yuklu degil veya PATH'e eklenmemis!
    echo Lutfen python.org adresinden Python'u indirin ve kurarken 
    echo "Add Python to PATH" kutucugunu ISARETLEYIN.
    echo.
    pause
    exit /b
)

echo [1/4] Python surumu kontrol edildi, basarili.
echo.

echo [2/4] Pip (Paket Yoneticisi) guncelleniyor...
python -m pip install --upgrade pip
echo.

echo [3/4] Gerekli Python kutuphaneleri (requirements.txt) yukleniyor...
pip install -r requirements.txt
echo.

echo [4/4] Playwright tarayicilari (Chromium) yukleniyor...
playwright install chromium
echo.

echo ========================================================
echo KURULUM TAMAMLANDI! 
echo ========================================================
echo Artik kisayola cift tiklayarak veya 'python main.py' 
echo komutu ile projeyi baslatabilirsiniz.
echo.
pause
