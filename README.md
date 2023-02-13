# README

This is a Discord Bot for Air France/KLM Virtual Airlines.

# Capabilities

- Registering User's Discord account with dev.afva.net server.
- Verifying user registration and auto-assigning roles and updating nickname.
- Display help menu with ?help? command
- Clears #verification channel weekly on Fridays at 23:59

# Future Plans

- Add !sync command, capability, and schedule.
    - Look into what is needed to allow staff members to run this on behalf of someone else.
- Add Feature to post announcements from the website using a webhook (may need input from site).
- Add feature to detect and announce pilot promotions (like the automated ones in the Forums on the website).
- Add feature to share ACARS flight status messages in a "dispatch" channel.

# Known-Issues

1. Cannot change users with Senior Staff role. Need to add check for that. <- Should be complete.
2. Need to make sure that if the user's registration isn't processed before the bot tries to fetch it that it won't error out. <- Need more testing.

~~1. Need to add code for removing the 'New Pilot' role once verification is complete.~~
~~2. Need to add error handling if the user hasn't registered their account with Discord.~~