import os
import random
from sqlite3.dbapi2 import DatabaseError
from typing import final
from discord import channel, embeds, message
from dotenv import load_dotenv
import sqlite3
import datetime
from discord.ext import commands, tasks
import discord
import asyncio
import sys
import requests
import numpy as np
from discord.utils import get
from datetime import datetime
from discord.ext.commands import Cog, command
import time

class RSQueue(commands.Cog, name='Trading'):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Bonjour")




def setup(bot):
    bot.add_cog(RSQueue(bot))
    print('Trading loaded')