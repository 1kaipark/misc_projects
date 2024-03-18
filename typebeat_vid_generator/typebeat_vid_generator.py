import subprocess
import os
import random

def create_video(img_path, audio_path, output_path):
    """
    creates video based on given inputs
    args:
        img_path: path to image
        audio_path: path to audio file
        output_path: output path of video
    """

    gif = img_path.lower().endswith('.gif')

    cmd = [
        'ffmpeg',
        '-i', img_path,
        '-i', audio_path,
        '-c:v', 'libx264', # video codec
        '-c:a', 'aac', # audio codec
        '-b:a', '192k', # audio bitrate
        '-pix_fmt', 'yuv420p', # pixel formate
        '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black', # retain original aspect ratio
        '-shortest',
        output_path
    ]
    if gif:
        cmd.insert(1, '-1')
        cmd.insert(1, '-stream_loop')
        print('gif')
    if not gif:
        cmd.extend(['-loop', '1'])
        cmd.extend(['-tune', 'stillimage'])
    try:
        subprocess.run(cmd, check = True)
    except subprocess.CalledProcessError as e:
        print(f"L {e}")


imgs_dir = input("absolute path to image directory: \n")
if imgs_dir.endswith(' '):
    imgs_dir = imgs_dir[:-1]
audio_file = input("absolute path to audio file: \n")
if audio_file.endswith(' '):
    audio_file = audio_file[:-1]

output_file = input("filename of output video, will be saved in current directory: \n")

# choose random image from directory
imgs_dir_files = os.listdir(imgs_dir)
img_exts = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

imgs_l = []

for img in imgs_dir_files:
    for ext in img_exts:
        if img.lower().endswith(ext) and img not in imgs_l:
            imgs_l.append(img)

img_file = random.choice(imgs_l)
img_path = os.path.join(imgs_dir, img_file)

create_video(img_path, audio_file, output_file)

