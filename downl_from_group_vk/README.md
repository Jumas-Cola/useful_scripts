downl_from_group_vk ![Python 3.6](https://pp.userapi.com/c846523/v846523407/b716d/N3RXKWFcPS0.jpg)
======
**downl_from_group_vk** – скрипт для скачивания файлов со стены для социальной сети Вконтакте (vk.com)

Download only photos and docs
------------

Usage
------------
```shell
python3 downl_from_group_vk.py <login> <password> <owner> <count> <offset> <-sep> <-nd>
```
Necessary
------------
* <***login***>
* <***password***>

Optional
------------
* ***<owner>*** - **123456789**(user id) OR **-123456789**(group id) **[default: your own wall]**
* ***<count>*** - count of 100-s (if count=5 : posts=500). If the number of posts is not a multiple of 100 - superfluous will be ignored. **[default: 1 (100 posts)]**
* ***<offset>*** - offset from newest post **[default: 0]**
* ***<-sep>*** - files to separate folders **[default: all in one folder]**
* ***<-nd>*** - not download. Only .txt file with links. **[default: download]**
