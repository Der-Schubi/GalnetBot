#!/usr/bin/python -u
# GalnetBot.py
import json
import os
import time
import urllib.request

from dotenv import load_dotenv

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
        if article['langcode'] == 'de':
          date = article['field_galnet_date']
          title = article['title']
          body = article['body']['value']

          print("New Article:")
          print('ID: ' + id + '\n')
          print('Length: ' + str(len(body)))
          print('Galnet News from ' + date)
          print(title + '\n')

          pos = 0
          while pos >= 0:
            if len(body) > 2000:
              pos = body.rfind('\r\n', 0, 2000)
              if pos == -1:
                pos = body.rfind(' ', 0, 2000)
                skip = 1
              else:
                skip = 2
              chunk = body[0:0 + pos]
              body = body[pos + 1 + skip:]
            else:
              pos = -1
              chunk = body

            print(chunk)
            print('\n')

          with open('./known_articles.log', 'a') as file:
            file.write(id + '\n')


while True:
  if time.time() >= last_time + 60:
    print('Updating...')
    update()
    last_time = time.time()
    print('done')
  time.sleep(1)
