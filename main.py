# AFVA Bot Version 1.0.1
# By: Daniel Duhon

# This example requires the 'message_content' intent.

import discord
from discord.ext import commands
import os
# import cogs.botCommands as BC
import asyncio
import logging as log
import datetime
import schedule
import time
import dotenv # DEV ONLY

# Global Constants
dotenv.load_dotenv() # DEV ONLY
token = os.getenv('TOKEN')
registrationURL = os.getenv('REG_URL')
currentTime = str(datetime.datetime.now()).split(' ')[0]

helpText = [
    "Use this account to register your discord account with your AFVA profile.\nUsage: '$verify' - You MUST react to the message contaning the link with :thumbsup:",
    "Use this function to view the log (IT only).\nUsage: '$log'"
]

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

client = commands.Bot(command_prefix="$", intents=intents)
client.remove_command('help')

# Load Cogs
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            if filename != 'botCommands.py':
                await client.load_extension(f"cogs.{filename[:-3]}")

# User verification
@client.command(name="verify1", help=helpText[0])
async def verifyUser(ctx):
    member = ctx.author
    username = str(member).split("#")[0]
    id = str(member).split('#')[1]
    reactionList = ['👍', '👍🏻', '👍🏼', '👍🏽', '👍🏾', '👍🏿']

    # Respond to the user with a welcome message and send the verification link:
    await ctx.channel.send(f"Hello {username}, I am sending you to the verification link.")
    await ctx.channel.send(f'Please open: {registrationURL + str(id)} to register your account, then react with 👍 within 2 minutes. (If you get a timeout error, type $verify again and add the reaction).')

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
        reaction, user = await bot.wait_for('reaction_add', timeout=120.0, check=check)
        # Store the user's nickname and roles from the verification Function
        
        try:
            nickName, roleList = BC.fetchUserInfo(id)
            log.debug(f"Received {nickName} and {roleList} roles.")
        except TypeError:
            await ctx.channel.send(f"Error! {member} is not registered.\nPlease use $verify again and register using the link provided.")
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
                npRole = discord.utils.get(member.guild.roles, name="New Pilot")
                
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


# Role Sync, fetches data from server and compares to current roles and nickName
# @client.command(name="sync", help=helpText[1])
# async def syncRoles(ctx, member: discord.Member=None):
#     if member is None:
#         member = ctx.author
    
#     allowedRoles = [discord.utils.get(member.guild.roles, name="Fleet Staff"), discord.utils.get(member.guild.roles, name="Senior Staff"), discord.utils.get(member.guild.roles, name="Operations & Administrative Staff")]

#     if not any(role in ctx.author.roles for role in allowedRoles):
#         member = ctx.author

#     id = str(member).split("#")[1]
    
#     try:
#         nickName, newRoles = BC.fetchUserInfo(id)
#         log.debug(f"Received {nickName} and {newRoles} roles.")

#     except TypeError:
#         log.error("An error occurred! Check if the user is registered.")
#         await ctx.channel.send("There was an error! If you get this message again, please register using $verify.")
#         return

#     log.info(f"{member} has the following roles: {newRoles}")

#     if nickName is not None:
#         try:
#             if member.nick != nickName:
#                 await member.edit(nick=nickName)
#                 log.info(f"{member}'s nickname was updated to: {nickName}.")
#                 await member.channel.send(f"Your nickname was updated to {nickName}")
                
#             else:
#                 await ctx.channel.send(f"{member.mention}'s nickname is already up to date.")
#                 log.info(f"{member}'s nickname was already up to date.")

#         except discord.errors.Forbidden:
#             log.error(f"The bot does not have permission to change {member}'s nickname! Please verify action and try again.")

#     else:
#         log.error(f"{member}'s nickname returned None! Try registering!")
#         await ctx.channel.send(f"Your nickname was not found! Please register with '$verify' and try again!")

#     if newRoles is not None:
#         discordRoleList = []
#         currentRoleList = member.roles
#         ignoreRolesId = [BC.discordRoles["AFVA-Booster"], BC.discordRoles["AFVA-Shareholder"], BC.discordRoles["P1 - PPL"], BC.discordRoles["RW Pilot"], BC.discordRoles["CFI"], BC.discordRoles["DCFI"], BC.discordRoles["everyone"], BC.discordRoles["Senior Captain"], BC.discordRoles["Senior Staff"]]

#         ignoreRoles = []
#         for roleID in ignoreRolesId:
#             ignoreRoles.append(discord.utils.get(member.guild.roles, id = roleID))

#         for role in newRoles:
#             discordRoleList.append(discord.utils.get(member.guild.roles, id = role))

#         try:
#             # Add new roles
#             for role in discordRoleList:
#                 if role not in member.roles:
#                     await member.add_roles(role)

#             # Remove old roles
#             for role in currentRoleList:
#                 if role not in discordRoleList and role not in ignoreRoles:
#                     await member.remove_roles(role)

#         except TypeError:
#             log.error("An unknown error occurred!")


# Reads current log file and outputs it as a message
@client.command(name="log1", help=helpText[1])
async def viewLog(ctx):
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


# # Unregisters user by sending a GET request to the unregister URI
# @bot.command(name="unregister", help=helpText[3])
# async def unregUser(ctx, member: discord.Member=None):
#     if member is None:
#         member = ctx.author

#     allowedRoles = [discord.utils.get(member.guild.roles, name="Fleet Staff"), discord.utils.get(member.guild.roles, name="Senior Staff"), discord.utils.get(member.guild.roles, name="Operations & Administrative Staff")]

#     if not any(role in ctx.author.roles for role in allowedRoles):
#         member = ctx.author
    
#     BC.unregUser(member.id)


# Event Handlers
@client.event
async def on_ready():
    log.info("Logged in as a bot {0.user}".format(client))
    print("Logged in as a bot {0.user}".format(client))


# Event for sending welcome message to users
@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="new-members")
    embedJoin = discord.Embed(title=f"Welcome to Air France/KLM Virtual Airlines, {member.mention}! :flag_fr: :flag_fr:", description=f"Please visit the #rules channel to see the rules for the server.\n\n Most importantly, please continue to have fun!\n\n Also, you may verify your account by typing `$verify` in #verification, or type `$help` to see a list of options.", color=0x0b228c)
    await channel.send(embed=embedJoin)


# Function to clear verification channel
def clearChannel(channelToBeCleared):
    channel = discord.utils.get(client.guild.text_channels, name=channelToBeCleared)
    try:
        channel.purge()
        log.info(f"Clearing {channelToBeCleared}...")
    except:
        log.error(f"An error occurred when trying to clear {channelToBeCleared}!")


# Verification channel name
verChannel = "verification"

# Clear the channel every friday at 23:59
schedule.every().week.friday.at("23:59").do(clearChannel, verChannel)

# Setup Main Function
async def main():
    async with client:
        await load_extensions()
        await client.start(token)

# Run the bot
asyncio.run(main())