# AFVA Bot Version 1.0
# By: Daniel Duhon

# This example requires the 'message_content' intent.

import discord
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
token = os.getenv('TOKEN')
registrationURL = 'https://dev.afva.net/discordreg.do?id='
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

async def verifyUser(message, username, id):
    member = message.author

    # Respond to the user with a welcome message and send the verification link:
    await message.channel.send(f"Hello {username}, I am sending you to the verification link.")
    await message.channel.send(f'Please open: {registrationURL + id} to register your account, then react with 👍.')

    log.info(f"Sent verification link to {username}.")

    # Define function to check for thumbsup reaction
    def check(reaction, user):
        return user == message.author and str(reaction.emoji) == '👍'

    try:
        # Check for the user's reaction
        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
        # Store the user's nickname and roles from the verification Function
        nickName, roleList = BC.fetchUserInfo(id)
        log.debug(f"Received {nickName} and {roleList} roles.")

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
            await message.channel.send(f"Success! Hello {nickName}")
            log.info('User successfully verified.')

    # Catch timeout
    except asyncio.TimeoutError:
        nickName = None
        await message.channel.send('Timeout Error! Please try again.')
        log.warning('Timeout Error! Please try again. User did not respond within 1 minute.')

    # Update Nickname
    if nickName is not None:
        try:
            await member.edit(nick=nickName)
            log.info(f"{member}'s nickname was updated to: {nickName}.")
        except discord.errors.Forbidden:
            log.error(f"The bot does not have permission to change {member}'s nickname! Please verify action and try again.")


async def showHelpMenu(member, message):
    helpMessage = f"Hello {member}! Here are the available options:\n ``` !help: View this menu.\n !verify: Verify your account and obtain roles.\n !sync: Sync your discord roles with the website. ```"

    await message.channel.send(helpMessage)


async def syncRoles(member, message, id):
    nickName, newRoles = BC.fetchUserInfo(id)
    log.debug(f"Received {nickName} and {newRoles} roles.")

    await message.channel.send(f"You have the following roles: {newRoles}")

    if nickName is not None:
        try:
            await member.edit(nick=nickName)
            log.info(f"{member}'s nickname was updated to: {nickName}.")
        except discord.errors.Forbidden:
            log.error(f"The bot does not have permission to change {member}'s nickname! Please verify action and try again.")


# Event Handlers
@client.event
async def on_ready():
    log.info("Logged in as a bot {0.user}".format(client))
    print("Logged in as a bot {0.user}".format(client))

@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="new-members")
    await channel.send(f"Welcome to Air France/KLM Virtual Airlines, @{member}!\n This is a place for AFVA Members to get together and chat about our experiences and help each other.\n\n Please visit the #rules channel to see the rules for the server.\n\n Most importantly, please continue to have fun!\n\n Also, you may verify your account by typing !verify in #verification, or type ?help? to see a list of options.")

@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    user_id = str(message.author).split("#")[1]
    member = message.author
    channel = str(message.channel.name)
    user_message = str(message.content)

    # Make sure that the bot only responds to users
    if message.author == client.user:
        return

    # Check if the user sent "!verify"
    if user_message.lower() == "!verify" and channel == "testing":
        log.info(f"{username} used !verify in {channel} channel.")
        await verifyUser(message, username, user_id)

    if user_message.lower() == "?help?":
        log.info(f"{member} used ?help?")
        await showHelpMenu(member, message)
        

    if user_message.lower() == "!sync":
        log.info(f"{member} used !sync.")
        await syncRoles(member, message, user_id)


# Function to clear verification channel
async def clearChannel(channelToBeCleared):
    channel = discord.utils.get(client.guild.text_channels, name=channelToBeCleared)
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
client.run(token)