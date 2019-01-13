"""
    Скрипт для перемещения фотографий из одного альбома в другой
"""

import urllib.request
from urllib.parse import urlparse
import requests
import vk_api
import json
import time
import os


config = {
    'from_owner_id': 408736104,
    'from_album_id': 'saved',
    'to_group_id': 169696294,
    'to_album_id': 258350914,
    'count': 1000,
    'token_list': [
        '',
        '',
    ],
    'v': '5.92',
}


def picture_send(vk, image_to_send, group_id, album_id):
    a = vk.method('photos.getUploadServer', {
                  'group_id': group_id, 'album_id': album_id, 'v': config['v']})
    b = requests.post(a['upload_url'], files={
                      'photo': open(image_to_send, 'rb')}).json()
    c = vk.method('photos.save', {'group_id': group_id, 'album_id': album_id,
                                  'photos_list': b['photos_list'], 'server': b['server'], 'hash': b['hash'], 'v': config['v']})[0]
    d = 'photo{}_{}'.format(c['owner_id'], c['id'])
    return d


def get_start_offset(vk, to_gr_id, to_al_id, fr_ou_id, fr_al_id, file_name='vk_config.json'):
    offset = 0
    try:
        with open(file_name, "r") as jsonFile:
            data = json.load(jsonFile)
        if (data['to_gr_id'] == to_gr_id) and (data['to_al_id'] == to_al_id) and (data['fr_ou_id'] == fr_ou_id) and (data['fr_al_id'] == fr_al_id):
            offset = data['start_offset']
        else:
            data['to_gr_id'] = to_gr_id
            data['to_al_id'] = to_al_id
            data['fr_ou_id'] = fr_ou_id
            data['fr_al_id'] = fr_al_id
            offset = vk.method('photos.get', {
                               'owner_id': to_gr_id, 'album_id': to_al_id})['count']
            data['start_offset'] = offset
    except:
        data = {}
        data['to_gr_id'] = to_gr_id
        data['to_al_id'] = to_al_id
        data['fr_ou_id'] = fr_ou_id
        data['fr_al_id'] = fr_al_id
        offset = vk.method('photos.get', {
                           'owner_id': to_gr_id, 'album_id': to_al_id})['count']
        data['start_offset'] = offset
    with open(file_name, "w") as jsonFile:
        json.dump(data, jsonFile)
    return offset


i = 0
vk = vk_api.VkApi(token=config['token_list'][0])
start_offset = get_start_offset(
    vk, -config['to_group_id'], config['to_album_id'], config['from_owner_id'], config['from_album_id'])
offset = vk.method('photos.get', {
                   'owner_id': -config['to_group_id'], 'album_id': config['to_album_id']})['count'] - start_offset
photos = vk.method('photos.get', {'owner_id': config['from_owner_id'], 'album_id': config['from_album_id'],
                                  'rev': 0, 'offset': offset, 'count': config['count'], })['items']
while photos:
    for photo in photos:
        url = photo['sizes'][-1]['url']
        file = urlparse(url)[2].split('/')[-1]
        urllib.request.urlretrieve(url, file)
        print(i)
        vk = vk_api.VkApi(token=config['token_list'][i])
        picture_send(vk, file, config['to_group_id'], config['to_album_id'])
        os.remove(file)
        if len(config['token_list']) > 1:
            i += 1
            if i == len(config['token_list']):
                i = 0
        # time.sleep(0.4)
    offset += config['count']
    photos = vk.method('photos.get', {'owner_id': config['from_owner_id'], 'album_id': config['from_album_id'],
                                      'rev': 0, 'offset': offset, 'count': config['count'], })['items']
