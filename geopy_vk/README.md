geopy_vk ![Python 3.6](https://pp.userapi.com/c846523/v846523407/b716d/N3RXKWFcPS0.jpg)
======
**geopy_vk** – скрипт для поиска фотографий по дате и геолокации для социальной сети Вконтакте (vk.com)

Для запуска введите:
* координаты **lat**, **long** или название населённого пункта **place** (поиск по названию работает через раз из-за особенностей библиотеки **geocoder**)
* начальную дату **start_time** в формате **YYYY.MM.DD**
* конечную дату **end_time** в формате **YYYY.MM.DD**
* логин от страницы вк (для авторизации и доступа к методу **photos.search**)
* пароль от страницы вк

```python
...
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
...
```

Внимание
------------
Идея взята из этой статьи.
Реализация собственная.

Статья:
[https://habr.com/company/xakep/blog/254129/](https://habr.com/company/xakep/blog/254129/)
