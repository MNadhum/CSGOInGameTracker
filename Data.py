import os
from Player import Player
import bst

def UniqueToCommunity(uniqueid):
    """
    Converts player's uniqueid to player's Community ID.
    Based on information from: https://developer.valvesoftware.com/wiki/SteamID

    :param uniqueid(int): id to be converted into new format
    :return (string): CommunityID format of the uniqueid
    """

    # The conversion formula is: CommunityID = Z*2 + V + Y
    # V represents account type (which is "Single User Account" for players, based on documentation)
    # Z and Y are from the uniqueid, which has the following format: STEAM_X:Y:Z

    uniqueid = uniqueid.split(':')

    Z = int(uniqueid[2])
    Y = int(uniqueid[1])
    V =76561197960265728

    communityId = (Z * 2) + V + Y

    return communityId

def LoadFileName(path):
    """
    Looks at given path and loads the newest console dump, in order to retrieve players' uniqueid.

    :param path (string): CSGO filepath in system
    :return: None
    """

    dumpNum = -1
    dumpNumString = ""

    for fileName in os.listdir(path):
        # Find the newest condump file
        # console dumps are saved as condumpX.txt with X starting at 000 and going up
        if (fileName.startswith("condump")):
            thisNum = int(fileName[fileName.find('p') + 1:fileName.find('.')])
            if (thisNum > dumpNum):
                dumpNum = thisNum
                dumpNumString = fileName

    file = path + dumpNumString

    return file

def GetPlayers(fileName):
    """
    Gathers player's data from the console dump text file.

    :param fileName (string): Name of condump file to extract data from
    :return (dict): Dictionary linking player# (0-9) to player data (steamID and name)
    """

    file = open(fileName, "r", encoding="utf8")
    here = False
    count = 0
    playerData = {}
    playerNum = 0

    for line in file:
        if here:
            count += 1
            # The table with player information has 10 rows (one for each player)
            if 0 < count <= 10:
                ind1 = line.find('"')
                ind2 = line.rfind('"')
                lineS = line.split(" ")
                # Ensure that player is not a bot, and add player's data to players dict
                if lineS[2] != "BOT":
                    lineS = line[ind2:].split(" ")
                    playerData[playerNum] = [line[ind1 + 1:ind2], lineS[1]]
                    playerNum += 1
            else:
                break
        # Checks if current line is the header of the table with player information
        if line == "# userid name uniqueid connected ping loss state rate\n":
            here = True

    file.close()

    # Convert the uniqueids of all players into steamIDs
    for val in playerData.values():
        val[1] = str(UniqueToCommunity(val[1]))

    return playerData

def CreatePlayers(playerData):
    """
    Creates Player objects for each player in the game using the Player class

    :param playerData (dict): Dictionary containing each player's name and steamID
    :return (list): List of Player objects (each representing one player in the game)
    """

    players = []
    for user in playerData.values():
        thisPlayer = Player(user[0], user[1])
        players.append(thisPlayer)

    return players

def CleanUpData(rawData):
    """
    Cleans up the raw data from the sites into a specific format to be used by Player.LoadData function

    :param rawData (string): raw player data scraped from sources
    :return (string): Cleaned up version of playerData
    """
    playerData = ["", -1, -1, None]
    """  
    OUTPUT/RETURN FORMAT:
        playerData[0] = rank
        playerData[1] = faceIt
        playerData[2] = wr
        playerData[3] = bst of associatedPlayers
        playerData[4] = steamAvatar
     
    rawData[0] gives the following:
        playerData[0]/rank - found in "Games  ⮕ 0 ⮕ skilllevel"
        playerData[2]/wr - iterate through "games ⮕ i ⮕ matchResult" and add up win, tie, loss and calculate wr
        playerData[3]/associatedPlayers - found in "teammates ⮕ i ⮕ steam64Id"
        playerData[4]/steamAvatarSteam - found in "meta ⮕ steamAvatarUrl"

    rawData[1] gives the following:
       playerData[3]/associatedPlayers - if "player ⮕ games" > 3, then add to associatedPlayers
     
    rawData[2] gives the following:
        playerData[1]/faceIt - "payload ⮕ players ⮕ results ⮕ (if not NONE) ⮕ 0 ⮕ games ⮕ 0 ⮕ skill_level"
    
    rawData[3] gives the following information:
        playerData[3]/associatedPlayers - "friendslist ⮕ friends ⮕ steamid"
     """


    return playerData

def ExportJSON(players):
    """
    Export relevant data of all players into a JSON file

    :param players (list): List of Player objects, representing each player in the game
    :return: None
    """
    pass


