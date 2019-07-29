"""
    Скрипт для выкачивания изображений из альбома (в т.ч. со стены сообщества) (vk.com)
    Usage: downl_from_group_vk.py <owner_id> <album_id> <access_token>
"""

import urllib.request
from multiprocessing import Pool
import vk_api
import os
import sys


def download(url):
    file = url.split('/')[-1]
    return urllib.request.urlretrieve(url, f'{path}/{file}')


def get_photos(offset):
    return vk.method('photos.get', {'owner_id': config['owner_id'], 'album_id': config['album_id'],
                                    'rev': 0, 'offset': offset, 'count': config['count'], })['items']


def assignment():
    config['owner_id'], config['album_id'], config['access_token'] = sys.argv[1], sys.argv[2], sys.argv[3]


config = {
    'owner_id': '',
    'album_id': '',
    'count': 1000,
    'processes': 10,
    'access_token': '',
    'v': '5.92',
}

assignment() if len(sys.argv) == 4 else exit(
    print('Usage: downl_from_group_vk.py <owner_id> <album_id> <access_token>'))

path = f'{config["owner_id"]}_{config["album_id"]}'

if __name__ == '__main__':
    offset = 0
    if not os.path.exists(path):
        os.mkdir(path)
    vk = vk_api.VkApi(token=config['access_token'])
    photos = get_photos(offset)
    while photos:
        url_list = [photo['sizes'][-1]['url'] for photo in photos]
        with open(f'{path}/url_list.txt', 'a') as f:
            [f.write(url + '\n') for url in url_list]
        with Pool(config['processes']) as p:
            p.map(download, url_list)
        offset += config['count']
        photos = get_photos(offset)
