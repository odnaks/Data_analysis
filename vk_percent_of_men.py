import requests

users = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
m = 0
w = 0
for user in users:
    param = {
        'user_id': user,
        'v': 5.52,
        'fields': 'sex, bdate',
        'access_token': '75cd869975cd869975cd86996775a4a6ba775cd75cd8699294dd25619e5cef8820bf1d7'
    }
    r = requests.get('https://api.vk.com/method/users.get?', param)
    data = r.json()
    sex = data['response'][0]['sex']
    if sex == 1:
        w+=1
    elif sex == 2:
        m+=1
print (w / (w + m))
