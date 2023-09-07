import Data
import Web
import bst

class Player:
    """
    Represents a Player

    Class allows for storing each player's information in an organized manner and allows for easy modification
    of each player's data through the class methods.

    Attributes:
        name (str): Steam username of player
        steamID (str): Player's steamID (also known as Community ID)
        queuedWith (set): Set of players that This player is queued with
        rank (str): Player's matchmaking rank
        faceIt (int): Player's FaceIt level (if applicable)
        wr (float): Player's matchmaking win rate
    """

    def __init__(self, name, steamID):
        """
        Class constructor.

        :param name: Steam username of the player
        :param name: SteamID (aka Community ID) of the player
        :return: None
        """
        self.name = name
        self.steamID = steamID
        self.queuedWith = set()
        self.rank = ""
        self.faceIt = -1
        self.winRate = -1.0
        self.associatedPlayers = None
        self.steamAvatar = ""

    def __str__(self):
        """
        Allows class to be represented as a string.

        :return (str): steamID of player
        """
        return str(self.steamID)

    def GetQueued(self):
        """
        Get the set of players that this player is queued with.

        :return (set): Set of Player objects that this player is queued with
        """
        return self.queuedWith

    def AddFriend(self, player):
        """
        Links two Player objects through adding them to each other's queuedWith set, which
        means that they are queued with each other in the game.

        :param player (Player): Player object representing the player that this player is queued with
        :return: None
        """

        if player not in self.queuedWith:
            self.queuedWith.add(player)
            player.AddFriend(self)
        pass


    def LoadData(self):
        """
        Gets Player's data from sources, cleans up the data, and adds that data to the Player object

        :return: None
        """

        scraped = Web.ScrapeData(str(self.steamID))
        myData = Data.CleanUpData(scraped)
        self.rank = myData[0]
        self.faceIt = myData[1]
        self.winRate = myData[2]
        self.associatedPlayers = myData[3]
        self.steamAvatar = myData[4]


    def LoadFriendsInGame(self, players):
        """
        Iterates through the players in this game, and figures out who each player is queued with
        :param players (list): List of player objects of players in the game
        :return: None
        """

        for player in players.values():
            if self != player:
                foundNode = bst.search(self.associatedPlayers, int(player.steamID))
                if foundNode != None:
                    foundPlayer = players[str(foundNode.key)]
                    self.AddFriend(foundPlayer)

    def GetDict(self):
        playerDict = {}
        playerDict["name"] = self.name
        playerDict["steamID"] = self.steamID
        queuedDict = {}
        for player in self.queuedWith:
            queuedDict["id"] = str(player)
        playerDict["queuedWith"] = queuedDict
        playerDict["rank"] = self.rank
        playerDict["faceIT"] = self.faceIt
        playerDict["winRate"] = self.winRate
        playerDict["avatar"] = self.steamAvatar
        return playerDict