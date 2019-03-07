import requests
import time

""" id участников группы habr в вк """

count = 1000
offset = 0
user_ids = []
url = 'https://api.vk.com/method/groups.getMembers'
while offset < 20000:
    print('Выгружаю {} пользователей с offset = {}'.format(count, offset))
    params = {
        'group_id': 'habr',
        'v': 5.73,
        'count': count,
        'offset': offset,
        'access_token': '75cd869975cd869975cd86996775a4a6ba775cd75cd8699294dd25619e5cef8820bf1d7'
    }
    r = requests.get(url, params)
    data = r.json()
    user_ids += data['response']['items']
    offset += count
    print('Ожидаю 0.5 секунды...')
    time.sleep(0.5)
print (user_ids)