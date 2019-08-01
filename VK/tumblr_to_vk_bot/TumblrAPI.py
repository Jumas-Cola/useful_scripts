import requests
import json


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

    def request(self, params={}):
        params['callback'] = 'a'
        self.api_url = self.api_url.format(user=self.user)
        response = requests.get(self.api_url, params=params).text
        return json.loads(response[2: -2])
