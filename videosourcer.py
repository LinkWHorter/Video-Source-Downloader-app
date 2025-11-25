import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
import ctypes
import json
from yt_dlp import YoutubeDL

# ------------------- PyInstaller resource path -------------------
def resource_path(relative_path):
    """Возвращает абсолютный путь к файлу, работает и для .exe и для .py"""
    try:
        base_path = sys._MEIPASS  # PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ------------------- Config -------------------
def get_default_download_folder():
    return os.path.join(os.path.expanduser("~"), "Downloads")

def get_config_path():
    local_appdata = os.getenv("LOCALAPPDATA") or os.path.abspath(".")
    config_dir = os.path.join(local_appdata, "ViDownloader")
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "config.json")

CONFIG_PATH = get_config_path()

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("Ошибка чтения config.json:", e)
    return {}

def save_config(data):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print("Ошибка сохранения конфигурации:", e)

# ------------------- Шрифт -------------------
def load_custom_font(path):
    if os.path.exists(path):
        try:
            FR_PRIVATE = 0x10
            ctypes.windll.gdi32.AddFontResourceExW(path, FR_PRIVATE, 0)
        except Exception as e:
            print("Ошибка загрузки шрифта:", e)

FONT_PATH = resource_path(os.path.join("fonts", "Genshin_Impact.ttf"))
load_custom_font(FONT_PATH)

# ------------------- CustomTkinter setup -------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

COLOR_BG = "#2d2d2d"
COLOR_BTN = "#d94f4f"
COLOR_ACCENT = "#4f4f4f"

# ------------------- Главное окно -------------------
app = ctk.CTk()
app.title("Скачивальщик видео")
app.geometry("600x320")
app.resizable(False, False)
icon_path = resource_path("icons/icon.ico")
app.iconbitmap(icon_path)
app.configure(fg_color=COLOR_BG)

# ------------------- Шрифт -------------------
try:
    from tkinter import font as tkfont

    FR_PRIVATE = 0x10
    if os.path.exists(FONT_PATH):
        ctypes.windll.gdi32.AddFontResourceExW(FONT_PATH, FR_PRIVATE, 0)

    font_family = "TT_Skip-E 85W"
    test_font = tkfont.Font(family=font_family, size=12)
    custom_font = (font_family, 12)
except Exception as e:
    print("Ошибка со шрифтом:", e)
    custom_font = ("Arial", 14)

# ------------------- Конфиг и переменные -------------------
config = load_config()
save_folder = config.get("save_folder", get_default_download_folder())
video_quality = ctk.StringVar(value="720p")

# ------------------- Выбор папки -------------------
def choose_folder():
    global save_folder
    folder = filedialog.askdirectory()
    if folder:
        save_folder = folder
        config["save_folder"] = folder
        save_config(config)

# ------------------- Прогресс -------------------
def progress_hook(d):
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 1
        progress = downloaded / total if total else 0
        progress_bar.set(progress)
    elif d['status'] == 'finished':
        progress_bar.set(1)

# ------------------- Загрузка -------------------
def start_download():
    url = url_entry.get().strip()
    quality = video_quality.get().replace("p", "")

    if not url:
        messagebox.showerror("Ошибка", "Вставьте ссылку")
        return

    def run():
        download_button.configure(state="disabled", text="Скачивание...")
        progress_bar.set(0)

        format_str = f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]'

        if "tiktok.com" in url:
            format_str = "best[ext=mp4][vcodec!*=hevc]"

        ydl_opts = {
            'format': format_str,
            'outtmpl': os.path.join(save_folder, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            'quiet': True,
            'no_warnings': True,
            'merge_output_format': 'mkv',
            'noplaylist': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'http_headers': {
                'Referer': 'https://www.tiktok.com/'
            }
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            messagebox.showerror("Ошибка загрузки", str(e))

        download_button.configure(state="normal", text="Скачать")
        progress_bar.set(1)

    threading.Thread(target=run, daemon=True).start()

# ------------------- UI элементы -------------------
url_frame = ctk.CTkFrame(app, fg_color=COLOR_BG)
url_frame.place(x=20, y=20)

url_entry = ctk.CTkEntry(
    url_frame,
    width=487,
    font=custom_font,
    fg_color=COLOR_BG,
    text_color="white",
    placeholder_text="Вставьте ссылку сюда",
    corner_radius=12,
    border_width=1,
    border_color="#bbbbbb",
)
url_entry.pack(fill="both", padx=10, pady=10, ipady=4)
url_entry.focus_set()

def on_key(event):
    ctrl = event.state & 0x4
    if ctrl and event.keycode == 86:
        try:
            url_entry.insert(tk.INSERT, app.clipboard_get())
        except tk.TclError:
            pass
        return "break"
    if ctrl and event.keycode == 65:
        url_entry.select_range(0, tk.END)
        url_entry.icursor(tk.END)
        return "break"

def select_all(event=None):
    url_entry.select_range(0, tk.END)
    url_entry.icursor(tk.END)
    return "break"

url_entry.bind("<KeyPress>", on_key)
url_entry.bind("<Control-a>", select_all)
url_entry.bind("<Control-A>", select_all)

folder_button = ctk.CTkButton(app, text="...", width=40, font=custom_font,
                              corner_radius=12, fg_color=COLOR_ACCENT, hover_color="#666666",
                              command=choose_folder)
folder_button.place(x=535, y=32)

quality_select = ctk.CTkOptionMenu(app,
                                   values=["144p", "240p", "360p", "480p", "720p", "1080p"],
                                   variable=video_quality,
                                   width=100,
                                   font=ctk.CTkFont(family=custom_font[0], size=12),
                                   corner_radius=12,
                                   fg_color=COLOR_ACCENT,
                                   button_color=COLOR_BTN)
quality_select.place(x=475, y=80)

progress_bar = ctk.CTkProgressBar(app, width=560, height=20, corner_radius=12, progress_color=COLOR_BTN)
progress_bar.place(x=20, y=230)
progress_bar.set(0)

download_button = ctk.CTkButton(app, text="Скачать", font=ctk.CTkFont(family=custom_font[0], size=14),
                                width=560, height=40, corner_radius=12,
                                fg_color=COLOR_BTN, hover_color="#aa3d3d",
                                command=start_download)
download_button.place(x=20, y=260)

app.mainloop()
