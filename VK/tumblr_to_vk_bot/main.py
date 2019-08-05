from Session import Session
import json
import random
import os


curr_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(curr_dir, 'config.json')
config = json.loads(open(path).read())
n = random.randint(0, len(config['tumblr_users']) - 1)
s = Session(config['access_token'], config['tumblr_users'][n]['user'], config['tumblr_users'][n]['posting_type'])
post = s.upd_tmblr_state()
s.make_vk_post(post, config['group_id'], config['message'])
