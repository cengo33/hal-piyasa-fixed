import os
import subprocess
import sys
import time
import threading
from datetime import datetime
from dotenv import load_dotenv, set_key
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import imageio_ffmpeg
import shutil

# .env yükle
ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(ENV_PATH)

app = Flask(__name__)
CORS(app)

# Global Durum
state = {
    "username": os.getenv("TIKTOK_USERNAME", "").strip("@"),
    "stream_key": os.getenv("FACEBOOK_STREAM_KEY", ""),
    "rtmp_url": os.getenv("FACEBOOK_RTMP_URL", "rtmps://live-api-s.facebook.com:443/rtmp/"),
    "bitrate": int(os.getenv("STREAM_BITRATE", "1500")),
    "resolution": os.getenv("STREAM_RESOLUTION", "720x1280"), # 720x1280, 1280x720, original
    "status": "STOPPED", # STOPPED, IDLE, CHECKING, STREAMING
    "status_text": "Sistem Durduruldu",
    "uptime_start": None,
    "logs": [],
    "should_restart": False,
    "is_active": False
}

def add_log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    state["logs"].append(f"[{timestamp}] {msg}")
    if len(state["logs"]) > 50:
        state["logs"].pop(0)
    print(f"[{timestamp}] {msg}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preview.jpg')
def get_preview():
    import os
    from flask import send_file
    preview_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "preview.jpg")
    if os.path.exists(preview_path):
        return send_file(preview_path, mimetype='image/jpeg')
    else:
        return "", 404

@app.route('/api/status')
def get_status():
    uptime = "00:00:00"
    if state["uptime_start"]:
        diff = datetime.now() - state["uptime_start"]
        uptime = str(diff).split(".")[0]
    
    return jsonify({
        "username": state["username"],
        "stream_key": state["stream_key"],
        "rtmp_url": state["rtmp_url"],
        "bitrate": state["bitrate"],
        "resolution": state["resolution"],
        "status": state["status"],
        "status_text": state["status_text"],
        "uptime": uptime,
        "logs": state["logs"],
        "is_active": state["is_active"]
    })

@app.route('/api/settings', methods=['POST'])
def save_settings():
    data = request.json
    state["username"] = data.get("username", state["username"])
    state["stream_key"] = data.get("stream_key", state["stream_key"])
    state["rtmp_url"] = data.get("rtmp_url", state["rtmp_url"])
    state["bitrate"] = int(data.get("bitrate", state["bitrate"]))
    state["resolution"] = data.get("resolution", state["resolution"])
    
    # .env dosyasına kaydet
    set_key(ENV_PATH, "TIKTOK_USERNAME", state["username"])
    set_key(ENV_PATH, "FACEBOOK_STREAM_KEY", state["stream_key"])
    set_key(ENV_PATH, "FACEBOOK_RTMP_URL", state["rtmp_url"])
    set_key(ENV_PATH, "STREAM_BITRATE", str(state["bitrate"]))
    set_key(ENV_PATH, "STREAM_RESOLUTION", state["resolution"])
    
    add_log(f"Ayarlar güncellendi: @{state['username']} | {state['bitrate']}k | {state['resolution']}")
    state["should_restart"] = True
    return jsonify({"status": "ok"})

@app.route('/api/start', methods=['POST'])
def start_stream():
    state["is_active"] = True
    state["should_restart"] = True
    add_log("Yayın aktarımı BAŞLATILDI.")
    return jsonify({"status": "ok"})

@app.route('/api/stop', methods=['POST'])
def stop_stream():
    state["is_active"] = False
    state["should_restart"] = True
    add_log("Yayın aktarımı DURDURULDU.")
    return jsonify({"status": "ok"})

@app.route('/manifest.json')
def get_manifest():
    return jsonify({
        "name": "Antigravity Restreamer",
        "short_name": "Restreamer",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0b0f19",
        "theme_color": "#0b0f19",
        "icons": [
            {
                "src": "/icon.svg",
                "sizes": "192x192 512x512",
                "type": "image/svg+xml",
                "purpose": "any maskable"
            }
        ]
    })

@app.route('/sw.js')
def get_sw():
    sw_content = """
self.addEventListener('install', function(e) {
    self.skipWaiting();
});
self.addEventListener('fetch', function(e) {
    // network only, no cache for live dash
});
"""
    return app.response_class(sw_content, mimetype='application/javascript')

@app.route('/icon.svg')
def get_icon():
    svg_content = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><rect width="512" height="512" rx="100" fill="#0b0f19"/><circle cx="256" cy="256" r="150" stroke="#3b82f6" stroke-width="40" fill="none"/><circle cx="256" cy="256" r="60" fill="#10b981"/></svg>'
    return app.response_class(svg_content, mimetype='image/svg+xml')


def restream_loop():
    global state
    
    # FFmpeg hazırlığı
    try:
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as e:
        add_log(f"FFmpeg hatası: {e}")
        return

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    temp_ffmpeg_dir = os.path.join(BASE_DIR, "temp_ffmpeg")
    if not os.path.exists(temp_ffmpeg_dir):
        os.makedirs(temp_ffmpeg_dir)
    
    temp_ffmpeg_exe = os.path.join(temp_ffmpeg_dir, "ffmpeg.exe")
    if not os.path.exists(temp_ffmpeg_exe):
        shutil.copy2(ffmpeg_exe, temp_ffmpeg_exe)
    
    os.environ["PATH"] = temp_ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
    COOKIE_FILE = os.path.join(BASE_DIR, "cookies.txt")

    while True:
        state["should_restart"] = False
        user = state["username"]
        key = state["stream_key"]
        rtmp = state["rtmp_url"]
        bitrate = state["bitrate"]
        res = state["resolution"]
        
        if not state["is_active"]:
            state["status"] = "STOPPED"
            state["status_text"] = "Yayın Durduruldu (Başlatılması Bekleniyor)"
            time.sleep(2)
            continue

        if not user or not key:
            state["status"] = "IDLE"
            state["status_text"] = "Yapılandırma Bekleniyor"
            time.sleep(5)
            continue

        state["status"] = "CHECKING"
        state["status_text"] = f"@{user} kontrol ediliyor..."
        add_log(f"@{user} için yayın kontrol ediliyor...")

        ytdlp_command = [
            sys.executable, "-m", "yt_dlp",
            "--no-warnings",
            "--socket-timeout", "15",
            "-f", "flv-hd/flv-sd/best",
            "-o", "-",
            f"https://www.tiktok.com/@{user}/live"
        ]
        
        if os.path.exists(COOKIE_FILE) and os.path.getsize(COOKIE_FILE) > 10:
            ytdlp_command.insert(3, "--cookies")
            ytdlp_command.insert(4, COOKIE_FILE)
        
        # Filtreleri ayarla
        if res == "720x1280":
            vf = "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2"
        elif res == "1280x720":
            vf = "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2"
        else:
            vf = "null"

        facebook_target = f"{rtmp}{key}"
        preview_path = os.path.join(BASE_DIR, "preview.jpg")
        
        # FFmpeg komutu (Facebook'a göndermek için)
        ffmpeg_command = [
            temp_ffmpeg_exe,
            '-hide_banner',
            '-thread_queue_size', '512',
            '-use_wallclock_as_timestamps', '1',
            '-probesize', '10M',
            '-analyzeduration', '10M',
            '-i', '-',
            '-vf', f"{vf},fps=30",
            '-c:v', 'libx264',
            '-preset', 'superfast',
            '-b:v', f'{bitrate}k',
            '-maxrate', f'{bitrate}k',
            '-bufsize', f'{bitrate*2}k',
            '-pix_fmt', 'yuv420p',
            '-g', '60',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-ar', '44100',
            '-f', 'flv',
            '-flvflags', 'no_duration_filesize',
            '-fflags', '+genpts+igndts',
            '-threads', '0',
            facebook_target,
            # Önizleme için ikinci çıktı
            '-y',
            '-vf', 'scale=-2:480',
            '-update', '1',
            '-r', '1/5',
            '-f', 'image2',
            preview_path
        ]

        try:
            process_ytdlp = subprocess.Popen(ytdlp_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process_ffmpeg = subprocess.Popen(ffmpeg_command, stdin=process_ytdlp.stdout, stderr=subprocess.PIPE)
            process_ytdlp.stdout.close()

            state["status"] = "STREAMING"
            state["status_text"] = "Yayında!"
            state["uptime_start"] = datetime.now()
            add_log(f"Aktarım başladı: @{user} -> Facebook")

            last_frame_time = [time.time()]
            process_active = [True]

            def watchdog():
                while process_active[0]:
                    if time.time() - last_frame_time[0] > 30:
                        add_log("Uyarı: 30 sn'dir veri alınamıyor (Donma Tespit Edildi)! Sistem yeniden başlatılıyor...")
                        try:
                            process_ffmpeg.kill()
                            process_ytdlp.kill()
                        except:
                            pass
                        break
                    time.sleep(2)

            watchdog_thread = threading.Thread(target=watchdog, daemon=True)
            watchdog_thread.start()

            while process_ffmpeg.poll() is None:
                if state["should_restart"]:
                    add_log("Yeniden başlatma sinyali alındı...")
                    break
                
                line = process_ffmpeg.stderr.readline()
                if line:
                    line_str = line.decode('utf-8', errors='ignore').strip()
                    if "frame=" in line_str:
                        last_frame_time[0] = time.time()
                        # Frame bilgisini konsola bas
                        print(f"FFMPEG: {line_str}")
                    else:
                        add_log(f"FFMPEG: {line_str}")

            process_active[0] = False
            
            try:
                process_ffmpeg.kill()
                process_ytdlp.kill()
            except:
                pass
            
            state["status"] = "IDLE"
            state["uptime_start"] = None
            
            if state["should_restart"]:
                state["status_text"] = "Yeniden Başlatılıyor..."
                add_log("Sistem kullanıcı isteğiyle yeniden başlatılıyor...")
                time.sleep(2)
            else:
                state["status_text"] = "Yayın Kesildi / Beklemede"
                add_log("Yayın koptu veya sonlandı. 10 saniye sonra tekrar denenecek...")
                time.sleep(10)

        except Exception as e:
            state["status"] = "IDLE"
            state["status_text"] = f"Hata: {str(e)[:20]}"
            add_log(f"Beklenmedik kritik hata: {e}")
            time.sleep(10)

if __name__ == '__main__':
    # Flask'ı ayrı bir thread'de başlat
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False))
    flask_thread.daemon = True
    flask_thread.start()
    
    add_log("Dashboard http://localhost:5000 adresinde başlatıldı.")
    
    # Restream döngüsünü ana thread'de başlat
    restream_loop()
