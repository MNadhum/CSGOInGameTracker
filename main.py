import json
from Player import Player
import Data


def main(event, context):
    """
    Main function to set up and run entire program
    :return: None
    """
    playersDict = dict()

    apiInfo = event['body']

    playersInGame = Data.GetPlayers(apiInfo)
    players = Data.CreatePlayers(playersInGame)

    for player in players:
        player.LoadData()
        playersDict[player.GetID()] = player

    for player in players:
        player.LoadFriendsInGame(playersDict)

    export = Data.ExportJSON(players)

    response = {
        "statusCode": 200,
        "body": json.dumps(export)
    }
    return response

