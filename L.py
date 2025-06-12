import pygame
import customtkinter as ctk
from mutagen.mp3 import MP3
import time
from datetime import datetime
import os

# Global variables
pygame.mixer.init()
current = 0
playing = False
paused = False
song_length = 0
current_time = 0
is_updating_time = False
current_position = 0
last_slider_value = 0

playlist = [
    os.path.join(os.path.dirname(__file__), "Cry.mp3"),
    os.path.join(os.path.dirname(__file__), "Apocalypse.mp3"),
    os.path.join(os.path.dirname(__file__), "Moth To A Flame.mp3"),
    os.path.join(os.path.dirname(__file__), "Save Your Tears.mp3"),
    os.path.join(os.path.dirname(__file__), "All to Myself.mp3")
]

# Define all functions first
def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def prev_song():
    global current, playing
    current = (current - 1) % len(playlist)
    playing = False
    play_song()

def play_song():
    global playing, paused, current, song_length
    idx = current
    
    if not playing:
        try:
            pygame.mixer.music.load(playlist[idx])
            pygame.mixer.music.play()
            title_label.configure(text=os.path.basename(playlist[idx]))
            playing = True
            paused = False
            
            # Update song length
            audio = MP3(playlist[idx])
            song_length = int(audio.info.length)
            time_slider.configure(to=song_length)
            duration_label.configure(text=format_time(song_length))
        except Exception as e:
            print(f"Error playing audio: {e}")
            playing = False
    elif paused:
        pygame.mixer.music.unpause()
        paused = False

def pause_song():
    global paused
    if playing and not paused:
        pygame.mixer.music.pause()
        paused = True

def next_song():
    global current, playing
    current = (current + 1) % len(playlist)
    playing = False
    play_song()

def on_slider_press(event):
    global is_updating_time
    is_updating_time = True

def on_slider_release(event):
    global is_updating_time, current_position, playing, last_slider_value
    try:
        current_position = float(time_slider.get())
        last_slider_value = current_position
        
        if playing:
            pygame.mixer.music.play(start=current_position)
        else:
            playing = True
            pygame.mixer.music.load(playlist[current])
            pygame.mixer.music.play(start=current_position)
        
        time_label.configure(text=format_time(int(current_position)))
    except Exception as e:
        print(f"Error seeking: {e}")
    finally:
        is_updating_time = False

def update_time():
    global current_position, last_slider_value
    if playing and not paused and not is_updating_time:
        try:
            pos = pygame.mixer.music.get_pos()
            if pos > 0:
                current_time = pos // 1000 + last_slider_value
                if current_time >= 0:
                    current_position = current_time
                    time_slider.set(current_time)
                    time_label.configure(text=format_time(current_time))
                    
                    if current_time >= song_length:
                        next_song()
        except:
            pass
    root.after(100, update_time)

def on_closing():
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    root.destroy()

# Initialize UI components after all functions are defined
root = ctk.CTk()
root.title("Music Player")
root.geometry("300x200")

# Create UI components
title_label = ctk.CTkLabel(root, text="", font=("Helvetica", 12))
title_label.pack(pady=10)

time_frame = ctk.CTkFrame(root)
time_frame.pack(fill='x', padx=10)

time_label = ctk.CTkLabel(time_frame, text="00:00", width=50)
time_label.pack(side='left', padx=5)

time_slider = ctk.CTkSlider(time_frame, from_=0, to=100, width=200)
time_slider.pack(side='left', padx=5, fill='x', expand=True)
time_slider.bind("<Button-1>", on_slider_press)
time_slider.bind("<ButtonRelease-1>", on_slider_release)

duration_label = ctk.CTkLabel(time_frame, text="00:00", width=50)
duration_label.pack(side='right', padx=5)

btn_frame = ctk.CTkFrame(root)
btn_frame.pack(expand=True)

prev_btn = ctk.CTkButton(btn_frame, text="⏮", width=60, command=prev_song)
prev_btn.grid(row=0, column=0, padx=5)

play_btn = ctk.CTkButton(btn_frame, text="▶", width=60, command=play_song)
play_btn.grid(row=0, column=1, padx=5)

pause_btn = ctk.CTkButton(btn_frame, text="⏸", width=60, command=pause_song)
pause_btn.grid(row=0, column=2, padx=5)

next_btn = ctk.CTkButton(btn_frame, text="⏭", width=60, command=next_song)
next_btn.grid(row=0, column=3, padx=5)

# Start application
root.protocol("WM_DELETE_WINDOW", on_closing)
update_time()
root.mainloop()
