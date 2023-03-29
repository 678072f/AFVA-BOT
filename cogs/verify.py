# AFVA Bot Version 1.0.1
# By: Daniel Duhon
#
# Verify Command Cog v1.0

import discord
from discord.ext import commands
import os
import botCommands as BC
import asyncio
import logging as log

helpText = "Use this account to register your discord account with your AFVA profile.\nUsage: '$verify' - You MUST react to the message contaning the link with :thumbsup:"

# Verify Cog
class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='verify', help=helpText)
    async def unregister(self, ctx):
        pass

async def setup(bot):
    await bot.add_cog(Verify(bot))
