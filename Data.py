import os
from Player import Player
import bst
import json

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

def GetPlayers(apiData):
    """
    Gathers player's data from the console dump text, received through GET request.

    :param apiData (string): Data from condump
    :return (dict): Dictionary linking player# (0-9) to player data (steamID and name)
    """

    here = False
    count = 0
    playerData = {}
    playerNum = 0
    apiData = apiData.split('#')

    for line in apiData:
        if len(line) != 0:
            line = line.strip()
            if line == "userid name uniqueid connected ping loss state rate":
                here = True
                continue
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


    # OUTPUT/RETURN FORMAT:
    # playerData[0] = rank
    # playerData[1] = faceIt
    # playerData[2] = wr
    # playerData[3] = bst of associatedPlayers
    # playerData[4] = steamAvatar

    playerData = ["", -1, -1, None, ""]

    JSON1 = rawData[0]
    JSON2 = rawData[1]
    JSON3 = rawData[2]
    JSON4 = rawData[3]


    ranksFile = open("ranks.json", "r", encoding="utf8")
    ranksJSON = json.load(ranksFile)
    ranksFile.close()

    # Count the W/L/T outcomes of the player's games and get name of the
    # rank based on its number (0 = unranked, 18 = Global Elite)
    win = 0
    loss = 0
    tie = 0
    try:
        for gameNum in range(len(JSON1["games"])):
            gameSource = JSON1["games"][gameNum]["dataSource"]
            gameRank = JSON1["games"][gameNum]["skillLevel"]
            cs2Game = JSON1["games"][gameNum]["isCs2"]
            teamCount = len(JSON1["games"][gameNum]["ownTeamSteam64Ids"])
            countable = False

            if (gameSource == "matchmaking") and not cs2Game  and (teamCount > 2):
                countable = True

            # If the game is a matchmaking game (not FaceIt), and the player had a rank in this game:
            if countable:
                if playerData[0] == "" and gameRank is not None:
                    playerData[0] = ranksJSON[str(JSON1["games"][gameNum]["skillLevel"])]
                gameResult = JSON1["games"][gameNum]["matchResult"]
                if gameResult == "win":
                    win += 1
                elif gameResult == "loss":
                    loss += 1
                else:
                    tie += 1
    except:
        pass

    # Calculating win rate based on number of WIN, TIE, LOSS games
    if (win + loss + tie) != 0:
        wr = (win + ((1/2) * tie)) / (win + loss + tie)
        playerData[2] = wr

    # Populate BST with IDs of players associated with THIS player using Source1
    try:
        for playerNum in range(len(JSON1["teammates"])):
            id = int(JSON1["teammates"][playerNum]["steam64Id"])
            if playerData[3] is None:
                playerNode = bst.Node(id)
                playerData[3] = playerNode
            else:
                bst.insert(playerData[3], id)
    except:
        pass

    # Get link to player's Steam profile picture
    try:
        playerData[4] = JSON1["meta"]["steamAvatarUrl"]
    except:
        pass

    # Gets FaceIT level of player
    try:
        if len(JSON3["payload"]["players"]) > 0:
            playerData[1] = JSON3["payload"]["players"]["results"][0]["games"][0]["skill_level"]
    except:
        pass

    try:
        for friendNum in range(len(JSON4["friendslist"]["friends"])):
            id = int(JSON4["friendslist"]["friends"][friendNum]["steamid"])
            if playerData[3] is None:
                playerNode = bst.Node(id)
                playerData[3] = playerNode
            else:
                bst.insert(playerData[3], id)
    except:
        pass

    return playerData



def ExportJSON(players):
    """
    Export relevant data of all players into a JSON format

    :param players (list): List of Player objects, representing each player in the game
    :return: Player data in JSON format to be sent back in API response
    """
    exporting = {}
    playerNum = 0
    for player in players:
        playerDict = player.GetDict()
        exporting[playerNum] = playerDict
        playerNum += 1
    return exporting
