import os
import random
from discord import embeds
from dotenv import load_dotenv
import sqlite3
import datetime
from discord.ext import commands
import discord
import asyncio
import sys
import requests
import numpy as np
from discord.utils import get
import discord
import psycopg2

intents = discord.Intents(messages=True, guilds=True)
intents.reactions = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
#TOKEN = os.getenv('TEMP_DISCORD_TOKEN')

bot = commands.Bot(command_prefix=["!"], intents=intents, case_insensitive=True)


# Ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    return await bot.change_presence(activity=discord.Activity(type=1, name="Hoarding artifacts"))


intital_extensions = ['cogs.trading']

if __name__ == '__main__':
    for extension in intital_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}', file=sys.stderr)
            print(e)


bot.run(TOKEN)