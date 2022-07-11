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


client= commands.Bot(command_prefix='!')

now = datetime.now()
removeYear = now.year - 5
current_date = datetime.today().strftime('%Y-%m-%d')
date_arr = current_date.split('-')
past = str(removeYear) + '-' + date_arr[1] + '-' + date_arr[2]


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
            plt.title(name)
            image_name = name 
            plt.savefig(image_name)
            return(image_name + ".png")
            
            
    def generate_returns(name):        
        plt.plot(returns[name])
        plt.title(name)
        plt.savefig(name + "returns")
        return(name + "returns.png")
    
    def compare_cumulative(first, second):
        arr = [first,second]
        if first and second in symbols:
            com_data = yf.download(arr, start = past, end = now)
            cum_returns = ((1 + com_data['Adj Close'].pct_change()).cumprod() - 1) * 100
            cum_returns.plot(figsize = (20,6))
            plt.title(first + " " + second + " Cumulative Returns")
            plt.savefig(first + "_" + second)
            return(first + "_" + second + ".png")

    def generate_heatmap(arr):
        heat = arr
        if arr[0] and arr[1] and arr[2] and arr[3] in symbols:
            heat_data = yf.download(heat, start = past, end =now)
            heat_corr = (((1 + heat_data['Adj Close'].pct_change()).cumprod() - 1) * 100).corr()
            sns.heatmap(heat_corr, annot = True, cmap = 'coolwarm')
            plt.title("Heat Map of Selected Cryptocurrencies")
            plt.savefig("HeatMap" +str(arr))
            return("HeatMap" +str(arr) +".png")

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
            
    for i in symbols:
        for j in symbols:
            if message.content.startswith("!cumulative" + i + " " + j):
                await message.channel.send(file = discord.File(str(Crypto.compare_cumulative(i,j))))
    
    await client.process_commands(message)

@client.command()
async def test(ctx,arg):
    await ctx.channel.send(arg)

@client.command()
async def heatmap(ctx):

    await ctx.send("enter four cryptocurrencies for heatmap comparisons")
    
    def split_string(string):
        a = string.split(",")
        return a
    
    def check_author(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    response = await client.wait_for("message",check=check_author)
    values_given = split_string(response.content)

    if (values_given)[0] in symbols and  (values_given)[1] in symbols and (values_given)[2] in symbols and \
    (values_given)[3] in symbols:    
        await ctx.send(file = discord.File(str(Crypto.generate_heatmap(values_given))))
    
    else:
        await ctx.send("Please choose four viable cryptocurrencies")


client.run(token)



