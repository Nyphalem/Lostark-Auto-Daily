from originConfig import config
import time
import pydirectinput
import logging
import random
import json

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

config_file_path = 'personalConfig.json'

pydirectinput.PAUSE = 0.05
newStates = {
    "status": "inCity",
    "abilities": [],
    "abilityScreenshots": [],
    "bossBarLocated": False,
    "clearCount": 0,
    "fullClearCount": 0,
    "moveToX": config["screenCenterX"],
    "moveToY": config["screenCenterY"],
    "moveTime": 0,
    "botStartTime": None,
    "instanceStartTime": None,
    "deathCount": 0,
    "healthPotCount": 0,
    "timeoutCount": 0,
    "badRunCount": 0,
    "gameRestartCount": 0,
    "gameCrashCount": 0,
    "gameOfflineCount": 0,
    "minTime": config["timeLimit"],
    "maxTime": -1,
    "floor3Mode": False,
    "multiCharacterMode": False,
    "currentCharacter": config["mainCharacter"],
    "multiCharacterModeState": [],
}

def sleep(min, max):
    sleepTime = random.randint(min, max) / 1000.0
    if sleepTime < 0:
        return
    time.sleep(sleepTime)


def sleepClickOrPress():
    sleep(300, 500)


def sleepClickOrPressLong():
    sleep(1000, 1200)


def sleepClickOrPressList():
    sleep(2000, 2500)


def sleepCommonProcess():
    sleep(5000, 6000)


def sleepSongSky():
    sleep(20000, 22000)


def sleepTransportLoading():
    sleep(20000, 22000)


def sleepVoyage():
    sleep(90000, 100000)


def mouseMoveTo(**kwargs):
    x = kwargs["x"]
    y = kwargs["y"]
    pydirectinput.moveTo(x=x, y=y)


def read_status_value(file_path, key):
    try:
        with open(file_path, 'r') as file:
            config_data = json.load(file)
            return config_data.get(key, None)
    except FileNotFoundError:
        logging.info("Config file not found.")
        return None


def update_status_value(file_path, key, value):
    try:
        with open(file_path, 'r') as file:
            config_data = json.load(file)
        config_data[key] = value
        with open(file_path, 'w') as file:
            json.dump(config_data, file, indent=4)
    except FileNotFoundError:
        logging.info("Config file not found.")
    except json.JSONDecodeError:
        logging.info("Error decoding JSON.")

