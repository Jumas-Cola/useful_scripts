import requests
import vk_api


class VkUtils:
    def __init__(self, access_token):
        self.vk = vk_api.VkApi(token=access_token)
        self.v = '5.101'

    """
        Загрузка изображения на сервер и получение объекта photo
    """

    def picture_send(self, image_to_send):
        a = self.vk.method('photos.getWallUploadServer', {'v': self.v})
        b = requests.post(a['upload_url'], files={
                          'photo': open(image_to_send, 'rb')}).json()
        c = self.vk.method('photos.saveWallPhoto', {
            'photo': b['photo'],
            'server': b['server'],
            'hash': b['hash'],
            'v': self.v
        })[0]
        d = 'photo{owner_id}_{id}'.format(owner_id=c['owner_id'], id=c['id'])
        return d

    """
        Загрузка документа на сервер и получение объекта doc
    """

    def file_send(self, file_to_send):
        a = self.vk.method('docs.getWallUploadServer', {'v': self.v})
        b = requests.post(a['upload_url'], files={
                          'file': open(file_to_send, 'rb')}).json()
        c = self.vk.method('docs.save', {
            'file': b['file'],
            'v': self.v
        })
        d = 'doc{owner_id}_{id}'.format(owner_id=c['doc']['owner_id'], id=c['doc']['id'])
        return d
