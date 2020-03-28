#!/usr/bin/env python3

'''
Usage:
    python3 youtube_to_mp3.py < url_1 > < url_2 > ... < url_n >
Result:
    mp3 files in "downloads" folder
'''

import os
import sys
from pytube import YouTube
from moviepy.editor import VideoFileClip


for url in sys.argv[1:]:
    try:
        mp4_path = YouTube(url.strip()).streams.get_highest_resolution().download('downloads')
        mp3_path = mp4_path[:-1] + '3'
        video = VideoFileClip(mp4_path)
        video.audio.write_audiofile(mp3_path)
        os.remove(mp4_path)
    except Exception as e:
        print(url, str(e))

