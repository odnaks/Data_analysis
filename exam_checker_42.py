import requests
import json
from bs4 import BeautifulSoup
import datetime
from time import sleep
import os

#inter your uid and secret
uid = ""
secret = ""

token_post = requests.post("https://api.intra.42.fr/oauth/token", data={'grant_type':'client_credentials','client_id':uid,'client_secret':secret})
data = json.loads(token_post.text)
acto = data['access_token']

time = datetime.datetime.now()
time_str = time.strftime("%d.%m")
print ("Чекаем наличие свободных мест на сегодняшний ({}) экз:\n".format(time_str))

while (1):
    test = requests.get("https://api.intra.42.fr/v2/campus/17/exams", params={'access_token':acto})
    data3 = json.loads(test.text)
    for index in data3:
        if index['name'] == "C Exam Alone In The Dark - Beginner (Для СТУДЕНТОВ)":
            time_exam_str = index['begin_at']
            time_exam = datetime.datetime.strptime(time_exam_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            time_exam_str = time_exam.strftime("%d.%m")
            if time_exam_str == time_str:
                print ("{}/{}".format(index['nbr_subscribers'], index['max_people']))
                if index['nbr_subscribers'] < 120:
                    os.system("afplay music.mp3 &")
                    sleep(3)
                    os.system("killall  afplay")
    sleep(1)
