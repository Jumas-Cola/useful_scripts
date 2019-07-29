"""
Постит картинки из папки в группу.
text - сообщение, которое будет отправлено вместе с картинкой.
После отправки картинка удаляется из папки.
Запускать через cron.
"""

import requests
import random
import vk_api
import time
import os



# загрузка изображения на сервер и получение объекта photo
def picture_send(image_to_send):
    a = vk.method('photos.getWallUploadServer')
    b = requests.post(a['upload_url'], files={'photo': open(image_to_send, 'rb')}).json()
    c = vk.method('photos.saveWallPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
    d = 'photo{}_{}'.format(c['owner_id'], c['id'])
    return d

def vk_request(vk, method, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить запрос
    :param vk: объект vk_api
    :param method: метод vk_api
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    delay = 100
    jitter = 0.1
    for i in range(max_retries):
        try:
            error = vk.method(method, params)
            return error
        except Exception as err:
            error = err
        time.sleep(delay*0.001)
        delay = delay*(1+backoff_factor)
        delay = delay + random.normalvariate(delay, jitter)
    return error


folder_name = 'folder'
owner_id = '-169696294'
text = ''
login = 'login'
password = 'password'


first_pic = os.listdir(path=folder_name)[0]
picture = f'{folder_name}/{first_pic}'
vk = vk_api.VkApi(login=login, password=password)
vk.auth()
try:
    picture_obj = picture_send(picture)
    vk_request(vk, 'wall.post', {'owner_id': owner_id, 'message': text, 'attachments': picture_obj, 'from_group': 1, 'signed': 0})
    os.remove(picture)
except:
    pass
