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
import yahoo_fin.stock_info as si


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
data = s.get_screeners('all_cryptocurrencies_us', count=200)

dicts = data['all_cryptocurrencies_us']['quotes']
symbols = [d['symbol'] for d in dicts]
symbols

crydata = yf.download(symbols, start = past, end = now)
cry_adjclose = crydata['Adj Close']
returns = crydata['Adj Close'].pct_change()
class Crypto:
    def __init__(self,name):
        self.name = name.lower()
    
    def generate_graph(name):
        if name in symbols:
            plt.plot(cry_adjclose[name])
            image_name = name 
            plt.savefig(image_name)
            return(image_name + ".png")
            
            
    def generate_returns(name):
        
        plt.plot(returns[name])
        plt.savefig(name + "returns")
        return(name + "returns.png")
    
    def compare_cumulative(first, second):
        cum_returns = ((1 + crydata['Adj Close'].pct_change()).cumprod() - 1) * 100


   

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

        if message.content.startswith("!returns " + i):
            await message.channel.send(file = discord.File(str(Crypto.generate_returns(i))))



client.run(token)






