import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import requests
import json

# Get environment variable(s)
API_KEY = os.getenv("API_KEY")
LINK1 = os.getenv("SITE1")
LINK2 = os.getenv("SITE2")
LINK2_2 = os.getenv("SITE2_2")
FACEIT = os.getenv("FACEIT")
STEAM = os.getenv("STEAM")
PATH = os.getenv("PATH")
id = os.getenv("TESTID")



def ScrapeData(player):

    """
    Uses Selenium and GET requests to retrieve data from sites

    :param player (string): steamID of player
    :return (string): Data received from sources in JSON format
    """

    # Configuring driver for scraping data from site 2
    driverOptions = webdriver.ChromeOptions()
    driverOptions.page_load_strategy = 'normal'
    driverOptions.add_argument("--headless=new")
    driverOptions.add_argument("--disable-dev-shm-usage")
    driverOptions.add_argument("--disable-notifications")
    driverOptions.add_argument("disable-infobars")

    driverService = ChromeService(executable_path=PATH)

    driver = webdriver.Chrome(service=driverService, options=driverOptions)
    driver.implicitly_wait(5)


    url1 = LINK1 + str(player)
    url2 = LINK2 + str(player) + LINK2_2
    url3 = FACEIT + str(player)
    url4 = (STEAM + API_KEY + "&steamid=" + str(player) + "&relationship=all")


    requestOne = requests.get(url1)
    info1 = requestOne.json()


    driver.get(url2)
    requestTwo = driver.find_element(by=By.CSS_SELECTOR, value="body > pre")
    info2 = requestTwo.text
    info2 = json.loads(info2)


    requestThree = requests.get(url3)
    info3 = requestThree.json()

    requstFour = requests.get(url4)
    info4 = requstFour.json()

    data = [info1, info2, info3, info4]

    return data

