import vk_api
import urllib.request
from multiprocessing import Pool
import os
from urllib.parse import urlparse
from functools import partial


class UserPhotoCollector:
    def __init__(self, token, id, folder_name=False, path=False, procs=10):
        self.v = '5.101'
        self.vk = vk_api.VkApi(token=token)
        user = self.vk.method(
            'users.get', {'user_ids': id, 'v': self.v})[0]
        self.id = str(user['id'])
        if folder_name == 'surname':
            try:
                folder_name = user['last_name']
            except:
                folder_name = False
        self.folder_name = folder_name or self.id
        self.path = os.path.join(path, self.folder_name) or os.path.join(os.path.dirname(
            os.path.abspath(__file__)), self.folder_name)
        self.count = 1000
        self.procs = procs

    def get_albums(self):
        return [i['id'] for i in self.vk.method('photos.getAlbums', {
            'owner_id': self.id,
            'v': self.v
        })['items']] + ['wall', 'profile']

    def get_photos(self, album, offset):
        return self.vk.method('photos.get', {
            'owner_id': self.id,
            'album_id': album,
            'rev': 0,
            'offset': offset,
            'count': self.count,
            'v': self.v
        })['items']

    def get_all_photos(self, album):
        links = []
        offset = 0
        photos = self.get_photos(album, offset)
        while photos:
            links += [photo['sizes'][-1]['url'] for photo in photos]
            offset += self.count
            photos = self.get_photos(album, offset)
        return links

    def download_list(self, url_list):
        func = partial(self.download, self.path)
        with Pool(self.procs) as p:
            p.map(func, url_list)

    @staticmethod
    def download(path, url):
        if not os.path.exists(path):
            os.mkdir(path)
        file = os.path.basename(urlparse(url).path)
        return urllib.request.urlretrieve(url, f'{path}/{file}')

    def dump(self):
        for album in self.get_albums():
            self.download_list(self.get_all_photos(album))
