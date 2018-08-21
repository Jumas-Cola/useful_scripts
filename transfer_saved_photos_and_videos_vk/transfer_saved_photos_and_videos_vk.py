import time
import vk_api
import os
import random


def file_write(photo_of, video_of, file_name='offsets.txt'):
	f = open(file_name,'w')
	f.write(str(photo_of))
	f.write("\n")
	f.write(str(video_of))
	f.close()

def file_read(file_name='offsets.txt'):
	with open(file_name, 'r') as file:
		file_list = [int(i.replace('\n','')) for i in file]
	return file_list




login = 'login'
password = 'password'

#...id страницы, с которой необходимо скопировать медиа
owner_id = 408736104
#...id альбома, из которого копировать фото. в данном случае - сохранённые фотографии
photo_album_id = 'saved'
#..нужно ли копировать фото
copy_photo = True
#..нужно ли копировать видео
copy_video = True




try:
	photo_offset, video_offset = file_read()
	if video_offset!=0:
		video_offset+=1
except:
	photo_offset = 0
	video_offset = 0


vk = vk_api.VkApi(login=login, password=password)
vk.auth()
count = 100

if copy_photo == True:
	offset = photo_offset
	photo_ids = []
	photos = vk.method('photos.get', {'owner_id': owner_id, 'album_id': photo_album_id, 'offset': offset, 'count': count})['items']
	while photos:
		for photo in photos:
			photo_ids.append(photo['id'])
		offset += 100
		photos = vk.method('photos.get', {'owner_id': owner_id, 'album_id': photo_album_id, 'offset': offset, 'count': count})['items']
	print('Photos count: {}'.format(len(photo_ids)))
	counter = photo_offset
	for num in photo_ids:
		print("{} : {}".format(num, counter))
		vk.method('photos.copy', {'owner_id': owner_id, 'photo_id': num})
		counter += 1
		file_write(counter, video_offset)
		time.sleep(random.randint(15, 35)*0.1)

	photo_end = counter
else:
	photo_end = 0

if copy_video == True:
	offset = video_offset
	video_ids = []
	videos = vk.method('video.get', {'owner_id': owner_id, 'offset': offset, 'count': count})['items']
	while videos:
		for video in videos:
			video_ids.append({ 'owner_id': video["owner_id"], 'video_id': video['id']})
		offset += 100
		videos = vk.method('video.get', {'owner_id': owner_id, 'offset': offset, 'count': count})['items']
	print('Videos count: {}'.format(len(video_ids)))
	counter = video_offset
	for num in video_ids:
		print("{} : {}".format(num, counter))
		vk.method('video.add', {'owner_id': num['owner_id'], 'video_id': num['video_id']})
		counter += 1
		file_write(photo_end, counter)
		time.sleep(random.randint(15, 55)*0.1)

try:
	os.remove("offsets.txt")
except:
	pass
print('All media copied!')