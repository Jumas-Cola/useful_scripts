"""
lat - географическая широта отметки, заданная в градусах (от -90 до 90). 
дробное число

long - географическая долгота отметки, заданная в градусах (от -180 до 180). 
дробное число

start_time - время в формате unixtime, не раньше которого должны были быть загружены найденные фотографии. 
положительное число

end_time - время в формате unixtime, не позже которого должны были быть загружены найденные фотографии. 
положительное число

sort - сортировка результатов. Возможные значения:
1 — по количеству отметок «Мне нравится»;
0 — по дате добавления фотографии.
положительное число

offset - смещение относительно первой найденной фотографии для выборки определенного подмножества. 
положительное число

count - количество возвращаемых фотографий. 
положительное число, по умолчанию 100, максимальное значение 1000

radius - радиус поиска в метрах. (работает очень приближенно, поэтому реальное расстояние до цели может отличаться от заданного). Может принимать значения: 10, 100, 800, 6000, 50000 
положительное число, по умолчанию 5000
"""

import geocoder
import vk_api
from datetime import datetime
from datetime import timedelta

def date_to_unixtime(in_date):
	year = int(in_date.split('.')[0])
	month = int(in_date.split('.')[1].lstrip('0'))
	day = int(in_date.split('.')[2].lstrip('0'))
	return int((datetime(year, month, day) - datetime(1970, 1, 1)).total_seconds())

def convertTSToDate(timestamp):
	return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') + ' UTC'

def get_photos(lat, long, start_time, end_time, radius, count, offset, sort=0):
	photos = vk.method('photos.search', {
				'lat':lat, 
				'long':long, 
				'start_time':start_time,
				'end_time':end_time,
				'sort':sort,
				'radius':radius,
				'count': count,
				'offset': offset,
				'v':'3.0'})[1:]
	return photos


# блок задания параметров
place = 'Orekhovo-Zuyevo'
lat = '55.8034354'
long = '38.9667903'
start_time = date_to_unixtime('2018.09.25')
end_time = date_to_unixtime('2018.10.01')
radius = 6000
count = 1000
counts = 10 # количество раз по count
login = 'login'
password = 'password'
offset = 0 # начальный отступ


# если не заданы координаты - то попытаться определить по названию place (работает раз/через раз)
if (not lat) or (not long):
	if place == 'me':
		coords = geocoder.ip('me').latlng
	else:
		coords = geocoder.google(place).latlng
	lat = str(coords[0])
	long = str(coords[1])

# авторизация вк
vk = vk_api.VkApi(login=login, password=password)
vk.auth()

# парсинг с записью в html
result_page = open('vk_{}-{}.html'.format(lat, long), 'w')
result_page.write('<html>')
for i in range(counts):
	photos = get_photos(lat, long, start_time, end_time, radius, count, offset)
	for photo in photos:
		result_page.write('<br>')
		result_page.write('<img src={}><br>'.format(photo['src_big']))
		try:
			result_page.write('<pre>{}</pre>'.format(photo['text']))
		except:
			result_page.write('<pre>TextError</pre>')
		try:
			result_page.write('{}, {}<br>'.format(str(photo['lat']), str(photo['long'])))
		except:
			result_page.write('<pre>LatLongError</pre>')
		result_page.write(convertTSToDate(photo['created']) + '<br>')
		owner_id = str(abs(photo['owner_id']))
		if photo['owner_id'] < 0:
			result_page.write('<a href=\"http://vk.com/club{}\">http://vk.com/club{}</a><br>'.format(owner_id, owner_id))
		else:
			result_page.write('<a href=\"http://vk.com/id{}\">http://vk.com/id{}</a><br>'.format(owner_id, owner_id))
		result_page.write('<br>')
	offset+=count
result_page.write('</html>')
result_page.close()
