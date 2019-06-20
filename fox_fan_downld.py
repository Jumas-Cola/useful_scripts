from urllib.request import urlretrieve as download
from urllib.parse import urljoin, urlparse
from multiprocessing import Process
from bs4 import BeautifulSoup
import requests
import re
import os


class FFDownloader:
    """
    Скрипт для скачивания серий/сезонов с fox-fan.
    В конструктор можно опционально передавать индекс озвучки.
    Можно счачать сезон целиком:
        download_season('http://<...>.fox-fan.tv/season.php?id=1')
    Или отдельно серии:
        d.download_series('http://<...>.fox-fan.tv/series.php?id=619')
    """

    def __init__(self, voice=None):
        self.voice = voice

    def download_season(self, season_url):
        procs = []
        page = requests.get(season_url).content
        soup = BeautifulSoup(page, 'html.parser')

        for series in soup.select('td.block_season_top > h2 > a'):
            proc = Process(target=self.download_series, args=(
                urljoin(season_url, series['href']),))
            procs.append(proc)
            proc.start()

        for proc in procs:
            proc.join()

    def download_series(self, series_url):
        page = requests.get(series_url, params={'voice': self.voice}).text
        src = re.findall(
            r"var\splayer\s=\snew\sPlayerjs\({id:'.*',\s*file:'(.*)',comment:",
            page)[0]
        a = urlparse(src)
        path_list = a.path.split('/')
        name = path_list[-1]
        path = os.path.join(os.getcwd(), *path_list[-4:-1])
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except:
                pass
        download(src, os.path.join(path, name))


if __name__ == '__main__':
    d = FFDownloader()
    d.download_season('http://futurama.fox-fan.tv/season.php?id=7')
    # d.download_series('http://futurama.fox-fan.tv/series.php?id=619')
