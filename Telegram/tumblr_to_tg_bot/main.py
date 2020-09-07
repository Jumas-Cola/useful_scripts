from Session import TumblrSession
import json
import random
import os
from telethon import TelegramClient, events, sync
from urllib.request import urlretrieve
from urllib.request import urlparse
from pathlib import Path


def download_and_return_path(img_list):
    return [urlretrieve(img_url,
        os.path.basename(urlparse(img_url).path))[0]
        for img_url in img_list]


curr_dir = Path(__file__).parent
path = curr_dir.joinpath('config.json')

config = json.loads(open(path).read())
locals().update(config)

tumblr_user = random.choice(tumblr_users)
s = TumblrSession(tumblr_user)
post = s.get_tmblr_photo_post()

with TelegramClient(channel, api_id, api_hash) as client:
    entity = client.get_entity(channel)
    files = download_and_return_path(post['imgs'])

    if any(not i.endswith(('png', 'jpg', 'jpeg')) for i in files):
        for n, f in enumerate(files):
            client.send_file(
                    entity,
                    f,
                    caption=post['photo-caption'] if n==0 else ''
                    )
    else:
        client.send_file(
                entity,
                files,
                caption=post['photo-caption']
                )

    for f in files:
        os.remove(f)

