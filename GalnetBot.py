#!/usr/bin/python -u
# GalnetBot.py
import disnake
import json
import os
import time
import urllib.request

from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()
ENV_TOKEN = os.getenv('DISCORD_TOKEN')
ENV_GUILD = os.getenv('DISCORD_GUILD')
ENV_CHANNEL = os.getenv('DISCORD_CHANNEL')
ENV_STATUS = os.getenv('DISCORD_STATUS')
ENV_GALNET_URL = os.getenv('DISCORD_GALNET_URL')

bot = commands.Bot(
  command_prefix='/',
  intents=disnake.Intents.all(),
  help_command=None,
  #sync_commands_debug=True,
)

async def update():
  with urllib.request.urlopen(ENV_GALNET_URL) as url:
    json_load = json.load(url)

  for data in reversed(json_load['data']):
    guild = disnake.utils.get(bot.guilds, name=ENV_GUILD)
    channel = disnake.utils.get(guild.channels, name=ENV_CHANNEL)

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

          post = 'GalNet News vom ' + date + '\n__**' + title + '**__\n\n' + body

          pos = 0
          while pos >= 0:
            if len(post) > 2000:
              pos = post.rfind('\r\n', 0, 2000)
              if pos == -1:
                pos = post.rfind(' ', 0, 2000)
                skip = 1
              else:
                skip = 2
              chunk = post[0:0 + pos]
              post = post[pos + 1 + skip:]
            else:
              pos = -1
              chunk = post

            print(chunk)
            print('\n')
            await channel.send(f'{chunk}')

          with open('./known_articles.log', 'a') as file:
            file.write(id + '\n')

@bot.event
async def on_ready():
  guild = disnake.utils.get(bot.guilds, name=ENV_GUILD)
  print(
    f'{bot.user} is connected to the following Guild:\n'
    f'{guild.name}(id: {guild.id})\n'
  )
  await bot.change_presence(activity=disnake.Game(name=ENV_STATUS))
  await update()
  last_time = time.time()
  while True:
    if time.time() >= last_time + 60:
      await update()
      last_time = time.time()

bot.run(ENV_TOKEN)


