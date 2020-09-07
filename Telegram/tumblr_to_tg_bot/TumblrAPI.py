import requests
import json
import re
from bs4 import BeautifulSoup


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


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
    imgs = [i for i in imgs if i]
    if imgs:
        content['imgs'] = imgs
        content['url'] = post['url']
        if 'photo-caption' in post:
            content['photo-caption'] = cleanhtml(post['photo-caption'])
        else:
            content['photo-caption'] = ''
        return content
    else:
        return content


class TumblrAPI:
    """
    start - The post offset to start from. The default is 0.
    num  - The number of posts to return. The default is 20, and the maximum is 50.
    type - The type of posts to return. If unspecified or empty,
            all types of posts are returned. Must be one of text,
            quote, photo, link, chat, video, or audio.
    id  -  A specific post ID to return. Use instead of start, num, or type.
    filter - Alternate filter to run on the text content. Allowed values:
             text - Plain text only. No HTML.
             none - No post-processing. Output exactly what the author entered.
             (Note: Some authors write in Markdown, which will not be converted
             to HTML when this option is used.)
    tagged - Return posts with this tag in reverse-chronological order
             (newest first). Optionally specify chrono=1 to sort in chronological
             order (oldest first).
    callback - A function name to call with the JSON object as its only
             parameter. When set, the function will be called instead of the
             tumblr_api_read variable being set.
    """

    api_url = 'https://{user}.tumblr.com/api/read/json/'

    def __init__(self, user):
        self.user = user
        self.api_url = self.api_url.format(user=self.user)
        self._photo_posts_total = None

    def request(self, params={}):
        params['callback'] = 'a'
        response = requests.get(self.api_url, params=params)
        if response.ok:
            return json.loads(response.text[2: -2])
        else:
            raise Exception('Response error\nStatus code: {}\nUrl: {}\nParams: {}'.format(response.status_code, self.api_url, params))

    def get_photo_post(self, start, _type='photo'):
        return self.request({'type': _type, 'num': 1, 'start': start})['posts'][0]

    @property
    def photo_posts_total(self, _type='photo'):
        if not self._photo_posts_total:
            self._photo_posts_total = self.request({'type': _type})['posts-total']
        return self._photo_posts_total
