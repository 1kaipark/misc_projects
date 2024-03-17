from pytube import YouTube as yt
import os

url = input("yt vid link: \n")
yt = yt(str(url))

audio = yt.streams.filter(only_audio = True)
os.makedirs('yt_mp3_dls', exist_ok = True)
audio[0].download('yt_mp3_dls')
