import requests
import vk_api
import json
import os


config = {
    'to_group_id': '',
    'to_album_id': 123456789,
    'access_token': '',
    'v': '5.92',
    'path_to_folder': 'C:\\Users\\...',
}


def upd_offset(offset=0, file_name='vk_config.json'):
    if offset:
        with open(file_name, "w") as jsonFile:
            json.dump({'offset': offset}, jsonFile)
        return True
    try:
        with open(file_name, "r") as jsonFile:
            data = json.load(jsonFile)
        offset = data['offset']
    except:
        with open(file_name, "w") as jsonFile:
            json.dump({'offset': offset}, jsonFile)
    return offset


def picture_send(vk, image_to_send, album_id, group_id=''):
    a = vk.method('photos.getUploadServer', {
                  'group_id': group_id, 'album_id': album_id, 'v': config['v']})
    b = requests.post(a['upload_url'], files={
                      'photo': open(image_to_send, 'rb')}).json()
    c = vk.method('photos.save', {'group_id': group_id, 'album_id': album_id,
                                  'photos_list': b['photos_list'], 'server': b['server'], 'hash': b['hash'], 'v': config['v']})[0]
    d = 'photo{}_{}'.format(c['owner_id'], c['id'])
    return d


vk = vk_api.VkApi(token=config['access_token'])
files = os.listdir(config['path_to_folder'])
offset = upd_offset(0)
for i in range(len(files))[offset:]:
    picture_send(vk, path + '\\' +
                 files[i], config['to_album_id'], config['to_group_id'])
    upd_offset(i + 1)
