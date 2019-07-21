import vk_api
import urllib.request
from multiprocessing import Pool
import os
from urllib.parse import urlparse
from functools import partial


class UserPhotoCollector:
    def __init__(self, token, id, folder_name=False, path=False, procs=10, by_albums=False):
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
        self.path = os.path.join(path, self.folder_name) or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), self.folder_name)
        self.count = 1000
        self.procs = procs
        self.by_albums = by_albums

    def get_albums(self):
        return [{'id': i['id'], 'title': i['title']}
                for i in self.vk.method('photos.getAlbums', {
                    'owner_id': self.id,
                    'v': self.v
                })['items']] +\
            [{'id': 'wall', 'title': 'Фото_со_стены'},
             {'id': 'profile', 'title': 'Фото_профиля'}]

    def get_photos(self, album, offset):
        return self.vk.method('photos.get', {
            'owner_id': self.id,
            'album_id': album,
            'rev': 0,
            'offset': offset,
            'count': self.count,
            'v': self.v
        })['items']

    def get_all_photos(self, album_id):
        links = []
        offset = 0
        photos = self.get_photos(album_id, offset)
        while photos:
            links += [photo['sizes'][-1]['url'] for photo in photos]
            offset += self.count
            photos = self.get_photos(album_id, offset)
        return links

    def download_list(self, url_list, sub_path=False):
        func = partial(self.download, os.path.join(
            self.path, sub_path) if sub_path else self.path)
        with Pool(self.procs) as p:
            p.map(func, url_list)

    @staticmethod
    def download(path, url):
        if not os.path.exists(path):
            os.makedirs(path)
        file = os.path.basename(urlparse(url).path)
        return urllib.request.urlretrieve(url, f'{path}/{file}')

    def dump(self):
        for album in self.get_albums():
            if self.by_albums:
                try:
                    title = '{}_{}'.format(album['title'], album['id'])
                except:
                    title = album['id']
                self.download_list(self.get_all_photos(album['id']), title)
            else:
                self.download_list(self.get_all_photos(album['id']))
