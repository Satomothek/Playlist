import pygame
import tkinter as tk

playlist = [
    "Cry.mp3",
    "Apocalypse.mp3",
    "Moth To A Flame.mp3",
    "Save Your Tears.mp3",
    "All to Myself.mp3"
]

pygame.mixer.init()
current = 0
playing = False
paused = False
last_idx = None
song_length = 0
seeking = False
manual_seek_pos = None 

def update_scale():
    global manual_seek_pos
    if playing and not paused and not seeking:
        pos = pygame.mixer.music.get_pos() // 1000
        if manual_seek_pos is not None:
            if pos == 0 and manual_seek_pos == 0:
                time_scale.set(0)
            if abs(pos - manual_seek_pos) <= 1 and pos != 0:
                time_scale.set(pos)
                manual_seek_pos = None
            else:
                time_scale.set(manual_seek_pos)
        else:
            time_scale.set(pos)
    root.after(300, update_scale)

def play_song(start_pos=0):
    global playing, paused, last_idx, current, song_length
    selected = listbox.curselection()
    if selected:
        idx = selected[0]
    else:
        idx = current

    if paused and idx == last_idx:
        pygame.mixer.music.unpause()
        status_label.config(text=f"Memainkan: {playlist[idx]}")
    else:
        pygame.mixer.music.load(playlist[idx])
        pygame.mixer.music.play(start=start_pos)
        status_label.config(text=f"Memainkan: {playlist[idx]}")
        current = idx
    playing = True
    paused = False
    last_idx = idx

    try:
        from mutagen.mp3 import MP3
        audio = MP3(playlist[idx])
        song_length = int(audio.info.length)
        time_scale.config(to=song_length)
    except:
        song_length = 0
        time_scale.config(to=100)

def pause_song():
    global paused, last_idx
    pygame.mixer.music.pause()
    status_label.config(text="Paused")
    paused = True
    last_idx = listbox.curselection()[0] if listbox.curselection() else current

def next_song():
    global current
    current = (current + 1) % len(playlist)
    listbox.selection_clear(0, tk.END)
    listbox.selection_set(current)
    play_song()

def stop_song():
    global playing
    pygame.mixer.music.stop()
    status_label.config(text="Stopped")
    playing = False

def seek_start(event):
    global seeking
    seeking = True

def seek_end(event):
    global seeking, paused, last_idx, manual_seek_pos, current, playing
    pos = int(time_scale.get())
    selected = listbox.curselection()
    if selected:
        idx = selected[0]
    else:
        idx = current

    pygame.mixer.music.load(playlist[idx])
    pygame.mixer.music.play(start=pos)
    status_label.config(text=f"Memainkan: {playlist[idx]}")
    current = idx
    playing = True
    paused = False
    last_idx = idx
    seeking = True
    manual_seek_pos = pos
    root.after(10, reset_seeking)

def reset_seeking():
    global seeking
    seeking = False

def on_closing():
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    root.destroy()

root = tk.Tk()
root.title("Playlist Lagu")

status_label = tk.Label(root, text="Tekan Play untuk mulai", width=40)
status_label.pack(pady=5)

listbox = tk.Listbox(root, width=40)
for song in playlist:
    listbox.insert(tk.END, song)
listbox.pack(pady=5)

time_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, length=300, label="Waktu (detik)")
time_scale.pack(pady=5)
time_scale.bind("<Button-1>", seek_start)
time_scale.bind("<ButtonRelease-1>", seek_end)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Play", width=10, command=play_song).grid(row=0, column=0, padx=2)
tk.Button(btn_frame, text="Pause", width=10, command=pause_song).grid(row=0, column=1, padx=2)
tk.Button(btn_frame, text="Next", width=10, command=next_song).grid(row=0, column=2, padx=2)
tk.Button(btn_frame, text="Stop", width=10, command=stop_song).grid(row=0, column=3, padx=2)

root.protocol("WM_DELETE_WINDOW", on_closing)
update_scale()
root.mainloop()