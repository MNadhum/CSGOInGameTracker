import Data
import Web
import Player
import bst

def main():
    """
    Main function to set up and run entire program
    :return: None
    """
    fileName = Data.LoadFileName()
    playersInGame = Data.GetPlayers(fileName)
    players = Data.CreatePlayers(playersInGame)

    for player in players:
        player.LoadData()

    pass




if __name__ == '__main__':
    main()