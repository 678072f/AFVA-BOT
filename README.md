# README

This is a Discord Bot for Air France/KLM Virtual Airlines.

This Discord bot is intended only for Air France/KLM Virtual Airlines.
For questions or inquiries, please contact info@afva.net

https://www.afva.net/


# Capabilities

- $verify to register and verify user registration, auto-assigning roles, and update nickname.
- $help command displays custom help menu.
- $sync to update their roles.
- Error Handling for cases where someone tries to use commands before registration.
- $log Allows IT Staff to view Log within Discord
- Allows Staff to $sync and $unregister users


# Future Plans

- Add Feature to post announcements from the website.
- Add feature to detect and announce pilot promotions (like the automated ones in the Forums on the website).
- Add feature to share ACARS flight status messages in a "dispatch" channel.


# Known-Issues

3/30/2023:

1. $help <module> doesn't work fully.
2. $sync command error handling incomplete.
3. Missing comments and documentation for parts.

2/19/2023: <- All are Fixed as of 3/15/2023

~~1. Cannot change users with Senior Staff role. Need to add check for that. <- Should be complete.~~
~~2. Need to make sure that if the user's registration isn't processed before the bot tries to fetch it that it won't error out. <- Need more testing.~~

~~1. Need to add code for removing the 'New Pilot' role once verification is complete.~~
~~2. Need to add error handling if the user hasn't registered their account with Discord.~~


# Release Notes

V1.0.0:

- Released: 3/29/2023
- Release Notes:
    - Initial Release
    - Features include: User verification, profile syncing, help menu, staff tools, log viewing for identifying issues