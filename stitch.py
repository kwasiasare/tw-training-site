# -*- coding: utf-8 -*-
"""Stitch slide PNGs + narration WAVs into one MP4 instructor video."""
import os, subprocess
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
VID = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'videos', 'M1_Functions')
count = int(open(os.path.join(VID, 'count.txt')).read().strip())

segments = []
for i in range(1, count + 1):
    n = f'{i:02d}'
    seg = f'seg_{n}.mp4'
    cmd = [FF, '-y', '-loop', '1', '-i', f'slide_{n}.png', '-i', f'audio_{n}.wav',
           '-af', 'apad=pad_dur=0.6',
           '-c:v', 'libx264', '-tune', 'stillimage', '-pix_fmt', 'yuv420p', '-r', '25',
           '-c:a', 'aac', '-b:a', '192k', '-shortest', seg]
    print('segment', n)
    subprocess.run(cmd, cwd=VID, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    segments.append(seg)

# concat list
listfile = os.path.join(VID, 'concat.txt')
with open(listfile, 'w') as f:
    for seg in segments:
        f.write(f"file '{seg}'\n")

out = 'M1_L06_Functions_in_Python.mp4'
subprocess.run([FF, '-y', '-f', 'concat', '-safe', '0', '-i', 'concat.txt',
                '-c', 'copy', out],
               cwd=VID, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# probe duration via ffprobe-less: use ffmpeg to print
outpath = os.path.join(VID, out)
size_mb = os.path.getsize(outpath) / (1024 * 1024)
print(f'\nDONE -> {outpath}')
print(f'Size: {size_mb:.1f} MB')
