# AFVA Bot Version 1.0
# By: Daniel Duhon

# This example requires the 'message_content' intent.

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import botCommands as BC
import asyncio
import logging as log
import datetime
import schedule
import time

# Global Constants
load_dotenv()
token = os.getenv('DEV_TOKEN')
registrationURL = 'https://www.afva.net/discordreg.do?id='
currentTime = str(datetime.datetime.now()).split(' ')[0]

# Set up Logging
log.basicConfig(
    filename='afva-bot-%s.log' % currentTime,
    filemode='w',
    level=log.DEBUG, ### Change to INFO when releasing ###
    format='%(levelname)s:%(asctime)s:%(message)s'
)

# Setup Discord
intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix="$", intents=intents)


# User verification
@bot.command(name="verify")
async def verifyUser(ctx):
    member = ctx.author
    username = str(member).split("#")[0]
    id = str(member).split("#")[1]

    # Respond to the user with a welcome message and send the verification link:
    await ctx.channel.send(f"Hello {username}, I am sending you to the verification link.")
    await ctx.channel.send(f'Please open: {registrationURL + id} to register your account, then react with 👍 within 2 minutes. (If you get a timeout error, type $verify again and add the reaction).')

    log.info(f"Sent verification link to {username}.")

    # Define function to check for thumbsup reaction
    def check(reaction, user):
        return user == member and str(reaction.emoji) == '👍'

    try:
        # Check for the user's reaction
        reaction, user = await bot.wait_for('reaction_add', timeout=120.0, check=check)
        # Store the user's nickname and roles from the verification Function
        
        try:
            nickName, roleList = BC.fetchUserInfo(id)
            log.debug(f"Received {nickName} and {roleList} roles.")
        except TypeError:
            await ctx.channel.send(f"Error! {member} is not registered.\nPlease use !verify again and register using the link provided.")
            log.error(f"Verification Error! {member} is not registered.")
            return

        if roleList:
            # Iterate through the roles provided from the server
            for afvaRole in roleList:
                # Check if the role exists and store in 'role'
                role = discord.utils.get(member.guild.roles, id = int(afvaRole))

                # Check if the user already has the role. If yes, skip
                if role in member.roles:
                    log.info(f"You already have the {role} role! Moving on...")
                    print(f"You already have the {role} role! Moving on...")
                # If the user doesn't already have the role, add it
                else:
                    # Make sure the role exists
                    if role is not None:
                        await member.add_roles(role)
                        log.info(f"Added {role} role to {member}.")
                        print(f"Added {role} role.")
                    
                    # Send a message if the role isn't available
                    else:
                        log.warning(f"The {role} role was not found on this server!")
                        print(f"The {role} role was not found on this server!")
            
                # Store the ID of the New Pilot role
                npRole = discord.utils.get(member.guild.roles, id=int(BC.discordRoles["New Pilot"]))
                
                # Check if the user has the New Pilot role and remove it if verified.
                if npRole in member.roles:
                    await member.remove_roles(npRole)
                    log.info(f"Removed New Pilot role from {member}")

        else:
            log.info(f"Error! The roleList is empty!")

        # Respond with user's new nickname
        if nickName is not None:
            await ctx.channel.send(f"Success! Hello {nickName}")
            log.info('User successfully verified.')

    # Catch timeout
    except asyncio.TimeoutError:
        nickName = None
        await ctx.channel.send('Timeout Error! You did not react within 2 minutes. Please try again.')
        log.warning('Timeout Error! Please try again. User did not respond within 2 minutes.')

    # Update Nickname
    if nickName is not None:
        try:
            await member.edit(nick=nickName)
            log.info(f"{member}'s nickname was updated to: {nickName}.")
        except discord.errors.Forbidden:
            log.error(f"The bot does not have permission to change {member}'s nickname! Please verify action and try again.")


# Role Sync
@bot.command(name="sync")
async def syncRoles(ctx, member: discord.Member=None):
    if member is None:
        member = ctx.message.author

    id = str(member).split("#")[1]
    
    try:
        nickName, newRoles = BC.fetchUserInfo(id)
        log.debug(f"Received {nickName} and {newRoles} roles.")

    except TypeError:
        log.error("An error occurred! Check if the user is registered.")
        await ctx.channel.send("There was an error! If you get this message again, please register using !verify.")
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
        await ctx.channel.send(f"Your nickname was not found! Please register with '!verify' and try again!")

    if newRoles is not None:
        discordRoleList = []
        currentRoleList = member.roles
        ignoreRolesId = [BC.discordRoles["AFVA-Booster"], BC.discordRoles["AFVA-Shareholder"], BC.discordRoles["P1 - PPL"], BC.discordRoles["RW Pilot"], BC.discordRoles["CFI"], BC.discordRoles["DCFI"], BC.discordRoles["everyone"], BC.discordRoles["Senior Captain"]]

        ignoreRoles = []
        for roleID in ignoreRolesId:
            ignoreRoles.append(ctx.guild.roles, id = roleID)

        for role in newRoles:
            discordRoleList.append(discord.utils.get(member.guild.roles, id = role))

        try:
            for role in discordRoleList:
                if role not in member.roles:
                    await member.add_roles(role)

            for role in currentRoleList:
                if role not in discordRoleList and role not in ignoreRoles:
                    await ctx.send(role)
                    await member.remove_roles(role)

        except TypeError:
            log.error("An unknown error occurred!")

# Event Handlers
@bot.event
async def on_ready():
    log.info("Logged in as a bot {0.user}".format(bot))
    print("Logged in as a bot {0.user}".format(bot))

# Event for sending welcome message to users
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="new-members")
    embedJoin = channel.Embed(title=f"Welcome to Air France/KLM Virtual Airlines, @{member}!", description="This is a place for AFVA Members to get together and chat about our experiences and help each other.\n\n Please visit the #rules channel to see the rules for the server.\n\n Most importantly, please continue to have fun!\n\n Also, you may verify your account by typing !verify in #verification, or type ?help? to see a list of options.", color=0x000000)
    await channel.send(embed=embedJoin)


# Function to clear verification channel
async def clearChannel(channelToBeCleared):
    channel = discord.utils.get(bot.guild.text_channels, name=channelToBeCleared)
    try:
        await channel.purge()
        log.info(f"Clearing {channelToBeCleared}...")
    except:
        log.error(f"An error occurred when trying to clear {channelToBeCleared}!")

# Verification channel name
verChannel = "verification"

# Clear the channel every friday at 23:59
schedule.every().week.friday.at("23:59").do(clearChannel, verChannel)

# Run the bot
bot.run(token)