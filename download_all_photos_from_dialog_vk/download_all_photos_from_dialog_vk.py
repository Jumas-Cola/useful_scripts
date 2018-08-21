from urllib.parse import urlparse
import urllib.request
import vk_api
import os


def download(url, path):
	file = '_'.join(urlparse(photo[size])[2].split('/')[-4:])
	urllib.request.urlretrieve(url, path+'/'+file)

def file_write(file_name='New_File', string=''):
	f = open(file_name,'a')
	f.write(string)
	f.write("\n")
	f.close()





# id диалога (параметр sel)
peer_id = 123456789
# тип медиа (в данном случае - фотографии)
media_type = 'photo'
# имя папки, куда скачивать фото (создаётся самой программой)
name = 'New_Folder'

login = 'login'

password = 'password'





photo_sizes = ['photo_2560', 'photo_1280', 'photo_807', 'photo_604', 'photo_130', 'photo_75']

vk = vk_api.VkApi(login=login, password=password)

vk.auth()

try:
	os.makedirs(name)
except:
	pass

messages_with_attachments = vk.method('messages.getHistoryAttachments', {'peer_id': peer_id, 'media_type': media_type, 'count': 200})
next_from = messages_with_attachments['next_from']


while next_from:
	for message_with_attachments in messages_with_attachments['items']:
		attachment = message_with_attachments['attachment']
		media = attachment[media_type]
		if media_type == 'photo':
			photo = media
			for size in photo_sizes:
				if size in photo:
					url = photo[size]
					file_write(name+'.txt', url)
					download(url, name)
					break
	messages_with_attachments = vk.method('messages.getHistoryAttachments', {'peer_id': peer_id, 'media_type': media_type, 'start_from': next_from, 'count': 200})
	try:
		next_from = messages_with_attachments['next_from']
	except:
		next_from = ''
