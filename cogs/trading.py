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


# TODO: Make a !order command to actually order stuff (!order <amount> <type>)
# TODO: Make a !accept command to show that a user has accepted the trade (make sure they have the rs level)
# TODO: Make a !cancel commmand to cancel an order 
# TODO: Make a !complete command to complete an order
class RSQueue(commands.Cog, name='Trading'):

    def __init__(self, bot):
        self.bot = bot
        self.trading_channel = {
            "rs6-trading" : 6,
            "rs7-trading" : 7,
            "rs8-trading" : 8,
            "rs9-trading" : 9,
            "rs10-trading" : 10,
            "rs11-trading" : 11,
        }
        self.rs11_trades = {
            'tets' : {'rs10' : 8.0, 'rs9' : 5.0, 'rs8' : 11.0, 'rs7' : 14.0, 'rs6' : 24.0},
            'crys' : {'rs10' : 4.5, 'rs9' : 4.5, 'rs8' : 6.0, 'rs7' : 8.0, 'rs6' : 12.0},
            'orbs' : {'rs10' : 4.5, 'rs9' : 4.5, 'rs8' : 6.0, 'rs7' : 8.0, 'rs6' : 12.0}
        }
        self.rs10_trades = {
            'tets' : {'rs9' : 5.0, 'rs8' : 6.0, 'rs7' : 7.0, 'rs6' : 8.0, 'rs5' : 10.0, 'rs4' : 14.0},
            'crys' : {'rs9' : 4.0, 'rs8' : 4.5, 'rs7' : 5.5, 'rs6' : 6.5, 'rs5' : 8.0, 'rs4' : 11.0},
            'orbs' : {'rs9' : 3.0, 'rs8' : 3.5, 'rs7' : 4.5, 'rs6' : 5.5, 'rs5' : 7.0, 'rs4' : 9.0}
        }
        self.rs9_trades = {
            'tets' : {'rs8' : 2.5, 'rs7' : 3.0, 'rs6' : 4.0, 'rs5' : 5.5, 'rs4' : 6.5 },
            'crys' : {'rs8' : 2.0, 'rs7' : 2.5, 'rs6' : 3.5, 'rs5' : 5.0, 'rs4' : 6.0},
            'orbs' : {'rs8' : 2.0, 'rs7' : 2.5, 'rs6' : 3.5, 'rs5' : 5.0, 'rs4' : 6.0}
        }
        self.rs8_trades = {
            'tets' : { 'rs7' : 2.0, 'rs6' : 2.5, 'rs5' : 3.5, 'rs4' : 5.0},
            'crys' : { 'rs7' : 2.0, 'rs6' : 2.5, 'rs5' : 3.5, 'rs4' : 5.0},
            'orbs' : { 'rs7' : 2.0, 'rs6' : 2.5, 'rs5' : 3.5, 'rs4' : 5.0}
        }
        self.rs7_trades = {
            'tets' : {'rs6' : 2.0, 'rs5' : 2.5, 'rs4' : 3.0},
            'crys' : {'rs6' : 2.0, 'rs5' : 2.5, 'rs4' : 3.0},
            'orbs' : {'rs6' : 2.0, 'rs5' : 2.5, 'rs4' : 3.0}
        }
        self.rs6_trades = {
            'tets' : { 'rs5' : 2.0, 'rs4' : 2.5},
            'crys' : { 'rs5' : 2.0, 'rs4' : 2.5},
            'orbs' : { 'rs5' : 2.0, 'rs4' : 2.5}
        }
        self.all_trades = {
            'rs6' : self.rs6_trades,
            'rs7' : self.rs7_trades,
            'rs8' : self.rs8_trades,
            'rs9' : self.rs9_trades,
            'rs10' : self.rs10_trades,
            'rs11' : self.rs11_trades,
        }

    def right_channel(self, ctx):
        for club_channel in self.trading_channel:
            if club_channel == str(ctx.message.channel) or str(ctx.channel) == 'bot-spam':
                return True
        return False


    @commands.command(aliases=["r"])
    async def rates(self, ctx, level=None, quantity=1):
        if self.right_channel(ctx):
            if level is not None and int(level) <= 11 and int(level) >= 5:
                # Send the embed
                rates_embed = discord.Embed(title=f"1x RS{level} Rates", color=discord.Color.green())
                total_string = "```RS#..........Tets| Crys| Orbs\n"
                if int(level) == 11:
                    for rs_level in range(int(level)-1, 5, -1):
                        total_string += f"RS{rs_level}"
                        total_string += "."*(14-len(str(quantity * self.all_trades[f'rs{level}']['tets'][f'rs{rs_level}']))) + str(quantity * self.all_trades[f'rs{level}']['tets'][f'rs{rs_level}']) + "|"
                        total_string += "."*(5-len(str(quantity * self.all_trades[f'rs{level}']['crys'][f'rs{rs_level}']))) + str(quantity * self.all_trades[f'rs{level}']['crys'][f'rs{rs_level}']) + "|"
                        total_string += "."*(5-len(str(quantity * self.all_trades[f'rs{level}']['orbs'][f'rs{rs_level}']))) + str(quantity * self.all_trades[f'rs{level}']['orbs'][f'rs{rs_level}'])
                        total_string += "\n"
                else:
                    for rs_level in range(int(level)-1, 3, -1):
                        total_string += f"RS{rs_level}"
                        total_string += "."*(14-len(str(quantity * self.all_trades[f'rs{level}']['tets'][f'rs{rs_level}']))) + str(quantity * self.all_trades[f'rs{level}']['tets'][f'rs{rs_level}']) + "|"
                        total_string += "."*(5-len(str(quantity * self.all_trades[f'rs{level}']['crys'][f'rs{rs_level}']))) + str(quantity * self.all_trades[f'rs{level}']['crys'][f'rs{rs_level}']) + "|"
                        total_string += "."*(5-len(str(quantity * self.all_trades[f'rs{level}']['orbs'][f'rs{rs_level}']))) + str(quantity * self.all_trades[f'rs{level}']['orbs'][f'rs{rs_level}'])
                        total_string += "\n"
                total_string += "```"
                rates_embed.add_field(name='\u200b', value=total_string)
                await ctx.send(embed=rates_embed)
            else:
                await ctx.send("RS Level not specified for rates, and must be between 5 and 11 (and an optional quantity if you want)")
        else:
            await ctx.send("Command not run in a RS Trading channel (or bot-spam)")

    @commands.command(aliases=["o"])
    async def order(self, ctx, quantity, giving_level, option):
        if self.right_channel(ctx):
            #self.trading_channel[str(ctx.message.channel)])
            # Find the amount of arts they need to give
            # Option can be any combination of c, o, t (co, ct, ot, cot)
            # TODO: implement option to be multiple params
            type_of_art = "crys" if option == 'c' else "orbs" if option == 'o' else "tets" if option == 't' else ""
            full_art_name = "Blue Crystals" if option == 'c' else "Orbs" if option == 'o' else "Tetrahedrons" if option == '' else ""
            exchange_rate = self.all_trades[f"rs{self.trading_channel[str(ctx.message.channel)]}"][type_of_art][f"rs{giving_level}"]
            recieving_arts = int(quantity) / int(exchange_rate)
            # send a message confirming it with reaction to a check or x emoji (probably make it spicy with an embed)
            message = await ctx.send(f"{ctx.author.mention} Confirm your trade: {int(quantity) - (int(quantity) % int(exchange_rate))} RS{giving_level} arts for {int(recieving_arts)} RS{self.trading_channel[str(ctx.message.channel)]} {full_art_name} (exchange rate is {exchange_rate} RS{giving_level} arts per RS{self.trading_channel[str(ctx.message.channel)]}")
            await message.add_reaction('✅')
            await message.add_reaction('❌')
        else:
            await ctx.send("Command not run in a RS Trading channel (or bot-spam)")







def setup(bot):
    bot.add_cog(RSQueue(bot))
    print('Trading loaded')