# AFVA Bot Version 1.0
# By: Daniel Duhon

# This example requires the 'message_content' intent.

import discord
import os
from dotenv import load_dotenv
import botCommands as BC
import asyncio

# Global Constants
load_dotenv()
token = os.getenv('TOKEN')
registrationURL = 'https://dev.afva.net/discordreg.do?id='

# Setup Discord
intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

# Event Handlers
@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))

@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    user_id = str(message.author).split("#")[1]
    member = message.author
    channel = str(message.channel.name)
    user_message = str(message.content)

    print(f"Message {user_message} by {username} on {channel}.")

    # Make sure that the bot only responds to users
    if message.author == client.user:
        return

    # Check if the user sent "!verify"
    if user_message.lower() == "!verify":
        # Respond to the user with a welcome message and send the verification link:
        await message.channel.send(f"Hello {username}, I am sending you to the verification link.")
        await message.channel.send(f'Please open: {registrationURL + user_id} to register your account, then react with 👍.')

        # Define function to check for thumbsup reaction
        def check(reaction, user):
            return user == message.author and str(reaction.emoji) == '👍'

        try:
            # Check for the user's reaction
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
            # Store the user's nickname and roles from the verification Function
            nickName, roleList = BC.verifyUser(user_id)

            # Iterate through the roles provided from the server
            for afvaRole in roleList:
                # Check if the role exists and store in 'role'
                role = discord.utils.get(member.guild.roles, id = afvaRole)

                # Check if the user already has the role. If yes, skip
                if afvaRole in member.roles:
                    await message.channel.send(f"You already have the {afvaRole} role! Moving on...")
                # If the user doesn't already have the role, add it
                else:
                    # Make sure the role exists
                    if role is not None:
                        await member.add_roles(role)
                        await message.channel.send("Added role.")
                    
                    # Send a message if the role isn't available
                    else:
                        await message.channel.send(f"The role with ID: {afvaRole} was not found on this server!")
                
                # Print the role (for debugging)
                print(role)

            # Respond with user's new nickname
            await message.channel.send(f"Success! Hello {nickName}")

        # Catch timeout
        except asyncio.TimeoutError:
            await channel.send('👎')

        # Update Nickname
        await member.edit(nick=nickName)
        
@client.event
async def on_member_join(member):
    username = str(member.id)
    await member.send(f"Welcome {username}!")
    return

client.run(token)