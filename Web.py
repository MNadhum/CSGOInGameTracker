import os
import requests
import json


API_KEY = os.getenv("API_KEY")
LINK1 = os.getenv("SITE1")
FACEIT = os.getenv("FACEIT")
STEAM = os.getenv("STEAM")


def ScrapeData(player):
    """
    Uses GET requests to retrieve data from sites

    :param player (string): steamID of player
    :return (string): Data received from sources in JSON format
    """

    url1 = LINK1 + str(player)
    url3 = FACEIT + str(player)
    url4 = (STEAM + API_KEY + "&steamid=" + str(player) + "&relationship=all")
    info1 = ""
    info2 = ""
    info3 = ""
    info4 = ""

    requestOne = requests.get(url1)
    try:
        info1 = requestOne.json()
    except:
        pass

    requestThree = requests.get(url3)
    try:
        info3 = requestThree.json()
    except:
        pass

    requstFour = requests.get(url4)
    try:
        info4 = requstFour.json()
    except:
        pass

    data = [info1, info2, info3, info4]

    return data

