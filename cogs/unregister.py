# AFVA Bot Version 1.0.1
# By: Daniel Duhon
#
# Unregister Command Cog v1.0

import discord
import os
import asyncio
import logging as log

from discord.ext import commands
from . import botCommands as BC

helpText = "Use this function to unregister the user.\nUsage: '$unregister [OPTIONAL: @<member>]' (Only staff may unregister other users)."

# Unregister Cog
class Unregister(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='unregister', help=helpText)
    async def unregister(self, ctx, member: discord.Member=None):
        # Cog functionality
        if member is None:
            member = ctx.author

        memberID = str(member).split('#')[1]

        allowedRoles = [
            discord.utils.get(member.guild.roles, name="Fleet Staff"), 
            discord.utils.get(member.guild.roles, name="Senior Staff"), 
            discord.utils.get(member.guild.roles, name="Operations & Administrative Staff")
        ]

        if not any(role in ctx.author.roles for role in allowedRoles):
            member = ctx.author
        
        BC.unregUser(memberID)
        log.info(f"Unregistered {str(member)}")

async def setup(bot):
    await bot.add_cog(Unregister(bot))