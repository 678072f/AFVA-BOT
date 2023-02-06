# AFVA Bot Version 1.0
# By: Daniel Duhon

# This example requires the 'message_content' intent.

import discord
import os
import requests
import json
from dotenv import load_dotenv

client = discord.Bot()
token = os.getenv('TOKEN')

@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))



def get_user():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return
            
        print(f'Message from {message.author}: {message.content}')
        
        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')
            
        if message.content.startswith('$inspire'):
            await message.channel.send(get_user())

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

client.run(token)

# os.getenv('TOKEN')
# 9059765248
# TOKEN = 'MTAzMzg0OTgxODMxOTE3NTczMA.GjM9v1.biTbqYkCrMDuDLYFF0GKUYmPqPooBg4Wcgpda4'
