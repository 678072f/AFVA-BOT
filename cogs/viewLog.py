# AFVA Bot Version 1.0.1
# By: Daniel Duhon
#
# Log Command Cog v1.0

import discord
import os
import asyncio
import logging as log

from discord.ext import commands
from . import botCommands as BC


helpText = "Use this function to view the log (IT only).\nUsage: '$log'"

# Log Cog
class ViewLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='log', help=helpText)
    async def log(self, ctx):
        member = ctx.author
        currentLog = BC.displayLog()

        allowedRoles = [discord.utils.get(member.guild.roles, name = "IT"), discord.utils.get(member.guild.roles, name = "Senior Staff"), discord.utils.get(member.guild.roles, name = "Operations & Administrative Staff")]

        for role in allowedRoles:
            if role in ctx.author.roles:
                with open(str(currentLog), 'r') as l:
                    logContents = l.read(1992).strip()
                    while len(logContents) > 0:
                        await ctx.channel.send(f"``` {logContents} ```")
                        logContents = l.read(1992).strip()
                break

async def setup(bot):
    await bot.add_cog(ViewLog(bot))