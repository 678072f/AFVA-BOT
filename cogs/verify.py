# AFVA Bot Version 1.0.1
# By: Daniel Duhon
#
# Verify Command Cog v1.0

import discord
import os
import asyncio
import logging as log

from discord.ext import commands
from . import botCommands as BC

LOG = log.getLogger(__name__)
helpText = "Use this account to register your discord account with your AFVA profile.\nUsage: '$verify' - You MUST react to the message contaning the link with :thumbsup:"

# Verify Cog
class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='verify', help=helpText)
    async def verify(self, ctx):
        member = ctx.author
        username = str(member).split("#")[0]
        id = str(member).split('#')[1]
        reactionList = ['👍', '👍🏻', '👍🏼', '👍🏽', '👍🏾', '👍🏿']

        # Respond to the user with a welcome message and send the verification link:
        await ctx.channel.send(f"Hello {username}, I am sending you to the verification link.")
        await ctx.channel.send(f'Please open: {BC.registrationURL + str(id)} to register your account, then react with 👍 within 2 minutes. (If you get a timeout error, type $verify again and add the reaction).')

        log.info(f"Sent verification link to {username}.")

        # Define function to check for thumbsup reaction
        def check(reaction, user):
            react = None
            for i in reactionList:
                if str(reaction.emoji) == i:
                    react = i
                    break
                
            return user == member and str(reaction.emoji) == react

        try:
            # Check for the user's reaction
            reaction, user = await ctx.channel.wait_for('reaction_add', timeout=120.0, check=check)
            # Store the user's nickname and roles from the verification Function
            
            try:
                runUpdate = asyncio.create_task(BC.fetchUserInfo(id))
                nickName, roleList = await runUpdate
                LOG.debug(f"Received {nickName} and {roleList} roles.")
            except TypeError:
                await ctx.channel.send(f"Error! {member} is not registered.\nPlease use $verify again and register using the link provided.")
                LOG.error(f"Verification Error! {member} is not registered.")
                return

            if roleList:
                # Iterate through the roles provided from the server
                for afvaRole in roleList:
                    # Check if the role exists and store in 'role'
                    role = discord.utils.get(member.guild.roles, id = int(afvaRole))

                    # Check if the user already has the role. If yes, skip
                    if role in member.roles:
                        LOG.info(f"You already have the {role} role! Moving on...")
                        print(f"You already have the {role} role! Moving on...")
                    # If the user doesn't already have the role, add it
                    else:
                        # Make sure the role exists
                        if role is not None:
                            await member.add_roles(role)
                            LOG.info(f"Added {role} role to {member}.")
                            print(f"Added {role} role.")
                        
                        # Send a message if the role isn't available
                        else:
                            LOG.warning(f"The {role} role was not found on this server!")
                            print(f"The {role} role was not found on this server!")
                
                    # Store the ID of the New Pilot role
                    npRole = discord.utils.get(member.guild.roles, name="New Pilot")
                    
                    # Check if the user has the New Pilot role and remove it if verified.
                    if npRole in member.roles:
                        await member.remove_roles(npRole)
                        LOG.info(f"Removed New Pilot role from {member}")

            else:
                LOG.info(f"Error! The roleList is empty!")

            # Respond with user's new nickname
            if nickName is not None:
                await ctx.channel.send(f"Success! Hello {nickName}")
                LOG.info('User successfully verified.')

        # Catch timeout
        except asyncio.TimeoutError:
            nickName = None
            await ctx.channel.send('Timeout Error! You did not react within 2 minutes. Please try again.')
            LOG.warning('Timeout Error! Please try again. User did not respond within 2 minutes.')

        # Update Nickname
        if nickName is not None:
            try:
                await member.edit(nick=nickName)
                LOG.info(f"{member}'s nickname was updated to: {nickName}.")
            except discord.errors.Forbidden:
                LOG.error(f"The bot does not have permission to change {member}'s nickname! Please verify action and try again.")

async def setup(bot):
    await bot.add_cog(Verify(bot))
