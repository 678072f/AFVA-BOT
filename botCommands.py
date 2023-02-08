 # Commands for AFVA BOT
 
 # AFVA Bot Version 1.0
# By: Daniel Duhon

# This example requires the 'message_content' intent.

import requests
import json


# Global Constants
verificationURL = 'https://dev.afva.net/discord_info.ws?id='

afvaStaffRoles = ["Fleet","HireMgr","Instructor","Charts","Developer","Dispatch","HR","Admin","PIREP","NOTAM","Senior Staff","Moderator","Tech","TestAdmin","AcademyAdmin","News","Schedule","Signature","Event","Operations","Examination","Route"]

# Discord roles. Format: ['role', 'id']
discordRoles = {
    'Senior Staff': '646449197469532172', 
    'Tour Guide': '1062420370268897334', 
    'Operations & Administrative Staff': '646449303677829126', 
    'Fleet Staff': '646449250632466445', 
    'Events': '884657255046332426',
    'Instructors': '895322298649829396',
    'IT': '993134705690026064',
    'Chief Pilot': '646467929348767804',
    'Assistant Chief Pilot': '646467957823635483',
    'Senior Captain': '793957552718348288',
    'Captain': '943238568497778699',
    'First Officer': '943237140270170182',
    'Concorde': '646467333077860383',
    'A380-800': '646467423729483797',
    'B777-300': '646467552259735562',
    'B747-400': '646467371774509094',
    'A350-900': '646467763644399636',
    'B787-9': '646467215520170005',
    'A330-200': '646467619368599562',
    'DC-3': '850890559723798569',
    'B737-800': '646467266493415444',
    'A320': '646467480872681483',
    'A220-3(CSeries)': '793282582316843038',
    'RW Pilot': '907986804681113610',
    'Pilots': '917498994098331659',
    'New Pilot': '793313617343938601'
}

afvaRanks = ["First Officer", "Captain", "Senior Captain", "Assistant Chief Pilot", "Chief Pilot"]

afvaPrograms = ["A220-3(CSeries)", "A320", "B737-800", "A330-200", "B787-9", "DC-3", "A350-900", "B747-400", "B777-300", "A380-800", "Concorde"]


# Set User's roles based on security roles, rank, and equipment program
def setUserRoles(roles, rank, equipment):
    
    discordUserRole = []
    for role in roles:
        if role == "Pilot":
            discordUserRole.append(discordRoles["Pilots"])
        elif not discordRoles["Fleet Staff"] in discordUserRole:
            if role in afvaStaffRoles:
                discordUserRole.append(discordRoles["Fleet Staff"])
        elif role == "Instructor":
            discordUserRole.append(discordRoles["Instructors"])
        elif role == "Senior Staff":
            discordUserRole.append(discordRoles["Senior Staff"])
        elif (role == "Developer" or role == "Tech") and discordRoles["IT"] not in discordUserRole:
            discordUserRole.append(discordRoles["IT"])
        elif role == "Operations" and discordRoles["Senior Staff"] not in discordUserRole:
            discordUserRole.append(discordRoles["Operations & Administrative Staff"])
        elif role == "Event":
            discordUserRole.append(discordRoles["Events"])

    discordUserRole.append(discordRoles[rank])
    discordUserRole.append(discordRoles[equipment])

    return discordUserRole


# Verify User Exists and apply appropriate roles
def verifyUser(id):
    # If user exists, store data
    try:
        # Fetch data from AFVA Site
        rawData = requests.get(f"{verificationURL + str(id)}")
        try:
            jsonData = json.loads(rawData.text)

        except TypeError:
            print("User is not registered! Please register your account and try again.")

        # Separate data into useable strings
        nickName = f'{jsonData["firstName"]} {jsonData["lastName"]} - {jsonData["pilotCode"]}'
        roles = jsonData["roles"]
        rank = jsonData["rank"]
        equipProgram = jsonData["eqType"]

        # Parse roles for Discord roles
        userRoles = setUserRoles(roles, rank, equipProgram)
       
        # DEBUG CODE:
        # print(nickName, roles)
        # print(userRoles)

        return [nickName, userRoles]

    # Catch the case where the user is not registered.
    except json.decoder.JSONDecodeError:
        print("Error! User not found. Please register your Discord account.")
        userRole = discordRoles["New Pilot"]

        return userRole


# Test code
# user = verifyUser('0995')

# # verifyUser('2563')

# print(user[1])