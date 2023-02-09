# README

This is a Discord Bot for Air France/KLM Virtual Airlines.

# Capabilities

- Registering User's Discord account with dev.afva.net server.
- Verifying user registration and auto-assigning roles and updating nickname.
- Display help menu with ?help? command
- Clears #verification channel weekly on Fridays at 23:59

# Known-Issues

1. Cannot change users with Senior Staff role. Need to add check for that.
2. Need to make sure that if the user's registration isn't processed before the bot tries to fetch it that it won't error out.

~~1. Need to add code for removing the 'New Pilot' role once verification is complete.~~
~~2. Need to add error handling if the user hasn't registered their account with Discord.~~