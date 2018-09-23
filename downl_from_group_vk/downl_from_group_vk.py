from urllib.parse import urlparse
from copy import copy
import urllib.request
import inspect
import random
import vk_api
import time
import sys
import os


def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

def file_write(string, file_name=get_script_dir()+"/"+'files_vk.txt'):
	f = open(file_name,'a')
	f.write(str(string))
	f.write("\n")
	f.close()

def downloader(url, num, file, downl_try_count):
	downl_try = 0
	while downl_try != downl_try_count:
		try:
			urllib.request.urlretrieve(url, "{}/{}/{}".format(get_script_dir(),str(num),file))
			break
		except:
			downl_try+=1
	if downl_try == downl_try_count:
		print("Download failed")
		file_write("Download failed")

if len(sys.argv) <3:
	print("--------------------------------------------------\n")
	print("Usage: downl_from_group_vk.py <login> <password> <owner> <count> <offset> <-sep> <-nd>\n")
	sys.exit(1)


try:
	login = sys.argv[1]
	password = sys.argv[2]
except:
	sys.exit(1)
try:
	owner = sys.argv[3]
except:
	owner = ''
try:
	count = int(sys.argv[4])
except:
	count = 1
try:
	offset = int(sys.argv[5])
except:
	offset = 0
try:
	if sys.argv[6]=='-sep':
		separate = True
except:
	separate = False
try:
	if sys.argv[7]=='-nd':
		download = False
except:
	download = True


downl_try_count = 50


print("--------------------------------------------------\n")
print("Owner: {}\n".format(owner))
print("Count of 100-s: {}\n".format(str(count)))
print("Offset: {}\n".format(str(offset)))
print("Separate to folders: {}\n".format(str(separate)))
print("Need to download: {}\n".format(str(download)))


vk = vk_api.VkApi(login=login, password=password)
vk.auth()
photo_sizes = ['photo_2560', 'photo_1280', 'photo_807', 'photo_604', 'photo_130', 'photo_75']
num = 0

for i in range(count):
	posts = vk.method('wall.get', {'owner_id': owner, 'count': 100, 'filter': 'owner', 'offset': offset, 'v': '5.60'})['items']
	for post in posts:
		if 'attachments' in post:
			for attachment in post['attachments']:
				if attachment['type'] == 'photo':
					photo = attachment['photo']
					for size in photo_sizes:
						if size in photo:
							url = photo[size]
							file = urlparse(photo[size])[2].split('/')[-1]
							try:
								os.makedirs(get_script_dir()+"/"+str(num))
							except:
								pass
							print(url)
							file_write(str(num)+"\t"+url)
							if download:
								downloader(url, num, file, downl_try_count)
							break
				if attachment['type'] == 'doc':
					doc = attachment['doc']
					url = doc['url']
					file = doc['title']
					try:
						os.makedirs(get_script_dir()+"/"+str(num))
					except:
						pass
					print(url)
					file_write(str(num)+"\t"+url)
					if download:
						downloader(url, num, file, downl_try_count)

		if separate:
			num += 1
	time.sleep(1)
	offset+=100
print("--------------------------------------------------\n")
print("Finished!\n")
