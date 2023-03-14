 # Commands for AFVA BOT
 
 # AFVA Bot Version 1.0
# By: Daniel Duhon

import requests
import json


# Global Constants
verificationURL = 'https://www.afva.net/discord_info.ws?id='
unregURL = 'https://www.afva.net/discord_unregister.ws?id='

afvaStaffRoles = ["Fleet","HireMgr","Instructor","Charts","Developer","Dispatch","HR","Admin","PIREP","NOTAM","Senior Staff","Moderator","Tech","TestAdmin","AcademyAdmin","News","Schedule","Signature","Event","Operations","Examination","Route"]


# Discord roles. Format: 'role': 'id'
discordRoles = {
    'AFVA-Booster': 793300706214936586,
    'AFVA-Shareholder': 904015787126325309,
    'Senior Staff': 646449197469532172, 
    'Tour Guide': 1062420370268897334, 
    'Operations & Administrative Staff': 646449303677829126, 
    'CFI': 1011661203816333442,
    'DCFI': 1072558336651821197,
    'Fleet Staff': 646449250632466445, 
    'Events': 884657255046332426,
    'Instructors': 895322298649829396,
    'IT': 993134705690026064,
    'Chief Pilot': 646467929348767804,
    'Assistant Chief Pilot': 646467957823635483,
    'Senior Captain': 793957552718348288,
    'Captain': 943238568497778699,
    'First Officer': 943237140270170182,
    'Concorde': 646467333077860383,
    'A380-800': 646467423729483797,
    'B777-300': 646467552259735562,
    'B747-400': 646467371774509094,
    'A350-900': 646467763644399636,
    'B787-9': 646467215520170005,
    'A330-200': 646467619368599562,
    'DC-3': 850890559723798569,
    'B737-800': 646467266493415444,
    'A320': 646467480872681483,
    'A220-3(CSeries)': 793282582316843038,
    'P1 - PPL': 1010682355876376606,
    'RW Pilot': 907986804681113610,
    'Pilots': 917498994098331659,
    'New Pilot': 793313617343938601,
    'everyone': 646368864187318302
}

# Available Ranks
afvaRanks = ["First Officer", "Captain", "Senior Captain", "Assistant Chief Pilot", "Chief Pilot"]

# Equipment Programs
afvaPrograms = ["A220-3(CSeries)", "A320", "B737-800", "A330-200", "B787-9", "DC-3", "A350-900", "B747-400", "B777-300", "A380-800", "Concorde"]


# Check username
def usernameLength(name, id):
    if len(name + ' - ' + id) < 29:
        return name + ' - ' + id
    elif len(name + ' - ' + id) >= 29 and len(name + ' - ' + id) < 32:
        return name + '-' + id
    else:
        return name + id


# Set User's roles based on security roles, rank, and equipment program
def setUserRoles(roles, rank, equipment):
    # Initialize empty roles list
    discordUserRole = [discordRoles['everyone']]

    # Check for roles
    for role in roles:
        if role == "Pilot": # Assign pilot role
            discordUserRole.append(discordRoles["Pilots"])
        elif not discordRoles["Fleet Staff"] in discordUserRole: # Assign Fleet Staff role once if user has any staff roles in afvaStaffRoles
            if role in afvaStaffRoles:
                discordUserRole.append(discordRoles["Fleet Staff"])
        elif role == "Instructor": # Assign Instructor role
            discordUserRole.append(discordRoles["Instructors"])
        elif (role == "Developer" or role == "Tech") and discordRoles["IT"] not in discordUserRole: # Add IT role if the user has the Developer or Tech role AND does not already have role
            discordUserRole.append(discordRoles["IT"])
        elif role == "Operations" and discordRoles["Senior Staff"] not in discordUserRole: # Add operations role if user is not SS and has Ops role
            discordUserRole.append(discordRoles["Operations & Administrative Staff"])
        elif role == "Event": # Assign Events role
            discordUserRole.append(discordRoles["Events"])

    discordUserRole.append(discordRoles[rank]) # Assigns role based on Rank
    discordUserRole.append(discordRoles[equipment]) # Assigns role based on Program

    # Return Roles
    return discordUserRole


# Verify User Exists and apply appropriate roles
def fetchUserInfo(id):
    # If user exists, store data
    try:
        # Fetch data from AFVA Site
        rawData = requests.get(f"{verificationURL + str(id)}")
        try:
            jsonData = json.loads(rawData.text)

        except TypeError:
            print("User is not registered! Please register your account and try again.")
            return None

        # Separate data into useable strings
        pilotID = jsonData['pilotCode']
        
        name = f"{jsonData['firstName']} {jsonData['lastName']}"

        # Check if the user has a Pilot ID
        if pilotID:
            nickName = usernameLength(name, pilotID)
        else:
            nickName = usernameLength(name, "NEW PILOT")

        roles = jsonData["roles"]
        rank = jsonData["rank"]
        equipProgram = jsonData["eqType"]

        # Parse roles for Discord roles
        userRoles = setUserRoles(roles, rank, equipProgram)

        return [nickName, userRoles]

    # Catch the case where the user is not registered.
    except json.decoder.JSONDecodeError:
        print("Error! User not found. Please register your Discord account.")

        return None
    

def unregUser(id):
    req = requests.get(f"{unregURL + str(id)}")

# Test code
# user = verifyUser('0995')

# # verifyUser('2563')

# print(user[1])