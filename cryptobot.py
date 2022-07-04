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
data = s.get_screeners('all_cryptocurrencies_us', count = 250)
dicts = data['all_cryptocurrencies_us']['quotes']
symbols = [d['symbol'] for d in dicts]


class Crypto:
    def __init__(self,name):
        self.name = name.lower()
    
    def generate_graph(name):
        cryptocurrencies = symbols
        crydata = yf.download(cryptocurrencies, start = past, end = now)
        cry_adjclose = crydata['Adj Close']

        if name in cryptocurrencies:
            plot = plt.plot(cry_adjclose[name])
            
        
       
        
Crypto.generate_graph("BTC-USD")


@client.event
async def on_ready():
    print('Connected!')














