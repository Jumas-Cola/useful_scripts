import sys
import youtube_dl
import os
from multiprocessing import Pool

'''
Usage:
python3 video_download.py <url1> <url2>...
or
python3 video_download.py -f file.txt
'''

def downloader(url):

    print('Start downloading:', url)

    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join('downloads', '%(title)s.%(ext)s'),
        'nooverwrites': True,
        'no_warnings': False,
        'ignoreerrors': True,
        'cookiefile': os.path.join(os.path.dirname(sys.argv[0]), 'cookies.txt'),
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])



if __name__ == '__main__':

    if sys.argv[1] == '-f':
        with open(sys.argv[2]) as f:
            urls = (url.strip() for url in f.readlines())
    else:
        urls = sys.argv[1:]

    if not os.path.isdir('downloads'):
        os.mkdir('downloads')

    with Pool(5) as p:
        p.map(downloader, urls)
