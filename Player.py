class Player:
    """
    Represents a Player

    Class allows for storing each player's information in an organized manner and allows for easy modification
    of each player's data through the class methods.

    Attributes:
        name (str): Steam username of player
        steamID (str): Player's steamID (also known as Community ID)
        queuedWith (set): Set of players that This player is queued with
        rank (int): Player's matchmaking rank
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
        self.rank = -1
        self.faceIt = -1
        self.wr = -1.0

    def __str__(self):
        """
        Allows class to be represented as a string.

        :return (str): Name and steamID of player in the following format "name:steamID"
        """
        return self.name + ":" + str(self.steamID)

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