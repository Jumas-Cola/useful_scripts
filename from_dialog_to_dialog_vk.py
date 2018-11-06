import vk_api
import time


login = 'login'
password = 'password'
"""
	Для пользователя:
	id пользователя.

	Для групповой беседы:
	2000000000 + id беседы.

	Для сообщества:
	-id сообщества.
"""
# откуда
peer_id = 2000000000+6
# куда
send_to_id = 123456789
# типы вложений
media_types = ['photo', 'video', 'audio', 'doc']
# задержка между сообщениями
delay = 5


vk = vk_api.VkApi(login=login, password=password)
vk.auth()

for media_type in media_types:
	messages_with_attachments = vk.method('messages.getHistoryAttachments', {'peer_id': peer_id, 'media_type': media_type, 'count': 200})
	next_from = messages_with_attachments['next_from']
	attachments = []
	while next_from:
		for message_with_attachments in messages_with_attachments['items']:
			attachment = message_with_attachments['attachment']
			media = attachment[media_type]
			attachments.append('{}{}_{}'.format(media_type, media['owner_id'], media['id']))
			if len(attachments) == 10 :
				try:
					vk.method('messages.send', {'peer_id' : send_to_id, 'attachment' : ','.join(attachments)})
					attachments = []
					time.sleep(delay)
				except:
					pass
		try:
			vk.method('messages.send', {'peer_id' : send_to_id, 'attachment' : ','.join(attachments)})
			attachments = []
			time.sleep(delay)
		except:
			pass
		messages_with_attachments = vk.method('messages.getHistoryAttachments', {'peer_id': peer_id, 'media_type': media_type, 'start_from': next_from, 'count': 200})
		try:
			next_from = messages_with_attachments['next_from']
		except:
			next_from = ''
