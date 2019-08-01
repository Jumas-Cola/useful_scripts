from Utils import Utils
import json
import random

config = json.loads(open('config.json').read())
n = random.randint(0, len(config['tumblr_users']) - 1)
s = Utils(config['access_token'], config['tumblr_users'][n]['user'], config['tumblr_users'][n]['posting_type'])
post = s.get_tmblr_post(s.upd_tmblr_start())
s.make_vk_post(post, config['group_id'], config['message'])
