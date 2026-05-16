import os
import subprocess
import threading
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import re
import imageio_ffmpeg
import ctypes

# Windows DPI ölçekleme sorunlarını (125%, 150%) düzeltir. gdigrab gerçek piksellerle çalışır.
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

CONFIG_FILE = "config.json"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Antigravity - Ekran Canlı Yayıncısı")
        self.root.geometry("450x650")
        self.root.configure(bg="#0f172a")
        
        # Varsayılan ekran seçim boyutları
        self.region = {"x": 0, "y": 0, "w": 1280, "h": 720}
        self.process = None
        self.config = {"rtmp_url": "rtmps://live-api-s.facebook.com:443/rtmp/", "stream_key": "", "audio_device": "Sistem Sesi (Tarayıcı vb. Tüm Sesler)"}
        
        self.load_config()
        self.build_ui()
        
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                self.config.update(json.load(f))
                
    def save_config(self):
        self.config["stream_key"] = self.entry_key.get().strip()
        self.config["rtmp_url"] = self.entry_url.get().strip()
        self.config["audio_device"] = self.combo_audio.get()
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.config, f)

    def get_audio_devices(self):
        devices = ["Sistem Sesi (Tarayıcı vb. Tüm Sesler)", "Sessiz (Sadece Görüntü)"]
        try:
            exe = imageio_ffmpeg.get_ffmpeg_exe()
            res = subprocess.run([exe, '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy'], capture_output=True, text=True, encoding='utf-8', errors='replace', creationflags=subprocess.CREATE_NO_WINDOW)
            for line in res.stderr.split('\n'):
                if '(audio)' in line:
                    match = re.search(r'"([^"]+)"\s+\(audio\)', line)
                    if match:
                        devices.append(match.group(1))
        except Exception:
            pass
        return devices
            
    def build_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#1e293b", pady=15)
        header.pack(fill=tk.X)
        tk.Label(header, text="Facebook Ekran Yayıncısı", font=("Arial", 16, "bold"), fg="#818cf8", bg="#1e293b").pack()
        
        # Body
        body = tk.Frame(self.root, bg="#0f172a", pady=15, padx=20)
        body.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(body, text="Facebook RTMP URL:", font=("Arial", 10, "bold"), fg="white", bg="#0f172a").pack(anchor="w")
        self.entry_url = tk.Entry(body, width=50, font=("Arial", 10))
        self.entry_url.insert(0, self.config.get("rtmp_url", ""))
        self.entry_url.pack(pady=5, fill=tk.X)
        
        tk.Label(body, text="Facebook Stream Key:", font=("Arial", 10, "bold"), fg="white", bg="#0f172a").pack(anchor="w", pady=(10,0))
        self.entry_key = tk.Entry(body, width=50, font=("Arial", 10), show="*")
        self.entry_key.insert(0, self.config.get("stream_key", ""))
        self.entry_key.pack(pady=5, fill=tk.X)
        
        tk.Label(body, text="Ses Kaynağı:", font=("Arial", 10, "bold"), fg="white", bg="#0f172a").pack(anchor="w", pady=(10,0))
        self.combo_audio = ttk.Combobox(body, values=self.get_audio_devices(), state="readonly", font=("Arial", 10))
        saved_audio = self.config.get("audio_device", "Sistem Sesi (Tarayıcı vb. Tüm Sesler)")
        if saved_audio in self.combo_audio['values']:
            self.combo_audio.set(saved_audio)
        else:
            self.combo_audio.set("Sistem Sesi (Tarayıcı vb. Tüm Sesler)")
        self.combo_audio.pack(pady=5, fill=tk.X)
        
        # Region Selection
        reg_frame = tk.Frame(body, bg="#1e293b", pady=10, padx=10, relief=tk.GROOVE, bd=1)
        reg_frame.pack(fill=tk.X, pady=15)
        
        self.lbl_region = tk.Label(reg_frame, text=f"Seçili Alan: {self.region['w']}x{self.region['h']} (X:{self.region['x']} Y:{self.region['y']})", font=("Arial", 9), fg="#94a3b8", bg="#1e293b")
        self.lbl_region.pack(pady=(0,10))
        
        tk.Button(reg_frame, text="YAYINLANACAK EKRAN BÖLGESİNİ SEÇ", command=self.select_region, bg="#4f46e5", fg="white", font=("Arial", 10, "bold"), relief=tk.FLAT, pady=5).pack(fill=tk.X)
        
        # Controls
        self.btn_start = tk.Button(body, text="▶ Yayını Başlat", command=self.start_stream, bg="#10b981", fg="white", font=("Arial", 12, "bold"), pady=8, relief=tk.FLAT)
        self.btn_start.pack(fill=tk.X, pady=(10,5))
        
        self.btn_stop = tk.Button(body, text="■ Yayını Durdur", command=self.stop_stream, bg="#ef4444", fg="white", font=("Arial", 12, "bold"), pady=8, relief=tk.FLAT, state=tk.DISABLED)
        self.btn_stop.pack(fill=tk.X)
        
        # Log Tracking Panel
        log_frame = tk.Frame(body, bg="#1e293b", pady=5, padx=5, bd=1, relief=tk.SUNKEN)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        tk.Label(log_frame, text="Yayın Logları (Canlı):", font=("Arial", 9, "bold"), fg="#94a3b8", bg="#1e293b").pack(anchor="w")
        
        self.log_text = tk.Text(log_frame, bg="#000000", fg="#10b981", font=("Consolas", 8), height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(5,0))
        self.append_log("Sistem hazır. Yayın bekleniyor...")
        
    def select_region(self):
        self.root.iconify() # Ana pencereyi gizle
        
        sel_win = tk.Toplevel(self.root)
        sel_win.title("Alanı Boyutlandır ve Seç")
        sel_win.geometry(f"{self.region['w']}x{self.region['h']}+{self.region['x']}+{self.region['y']}")
        
        # Şeffaflık ayarı (Windows'a özel kırmızı bir çerçeve yaratır)
        sel_win.attributes('-alpha', 0.5)
        sel_win.attributes('-topmost', True)
        sel_win.configure(bg='red')
        
        msg = "1. Bu yarı şeffaf kırmızı pencereyi ekranınızda kopyalamak istediğiniz alanın üzerine getirin.\n\n2. Köşelerinden çekerek tam istediğiniz boyuta getirin.\n\n3. Hazır olunca aşağıdaki butona basın."
        lbl = tk.Label(sel_win, text=msg, font=("Arial", 12, "bold"), bg="red", fg="white", justify=tk.CENTER, wraplength=400)
        lbl.pack(expand=True)
        
        def on_confirm():
            x = sel_win.winfo_x()
            y = sel_win.winfo_y()
            w = sel_win.winfo_width()
            h = sel_win.winfo_height()
            
            # Ekran sınırlarını al (DPI aware olduğu için gerçek piksellerdir)
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Koordinatları 0'dan başlat
            x = max(0, x)
            y = max(0, y)
            
            # Ekran sınırlarını aşmasını engelle
            if x + w > screen_width: w = screen_width - x
            if y + h > screen_height: h = screen_height - y
            
            # FFmpeg genişlik ve yükseklik değerlerinin çift sayı olmasını zorunlu kılar.
            self.region['w'] = w if w % 2 == 0 else w - 1
            self.region['h'] = h if h % 2 == 0 else h - 1
            self.region['x'] = x
            self.region['y'] = y
            
            self.lbl_region.config(text=f"Seçili Alan: {self.region['w']}x{self.region['h']} (X:{self.region['x']} Y:{self.region['y']})")
            sel_win.destroy()
            self.root.deiconify() # Ana pencereyi geri getir
            
        tk.Button(sel_win, text="BU ALANI ONAYLA", command=on_confirm, font=("Arial", 14, "bold"), bg="black", fg="white", pady=10, padx=20).pack(pady=20)
        
    def start_stream(self):
        self.save_config()
        rtmp = self.entry_url.get().strip()
        key = self.entry_key.get().strip()
        
        if not key:
            messagebox.showerror("Hata", "Lütfen Stream Key girin!")
            return
            
        stream_url = f"{rtmp}/{key}" if not rtmp.endswith('/') else f"{rtmp}{key}"
        
        try:
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception as e:
            messagebox.showerror("Hata", f"FFmpeg bulunamadı: {e}")
            return
            
        cmd = [
            ffmpeg_exe, "-y",
            "-f", "gdigrab",
            "-framerate", "30",
            "-offset_x", str(self.region['x']),
            "-offset_y", str(self.region['y']),
            "-video_size", f"{self.region['w']}x{self.region['h']}",
            "-i", "desktop"
        ]
        
        selected_audio = self.combo_audio.get()
        use_pyaudio = False
        loopback_device = None
        
        if selected_audio == "Sistem Sesi (Tarayıcı vb. Tüm Sesler)":
            try:
                import pyaudiowpatch as pyaudio
            except ImportError:
                messagebox.showerror("Hata", "Ses kütüphanesi bulunamadı! 'pip install pyaudiowpatch' çalıştırılmalı.")
                return
                
            self.pyaudio_instance = pyaudio.PyAudio()
            try:
                loopback_device = self.pyaudio_instance.get_default_wasapi_loopback()
                use_pyaudio = True
            except Exception as e:
                messagebox.showerror("Hata", f"Sistem sesi alınamadı: {e}")
                self.pyaudio_instance.terminate()
                self.pyaudio_instance = None
                return

        if use_pyaudio:
            cmd.extend([
                "-f", "s16le",
                "-ar", str(int(loopback_device['defaultSampleRate'])),
                "-ac", str(loopback_device['maxInputChannels']),
                "-i", "pipe:0"
            ])
        elif selected_audio == "Sessiz (Sadece Görüntü)":
            cmd.extend(["-f", "lavfi", "-i", "anullsrc"])
        else:
            cmd.extend(["-f", "dshow", "-i", f"audio={selected_audio}"])
            
        cmd.extend([
            "-c:v", "libx264", "-preset", "veryfast", "-maxrate", "2500k", "-bufsize", "5000k",
            "-pix_fmt", "yuv420p", "-g", "60",
            "-c:a", "aac", "-b:a", "128k",
            "-f", "flv", stream_url
        ])
        
        self.append_log(f"Çözünürlük: {self.region['w']}x{self.region['h']} (X:{self.region['x']} Y:{self.region['y']})")
        
        stdin_dest = subprocess.PIPE if use_pyaudio else subprocess.DEVNULL
        # Byte okuma için universal_newlines=False olmalı, encoding kaldırılmalı.
        self.process = subprocess.Popen(cmd, stdin=stdin_dest, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
        
        if use_pyaudio:
            import pyaudiowpatch as pyaudio
            def audio_callback(in_data, frame_count, time_info, status):
                if self.process and self.process.poll() is None:
                    try:
                        self.process.stdin.write(in_data)
                    except Exception:
                        pass
                return (in_data, pyaudio.paContinue)
            
            self.audio_stream = self.pyaudio_instance.open(
                format=pyaudio.paInt16,
                channels=loopback_device["maxInputChannels"],
                rate=int(loopback_device["defaultSampleRate"]),
                input=True,
                frames_per_buffer=2048,
                input_device_index=loopback_device["index"],
                stream_callback=audio_callback
            )
            
        self.btn_start.config(state=tk.DISABLED, text="YAYINDA...")
        self.btn_stop.config(state=tk.NORMAL)
        
        self.append_log("--- YAYIN BAŞLATILDI ---")
        threading.Thread(target=self.log_reader_thread, daemon=True).start()
        
    def log_reader_thread(self):
        if not self.process: return
        try:
            for line in iter(self.process.stdout.readline, b''):
                if not line: break
                text = line.decode('utf-8', errors='replace').strip()
                self.root.after(0, self.append_log, text)
        except Exception:
            pass

    def append_log(self, text):
        if int(self.log_text.index('end-1c').split('.')[0]) > 100:
            self.log_text.delete('1.0', '10.0')
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)
        
    def stop_stream(self):
        if hasattr(self, 'audio_stream') and self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            self.audio_stream = None
        if hasattr(self, 'pyaudio_instance') and self.pyaudio_instance:
            self.pyaudio_instance.terminate()
            self.pyaudio_instance = None
            
        if self.process:
            self.process.terminate()
            self.process = None
        
        self.append_log("--- YAYIN DURDURULDU ---")
        self.btn_start.config(state=tk.NORMAL, text="▶ Yayını Başlat")
        self.btn_stop.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
