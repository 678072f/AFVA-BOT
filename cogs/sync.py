# AFVA Bot Version 1.0.1
# By: Daniel Duhon
#
# Sync Command Cog v1.0

import discord
from discord.ext import commands
import os
import asyncio
import logging as log
import botCommands as BC

helpText = "Use this command to sync your roles with your AFVA Profile.\nUsage: '$sync [OPTIONAL: @<member>]' (Only staff may update other users)."


# Sync Cog
class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='sync', help=helpText)
    async def sync(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
    
        allowedRoles = [discord.utils.get(member.guild.roles, name="Fleet Staff"), discord.utils.get(member.guild.roles, name="Senior Staff"), discord.utils.get(member.guild.roles, name="Operations & Administrative Staff")]

        if not any(role in ctx.author.roles for role in allowedRoles):
            member = ctx.author

        id = str(member).split("#")[1]
        
        try:
            nickName, newRoles = BC.fetchUserInfo(id)
            log.debug(f"Received {nickName} and {newRoles} roles.")

        except TypeError:
            log.error("An error occurred! Check if the user is registered.")
            await ctx.channel.send("There was an error! If you get this message again, please register using $verify.")
            return

        log.info(f"{member} has the following roles: {newRoles}")

        if nickName is not None:
            try:
                if member.nick != nickName:
                    await member.edit(nick=nickName)
                    log.info(f"{member}'s nickname was updated to: {nickName}.")
                    await member.channel.send(f"Your nickname was updated to {nickName}")
                    
                else:
                    await ctx.channel.send(f"{member.mention}'s nickname is already up to date.")
                    log.info(f"{member}'s nickname was already up to date.")

            except discord.errors.Forbidden:
                log.error(f"The bot does not have permission to change {member}'s nickname! Please verify action and try again.")

        else:
            log.error(f"{member}'s nickname returned None! Try registering!")
            await ctx.channel.send(f"Your nickname was not found! Please register with '$verify' and try again!")

        if newRoles is not None:
            discordRoleList = []
            currentRoleList = member.roles
            ignoreRolesId = [BC.discordRoles["AFVA-Booster"], BC.discordRoles["AFVA-Shareholder"], BC.discordRoles["P1 - PPL"], BC.discordRoles["RW Pilot"], BC.discordRoles["CFI"], BC.discordRoles["DCFI"], BC.discordRoles["everyone"], BC.discordRoles["Senior Captain"], BC.discordRoles["Senior Staff"]]

            ignoreRoles = []
            for roleID in ignoreRolesId:
                ignoreRoles.append(discord.utils.get(member.guild.roles, id = roleID))

            for role in newRoles:
                discordRoleList.append(discord.utils.get(member.guild.roles, id = role))

            try:
                # Add new roles
                for role in discordRoleList:
                    if role not in member.roles:
                        await member.add_roles(role)

                # Remove old roles
                for role in currentRoleList:
                    if role not in discordRoleList and role not in ignoreRoles:
                        await member.remove_roles(role)

            except TypeError:
                log.error("An unknown error occurred!")

async def setup(bot):
    await bot.add_cog(Sync(bot))