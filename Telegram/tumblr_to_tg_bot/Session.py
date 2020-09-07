from TumblrAPI import TumblrAPI
from TumblrAPI import parse_content
import json
import random
from pathlib import Path


class TumblrSession:

    curr_dir = Path(__file__).parent

    def __init__(self, tumblr_user, posting_type=1, retries=1000):
        self.tumblr_user = tumblr_user
        self.api_session = TumblrAPI(tumblr_user)
        self.posting_type = posting_type
        self.retries = retries


    def get_tmblr_photo_post(self, _file=curr_dir.joinpath('prev_post_ids.json')):

        if not _file.is_file():
            state = {}
            with open(_file, 'w') as f:
                f.write(json.dumps(state))
        else:
            state = json.loads(open(_file).read())

        post_id = state[self.tumblr_user] if self.tumblr_user in state else None
        total_posts = self.api_session.photo_posts_total

        for i in range(self.retries):
            if self.posting_type == 1:
                # От старых к новым
                if post_id is None or post_id < 0:
                    post_id = total_posts - 1
                else:
                    post_id -= 1
            elif self.posting_type == 0:
                # Случайный порядок
                post_id = random.choice(set(range(0, total_posts)) - \
                        {post_id} if post_id is not None else {})
            elif self.posting_type == -1:
                # Обратный порядок
                if post_id is None or post_id >= total_posts:
                    post_id = 0
                else:
                    post_id += 1
            post = self.api_session.get_photo_post(post_id)
            content = parse_content(post)
            if content:
                break
        state[self.tumblr_user] = post_id

        with open(_file, 'w') as f:
            f.write(json.dumps(state))
        return content
