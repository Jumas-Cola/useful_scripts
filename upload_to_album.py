"""
    Скрипт для загрузки фотографий в альбом
"""

import urllib.request
from urllib.parse import urlparse
import requests
import vk_api
import json
import time
import os


config = {
    'group_id': 176241274,
    'album_id': 258875314,
    'token_list': [
        '',
        '',
    ],
    'v': '5.92',
    'path_to_folder': r'C:\Users\...',
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


def get_start_offset(vk, group_id, album_id, file_name='vk_config.json'):
    offset = 0
    try:
        with open(file_name, "r") as jsonFile:
            data = json.load(jsonFile)
        if (data['group_id'] == group_id) and (data['album_id'] == album_id):
            offset = data['start_offset']
        else:
            data['group_id'] = group_id
            data['album_id'] = album_id
            offset = vk.method('photos.get', {
                               'owner_id': group_id, 'album_id': album_id})['count']
            data['start_offset'] = offset
    except:
        data = {}
        data['group_id'] = group_id
        data['album_id'] = album_id
        offset = vk.method('photos.get', {
                           'owner_id': group_id, 'album_id': album_id})['count']
        data['start_offset'] = offset
    with open(file_name, "w") as jsonFile:
        json.dump(data, jsonFile)
    return offset


i = 0
vk = vk_api.VkApi(token=config['token_list'][0])
start_offset = get_start_offset(
    vk, -config['group_id'], config['album_id'])
offset = vk.method('photos.get', {
                   'owner_id': -config['group_id'], 'album_id': config['album_id']})['count'] - start_offset
photos = [f'{config["path_to_folder"]}/{file}' for file in os.listdir(config['path_to_folder'])]
for photo in photos[offset:]:
    vk = vk_api.VkApi(token=config['token_list'][i])
    picture_send(vk, photo, config['group_id'], config['album_id'])
    # os.remove(photo)
    if len(config['token_list']) > 1:
        i += 1
        if i == len(config['token_list']):
            i = 0
