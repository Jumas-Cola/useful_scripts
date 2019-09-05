"""
Скрипт для скачивания музыки из VK
Основан на данной статье:
https://habr.com/ru/sandbox/132499/

Использование:
py vk_audio_saver.py -l <login> -p <password> -i <user_id_1> <user_id_2> ... { -pr <processes> }
"""


import os
import vk_api
from vk_api.audio import VkAudio
from urllib.request import urlretrieve
from multiprocessing import Pool
from functools import partial
import sys
import argparse
import re


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--login')
    parser.add_argument('-p', '--password')
    parser.add_argument('-i', '--ids', nargs='+')
    parser.add_argument('-pr', '--processes', default=10)
    return parser


def auth_handler(remember_device=None):
    code = input("Введите код подтверждения\n> ")
    if (remember_device is None):
        remember_device = True
    return code, remember_device


def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]


def download(audios, folder='vk_music'):
    for audio in audios:
        url = audio['url']
        file_name = '{}-{}.mp3'.format(audio['artist'], audio['title'])
        file_name = re.sub(r'[ \|/:*?"<>+%!@]', '_', file_name)
        print('Скачивание: {}'.format(file_name))
        try:
            urlretrieve(url, os.path.join(folder, file_name))
            print('Скачивание завершено: {}'.format(file_name))
        except:
            print('Не удалось скачать: {}'.format(file_name))


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    if not namespace.login:
        raise Exception('Login required!')
    if not namespace.password:
        raise Exception('Password required!')
    if not namespace.ids:
        raise Exception('Users ids required!')

    login = namespace.login
    password = namespace.password
    user_ids = namespace.ids
    processes = int(namespace.processes)

    vk = vk_api.VkApi(login=login, password=password)
    try:
        vk.auth()
    except:
        vk = vk_api.VkApi(login=login, password=password,
                          auth_handler=auth_handler)
        vk.auth()
    vk_audio = VkAudio(vk)
    for user_id in user_ids:
        folder = '{}_audio'.format(user_id)
        audios = vk_audio.get(owner_id=user_id)
        print('Будет скачано {} композиций пользователя {}.'.format(
            len(audios), user_id))
        if not os.path.exists(folder):
            os.mkdir(folder)
        func = partial(download, folder=folder)
        p = Pool(processes)
        p.map(func, chunkify(audios, processes))
        print('Завершено скачивание композиций пользователя {}.'.format(user_id))
