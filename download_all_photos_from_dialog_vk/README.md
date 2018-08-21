download_all_photos_from_dialog_vk ![Python 3.6](https://pp.userapi.com/c846523/v846523407/b716d/N3RXKWFcPS0.jpg)
======
**download_all_photos_from_dialog_vk** – скрипт для скачивания всех фотографий из диалога для социальной сети Вконтакте (vk.com)

Для запуска введите:
* id диалога. Для этого откройте желаемый диалог. В URL после **https://vk.com/im?sel=** будут идти цифры. Это и есть id диалога.
* тип медиа менять не нужно.
* имя папки, куда будут сохранены фотографии (папка создаётся самой программой в текущей директории)
* логин от страницы вк
* пароль от страницы вк

```python
...
# id диалога (параметр sel)
peer_id = 123456789
# тип медиа (в данном случае - фотографии)
media_type = 'photo'
# имя папки, куда скачивать фото (создаётся самой программой)
name = 'New_Folder'

login = 'login'

password = 'password'
...
```

Метод VK API
------------
Скрипт использует всего один метод VK API - messages.getHistoryAttachments.

Подробнее о методе:
[https://vk.com/dev/messages.getHistoryAttachments](https://vk.com/dev/messages.getHistoryAttachments)
