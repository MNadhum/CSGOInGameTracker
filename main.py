import Data
import Web
import Player
import os

CSGOPATH = os.getenv("CONPATH")

def main():
    """
    Main function to set up and run entire program
    :return: None
    """
    playersDict = dict()
    fileName = Data.LoadFileName(CSGOPATH)

    playersInGame = Data.GetPlayers(fileName)
    players = Data.CreatePlayers(playersInGame)

    for player in players:
        player.LoadData()
        playersDict[player.steamID] = player


    for player in players:
        player.LoadFriendsInGame(playersDict)

    # FOR TESTING
    for player in players:
        print(player.name)
        print(player.steamID)
        print('[', end="")
        for p in player.GetQueued():
            print(p, end = ",")
        print(']', end = "")
        print()
        print(player.rank)
        print(player.faceIt)
        print(player.wr)
        print(player.associatedPlayers)
        print(player.steamAvatar)
        print("-------------------------------")




if __name__ == '__main__':
    main()