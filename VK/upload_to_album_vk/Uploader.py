import requests
import vk_api
import time
import os


class Uploader:
    def __init__(self, login, password, group_id, path_to_folder):
        self.login = login
        self.password = password
        self.group_id = group_id
        self.path_to_folder = path_to_folder
        self.v = '5.92'

        self.folder_name = os.path.basename(self.path_to_folder)
        self.photos = []
        for root, dirs, files in os.walk(self.path_to_folder):
            self.photos += [os.path.join(root, file) for file in files]
        # print(f'Photos count: {len(self.photos)}')
        self.vk = vk_api.VkApi(login=self.login, password=self.password)
        self.vk.auth()

    def create_album(self):
        new_album = self.vk.method('photos.createAlbum', {
            'title': self.folder_name,
            'group_id': self.group_id
        })
        return new_album

    def upload_photos(self, images_to_send, album_id):
        upload_server = self.vk.method('photos.getUploadServer', {
            'group_id': self.group_id,
            'album_id': album_id,
            'v': self.v
        })
        server_response = requests.post(upload_server['upload_url'], files={
            f'file{i + 1}': open(images_to_send[i], 'rb') for i in range(len(images_to_send))
        }).json()
        save_response = self.vk.method('photos.save', {
            'group_id': self.group_id,
            'album_id': album_id,
            'photos_list': server_response['photos_list'],
            'server': server_response['server'],
            'hash': server_response['hash'],
            'v': self.v
        })[0]
        photo_obj = 'photo{}_{}'.format(save_response['owner_id'], save_response['id'])
        return photo_obj

    def upload_album(self):
        new_album = self.create_album()
        for i in range(0, len(self.photos), 5):
            self.upload_photos(self.photos[i: i + 5], new_album['id'])
            time.sleep(0.5)
            yield i + 5, len(self.photos)
        # print('Uploading finished!')
