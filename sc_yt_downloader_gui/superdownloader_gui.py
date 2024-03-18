# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer
from lib.Downloader import Downloader as scdl
from pytube import YouTube as yt

from pathlib import Path
import os

import requests
import os
from mutagen.id3 import ID3, APIC
import mutagen

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog, messagebox, simpledialog, Menu, BooleanVar

# OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = os.path.join("assets", "frame0")


client_id = 'rVtnkH7kI646kRDwGSONEc7euMBMyJwv'
downloader = scdl(client_id)
window = Tk()
window.title("superdownloader GUI")
window.resizable(False, False)
window.geometry("400x224")
window.configure(bg="#FFFFFF")
window.eval('tk::PlaceWindow . center')


def set_client_id():
    client_id = simpledialog.askstring("what", "is yo soundcloud client id: ")
    if client_id:
        messagebox.showinfo("ye", "gotchu")


menu_bar = Menu(window)
window.config(menu=menu_bar)

prefs = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="prefs", menu=prefs)
prefs.add_command(label="soundcloud client id", command=set_client_id)

include_artist = BooleanVar()
include_artist.set(True)

metadata = BooleanVar()
metadata.set(True)

prefs.add_checkbutton(label="include artist name", variable=include_artist, onvalue=True, offvalue=False)
prefs.add_checkbutton(label="auto-generate metadata", variable=metadata, onvalue=True, offvalue=False)


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def parse_url(url):
    if 'soundcloud' in url:
        return 'soundcloud'
    elif 'youtube' in url:
        return 'youtube'
    else:
        return None


def add_yt_metadata(url, dest):
    # get thumbnail as 'cover art'
    ytube = yt(url)
    img_url = ytube.thumbnail_url
    img = requests.get(img_url).content
    temp_ca = 'temp.jpg'
    with open(temp_ca, 'wb') as fi:
        fi.write(img)

    # get video name
    vidname = ytube.vid_info['videoDetails']['title']

    # 'artist' (channel) name
    artistname = ytube.author

    audio_ez = mutagen.File(dest, easy=True)
    if audio_ez.tags is None:
        audio_ez.add_tags()
    audio_ez['artist'] = artistname
    audio_ez['title'] = vidname
    audio_ez.save()

    # add cover art - can't use easyID3
    ad = mutagen.File(dest)
    with open(temp_ca, 'rb') as coverart:
        ad['APIC'] = APIC(
            encoding=3,
            mime='image/jpeg',
            type=3,
            desc=u'Cover',
            data=coverart.read()
        )
    ad.save()

def download():
    url = entry_1.get()

    which = parse_url(url)

    if which == 'soundcloud':
        try:
            res = downloader.get_resolved(url)
            stream = downloader.get_streaming_url(res)
            filename_hint = f"{res['user']['username']} - {res['title']}" if include_artist.get() else res['title']
            dest = filedialog.asksaveasfilename(initialfile=f"{filename_hint}.mp3", defaultextension=".mp3")
            if not dest:
                return
            downloader.stream_download(stream, dest)
            if metadata.get():
                downloader.add_metadata(res, dest)
            messagebox.showinfo("lesgo", "soundcloud downloaded")
        except Exception as e:
            messagebox.showerror("error!!!", str(e))
    elif which == 'youtube':
        try:
            ytube = yt(url)
            audio = ytube.streams.get_audio_only()
            video = ytube.streams.filter(file_extension = 'mp4').get_highest_resolution()
            filetypes = (
                ('mp3 (audio only)', '*.mp3'),
                ('mp4 (video + audio)', '*.mp4'),
            )
            dest = filedialog.asksaveasfilename(defaultextension='.mp3', filetypes=filetypes, initialfile = f"{ytube.author} - {ytube.vid_info['videoDetails']['title']}")
            if not dest:
                return
            if dest[-4:] == '.mp4':
                video.download(filename = dest)
            else:
                audio.download(filename=dest)
                if metadata:
                    add_yt_metadata(url, dest)


            messagebox.showinfo("lesgo", "youtube downloaded")
        except Exception as e:
            messagebox.showerror("error!!!", str(e))
    else:
        messagebox.showwarning("what", "you dumbaxe")



canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=224,
    width=400,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_rectangle(
    0.0,
    0.0,
    400.0,
    224.0,
    fill="#000000",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    82.0,
    165.0,
    image=image_image_1
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    200.5,
    100.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=('Arial', 20),
    insertbackground="#000000"
)
entry_1.place(
    x=33.0,
    y=78.0,
    width=335.0,
    height=42.0
)

canvas.create_text(
    42.0,
    42.0,
    anchor="nw",
    text="soundcloud/youtube url:",
    fill="#FFFFFF",
    font=("Papyrus", 20 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=download,  # NOTE NOTE TODO NOTE
    relief="flat"
)
button_1.place(
    x=135.0,
    y=154.0,
    width=131.0,
    height=33.0
)

button_image_hover_1 = PhotoImage(
    file=relative_to_assets("button_hover_1.png"))


def button_1_hover(e):
    button_1.config(
        image=button_image_hover_1
    )


def button_1_leave(e):
    button_1.config(
        image=button_image_1
    )


button_1.bind('<Enter>', button_1_hover)
button_1.bind('<Leave>', button_1_leave)


window.mainloop()
