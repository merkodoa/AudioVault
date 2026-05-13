import customtkinter as ctk
from tkinter import filedialog
import yt_dlp
import os
import threading

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("550x400")
app.title("AudioVault")

def wybierz_folder():
    wybrany_katalog = filedialog.askdirectory()
    if wybrany_katalog:
        pole_folderu.delete(0, 'end')
        pole_folderu.insert(0, wybrany_katalog)

def proces_pobierania(url, sciezka_zapisu, fformat):
    if fformat == "Audio":
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        'outtmpl': os.path.join(sciezka_zapisu, '%(title)s.%(ext)s'),
        }
    else: 
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'outtmpl': os.path.join(sciezka_zapisu, '%(title)s.%(ext)s'),
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        status_label.configure(text="Download successful!", text_color="green")
        pole_linku.delete(0, 'end')
    except Exception as e:
        status_label.configure(text="Error while downloading.", text_color="red")
        print(f"Błąd: {e}")
    finally:
        przycisk_pobierz.configure(state="normal")

def klikniecie_pobierz():
    link = pole_linku.get()
    folder = pole_folderu.get()
    wybrany_format = format_var.get()
    
    if not link.strip():
        status_label.configure(text="Insert link...", text_color="red")
        return
    if not folder.strip() or not os.path.exists(folder):
        status_label.configure(text="Choose an existing folder!", text_color="red")
        return
        
    status_label.configure(text="Downloading...", text_color="orange")
    przycisk_pobierz.configure(state="disabled")
    
    watek = threading.Thread(target=proces_pobierania, args=(link, folder,wybrany_format))
    watek.start()

ctk.CTkLabel(app, text="AudioVault", font=("Arial", 20, "bold")).pack(pady=15)

ctk.CTkLabel(app, text="File link:").pack()
pole_linku = ctk.CTkEntry(app, placeholder_text="Insert audio file link", width=450)
pole_linku.pack(pady=5)

ctk.CTkLabel(app, text="File format:").pack(pady=(10,0))
format_var = ctk.StringVar(value="Audio")
format_switch = ctk.CTkSegmentedButton(app, values=["Audio", "Video"], variable=format_var)
format_switch.pack(pady=5)

ctk.CTkLabel(app, text="Folder to store:").pack(pady=(10, 0))
kontener_folderu = ctk.CTkFrame(app, fg_color="transparent") 
kontener_folderu.pack(pady=5)

pole_folderu = ctk.CTkEntry(kontener_folderu, width=340)
pole_folderu.pack(side="left", padx=(0, 10))

pole_folderu.insert(0, os.path.dirname(os.path.abspath(__file__)))

przycisk_folder = ctk.CTkButton(kontener_folderu, text="Choose folder...", width=100, command=wybierz_folder)
przycisk_folder.pack(side="left")

przycisk_pobierz = ctk.CTkButton(app, text="Download", height=40, font=("Arial", 14, "bold"), command=klikniecie_pobierz)
przycisk_pobierz.pack(pady=30)

status_label = ctk.CTkLabel(app, text="")
status_label.pack()

app.mainloop()