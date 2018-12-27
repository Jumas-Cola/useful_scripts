
import vk_api

config = {
    'offset': 0,
    'access_token': '',
    'v': '5.92',
}

vk = vk_api.VkApi(token=config['access_token'])

friends = vk.method(
    'friends.get', {'offset': config['offset'], 'v': config['v']})['items']

for i in range(2):
    for friend in friends:
        human = vk.method('users.get', {'user_ids': friend, 'v': config['v']})
        if 'deactivated' in human[0]:
            vk.method('friends.delete', {'user_id': friend, 'v': config['v']})
            print(str(friend) + ' - deleted')
    config['offset'] += 5000
    friends = vk.method(
        'friends.get', {'offset': config['offset'], 'v': config['v']})['items']
