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

    Data.ExportJSON(players)




if __name__ == '__main__':
    main()