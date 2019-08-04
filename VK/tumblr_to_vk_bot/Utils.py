from TumblrAPI import TumblrAPI
from VkUtils import VkUtils
from ConnectDB import ConnectDB
from urllib.request import urlretrieve
from urllib.parse import urlparse
import os
import re
import json
import random


class Utils:
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
                if 'photo-url-1280' in post:
                    break
        elif self.posting_type == 0:
            # Случайный порядок
            for i in range(1000):
                state[self.tumblr_user] = random.randint(0, tmblr_count - 1)
                post = self.get_tmblr_post(state[self.tumblr_user])
                if ('photo-url-1280' in post) and (not self.db.check(post['id'])):
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
                if 'photo-url-1280' in post:
                    break
        with open(file, 'w') as f:
            f.write(json.dumps(state))
        return post

    def make_vk_post(self, tmblr_post, group_id, message=None):
        from_url = tmblr_post['url']
        if message is None:
            photo_caption = tmblr_post['photo-caption'] if 'photo-caption' in tmblr_post else None
            message = """{caption}

            Источник: {from_url}""".format(from_url=from_url, caption=photo_caption)

        urls = []
        if ('photos' in tmblr_post) and tmblr_post['photos']:
            for photo in tmblr_post['photos']:
                urls.append(photo['photo-url-1280'])
        else:
            urls.append(tmblr_post['photo-url-1280'])

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
            'message': self.cleanhtml(message),
            'attachments': ','.join(attachments)
        })

    @staticmethod
    def cleanhtml(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext
