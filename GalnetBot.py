#!/usr/bin/python -u
# GalnetBot.py
import os
import json
#import sys
from dotenv import load_dotenv
import urllib.request
import time

last_time = 0

load_dotenv()
ENV_GALNET_URL = os.getenv('DISCORD_GALNET_URL')

def update():
  with urllib.request.urlopen(ENV_GALNET_URL) as url:
    json_load = json.load(url)

  for data in reversed(json_load['data']):
    id = data['id']

    with open('./known_articles.log') as file:
      if id not in file.read():
        article = data['attributes']
        date = article['field_galnet_date']
        title = article['title']
        body = article['body']['value']

        print("New Article:")
        print('ID: ' + id + '\n')
        print('Galnet News from ' + date)
        print(title + '\n')
        print(body)
        print('\n\n')

        with open('./known_articles.log', 'a') as file:
          file.write(id + '\n')


while True:
  if time.time() >= last_time + 60:
    print('Updating...')
    update()
    last_time = time.time()
    print('done')
  time.sleep(1)
