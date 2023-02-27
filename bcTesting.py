import requests
import json

verificationURL = 'https://dev.afva.net/discord_info.ws?id='

discordRoles = {
    'test-role': 1072568546133029074,
    'role1': 1079910340667637850,
    'role2': 1079910446150197278,
    'everyone': 1033851887117664306,
    'AFVA-Booster': None,
    'AFVA-Shareholder': None,
    'P1 - PPL': None,
    'CFI': None,
    'DCFI': None,
    'Senior Captain': None
}

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
        pilotID = jsonData["pilotCode"]
        
        # Check if the user has a Pilot ID
        if pilotID:
            nickName = f'{jsonData["firstName"]} {jsonData["lastName"]} - {pilotID}'
        else:
            nickName = f"{jsonData['firstName']} {jsonData['lastName']} - NEW PILOT"

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