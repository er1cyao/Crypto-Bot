#crypto bot
import os
import discord
from discord.ext import commands
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pycoingecko import CoinGeckoAPI
from datetime import datetime
from yahooquery import Screener

client = discord.Client()
now = datetime.now()
removeYear = now.year - 10
current_date = datetime.today().strftime('%Y-%m-%d')
date_arr = current_date.split('-')
past = str(removeYear) + '-' + date_arr[1] + '-' + date_arr[2]


intents = discord.Intents.all()
intents.members = True 
intents.presences = True
bot = commands.Bot(command_prefix='!', intents = intents)

def read_token():
    with open('bot.txt', 'r') as f:
        lines = f.readline()
        return(lines)

token = read_token()

s = Screener()
data = s.get_screeners('all_cryptocurrencies_us', count=250)

dicts = data['all_cryptocurrencies_us']['quotes']
symbols = [d['symbol'] for d in dicts]
symbols

crydata = yf.download(symbols, start = past, end = now)

class Crypto:
    def __init__(self,name):
        self.name = name.lower()
    
    def generate_graph(name):
        cry_adjclose = crydata['Adj Close']

        if name in symbols:
            plt.plot(cry_adjclose[name])
            image_name = name 
            plt.savefig(image_name)
            return(image_name + ".png")
            
            
    def generate_name(input):
        if input in symbols:
            return input
       
        
# events for the bot to process and run
@client.event
async def on_ready():
    print('Connected!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    for i in symbols:
        if message.content.startswith("!" + i):
            await message.channel.send(file = discord.File(str(Crypto.generate_graph(i))))
            print("working")





client.run(token)






