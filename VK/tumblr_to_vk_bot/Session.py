from TumblrAPI import TumblrAPI
from VkUtils import VkUtils
from ConnectDB import ConnectDB
from urllib.request import urlretrieve
from urllib.parse import urlparse
import os
import re
import json
import random
from bs4 import BeautifulSoup


class Session:
    curr_dir = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, access_token, tumblr_user, posting_type=1):
        self.tumblr_user = tumblr_user
        self.tmblr_session = TumblrAPI(self.tumblr_user)
        self.vk_session = VkUtils(access_token)
        self.db = ConnectDB()
        self.posting_type = posting_type

    def get_tmblr_post(self, start, type='photo'):
        return self.tmblr_session.request({'type': type, 'num': 1, 'start': start})['posts'][0]

    def get_tmblr_count(self, type='photo'):
        return self.tmblr_session.request({'type': type})['posts-total']

    def upd_tmblr_state(self, file=os.path.join(curr_dir, 'state.json')):
        if not os.path.exists(file):
            state = {}
            with open(file, 'w') as f:
                f.write(json.dumps(state))
        else:
            state = json.loads(open(file).read())
        tmblr_count = self.get_tmblr_count()
        if self.posting_type == 1:
            # От старых к новым
            for i in range(1000):
                if self.tumblr_user not in state:
                    state[self.tumblr_user] = tmblr_count - 1
                else:
                    state[self.tumblr_user] -= 1
                    if state[self.tumblr_user] < 0:
                        state[self.tumblr_user] = tmblr_count - 1
                post = self.get_tmblr_post(state[self.tumblr_user])
                content = self.parse_content(post)
                if content:
                    break
        elif self.posting_type == 0:
            # Случайный порядок
            for i in range(1000):
                state[self.tumblr_user] = random.randint(0, tmblr_count - 1)
                post = self.get_tmblr_post(state[self.tumblr_user])
                if not self.db.check(post['id']):
                    content = self.parse_content(post)
                    if content:
                        break
            self.db.insert(post['id'])
        elif self.posting_type == -1:
            # Обратный порядок
            for i in range(1000):
                if self.tumblr_user not in state:
                    state[self.tumblr_user] = 0
                else:
                    state[self.tumblr_user] += 1
                    if state[self.tumblr_user] >= self.get_tmblr_count():
                        state[self.tumblr_user] = 0
                post = self.get_tmblr_post(state[self.tumblr_user])
                content = self.parse_content(post)
                if content:
                    break
        with open(file, 'w') as f:
            f.write(json.dumps(state))
        return content

    @staticmethod
    def parse_content(post):
        content = {}
        imgs = []
        if ('photos' in post) and post['photos']:
            imgs.extend([photo['photo-url-1280'] for photo in post['photos']])
        elif 'photo-url-1280' in post:
            imgs.append(post['photo-url-1280'])
        elif 'regular-body' in post:
            soup = BeautifulSoup(post['regular-body'], 'html.parser')
            imgs.extend([img.get('src') for img in soup.select('img')])
        imgs = list(filter(lambda x: x, imgs))
        if imgs:
            content['imgs'] = imgs
            content['url'] = post['url']
            if 'photo-caption' in post:
                content['photo-caption'] = Session.cleanhtml(post['photo-caption'])
            else:
                content['photo-caption'] = ''
            return content
        else:
            return content

    def make_vk_post(self, content, group_id, message=None):
        if message is None:
            message = """{caption}

            Источник: {from_url}""".format(from_url=content['url'], caption=content['photo-caption'])

        urls = content['imgs']

        attachments = []
        for url in urls:
            destination = os.path.basename(urlparse(url).path)
            urlretrieve(url, destination)
            is_picture = destination.endswith(('.jpg', '.png', '.jpeg'))
            attachments.append(self.vk_session.picture_send(destination)
                               if is_picture
                               else self.vk_session.file_send(destination))
            os.remove(destination)

        self.vk_session.vk.method('wall.post', {
            'owner_id': group_id,
            'message': message,
            'attachments': ','.join(attachments)
        })

    @staticmethod
    def cleanhtml(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext
