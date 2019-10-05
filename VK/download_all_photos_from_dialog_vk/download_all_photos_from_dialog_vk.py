from urllib.parse import urlparse
import urllib.request
import vk_api
import os


def download(url, path):
    file = '_'.join(urlparse(photo[size])[2].split('/')[-4:])
    urllib.request.urlretrieve(url, path + '/' + file)


def file_write(file_name='New_File', string=''):
    f = open(file_name, 'a')
    f.write(string)
    f.write("\n")
    f.close()


# id диалога (параметр sel)
peer_id = 123456789
token = ''


vk = vk_api.VkApi(token=token)
media_type = 'photo'
user_id = vk.method('users.get')[0]['id']
photo_sizes = ['photo_2560', 'photo_1280',
               'photo_807', 'photo_604', 'photo_130', 'photo_75']
name = 'user_{}_dialog_{}_dump'.format(user_id, peer_id)

try:
    os.makedirs(name)
except:
    pass

messages_with_attachments = vk.method('messages.getHistoryAttachments', {
                                      'peer_id': peer_id, 'media_type': media_type, 'count': 200, 'v': '5.62'})
next_from = messages_with_attachments['next_from']

urls = []

while next_from:
    print(next_from)
    for message_with_attachments in messages_with_attachments['items']:
        attachment = message_with_attachments['attachment']
        media = attachment[media_type]
        if media_type == 'photo':
            photo = media
            for size in photo_sizes:
                if size in photo:
                    url = photo[size]
                    if url not in urls:
                        file_write(name + '.txt', url)
                        download(url, name)
                        urls.append(url)
                        break
    messages_with_attachments = vk.method('messages.getHistoryAttachments', {
                                          'peer_id': peer_id, 'media_type': media_type, 'start_from': next_from, 'count': 200, 'v':'5.62'})
    try:
        next_from = messages_with_attachments['next_from']
    except:
        next_from = ''
