import pyautogui
import pydirectinput
import logging
from config import config
from utils import *

def enterChaos(currentCharacter):
    sleep(600, 800)
    while True:
        sleep(1000, 1200)

        pydirectinput.keyDown("alt")
        sleep(100, 200)
        pydirectinput.press("q")
        sleep(100, 200)
        pydirectinput.keyUp("alt")
        sleep(1200, 1400)

        mouseMoveTo(x=886, y=316)
        sleep(500, 600)
        pydirectinput.click(x=886, y=316, button="left")
        sleep(500, 600)
        mouseMoveTo(x=886, y=316)
        sleep(500, 600)
        pydirectinput.click(x=886, y=316, button="left")
        sleep(500, 600)

        # select chaos dungeon level based on current Character
        _curr = config["characters"][currentCharacter]
        chaosTabPosition = {
            # punika
            1100: [[1317, 256], [411, 382]],
            1310: [[1317, 256], [411, 455]],
            1325: [[1317, 256], [411, 525]],
            1340: [[1317, 256], [411, 580]],
            1355: [[1317, 256], [411, 655]],
            1370: [[1317, 256], [411, 731]],
            1385: [[1317, 256], [411, 796]],
            1400: [[1317, 256], [411, 865]],
            # south vern
            1415: [[1561, 255], [411, 382]],
            1445: [[1561, 255], [411, 455]],
            1475: [[1561, 255], [411, 525]],
            1490: [[1561, 255], [411, 580]],
            1520: [[1561, 255], [411, 655]],
        }
        mouseMoveTo(
            x=chaosTabPosition[_curr["ilvl-aor"]][0][0],
            y=chaosTabPosition[_curr["ilvl-aor"]][0][1],
        )
        sleep(800, 900)
        pydirectinput.click(
            x=chaosTabPosition[_curr["ilvl-aor"]][0][0],
            y=chaosTabPosition[_curr["ilvl-aor"]][0][1],
            button="left",
        )
        sleep(500, 600)
        pydirectinput.click(
            x=chaosTabPosition[_curr["ilvl-aor"]][0][0],
            y=chaosTabPosition[_curr["ilvl-aor"]][0][1],
            button="left",
        )
        sleep(500, 600)
        mouseMoveTo(
            x=chaosTabPosition[_curr["ilvl-aor"]][1][0],
            y=chaosTabPosition[_curr["ilvl-aor"]][1][1],
        )
        sleep(800, 900)
        pydirectinput.click(
            x=chaosTabPosition[_curr["ilvl-aor"]][1][0],
            y=chaosTabPosition[_curr["ilvl-aor"]][1][1],
            button="left",
        )
        sleep(500, 600)
        pydirectinput.click(
            x=chaosTabPosition[_curr["ilvl-aor"]][1][0],
            y=chaosTabPosition[_curr["ilvl-aor"]][1][1],
            button="left",
        )
        sleep(500, 600)

        enterButton = pyautogui.locateCenterOnScreen(
            "./screenshots/enterButton.png",
            confidence=0.75,
        )
        if enterButton != None:
            x, y = enterButton
            mouseMoveTo(x=x, y=y)
            sleep(800, 900)
            pydirectinput.click(x=x, y=y, button="left")
            sleep(100, 200)
            pydirectinput.click(x=x, y=y, button="left")
            sleep(100, 200)
            pydirectinput.click(x=x, y=y, button="left")
            sleep(100, 200)
            pydirectinput.click(x=x, y=y, button="left")
            sleep(100, 200)
            pydirectinput.click(x=x, y=y, button="left")
            break

    mouseMoveTo(x=914, y=638)
    sleep(800, 900)
    pydirectinput.click(x=x, y=y, button="left")
    sleep(100, 200)
    pydirectinput.click(x=x, y=y, button="left")
    sleep(100, 200)
    pydirectinput.click(x=x, y=y, button="left")
    sleep(100, 200)
    pydirectinput.click(x=x, y=y, button="left")
    sleep(100, 200)
    pydirectinput.click(x=x, y=y, button="left")

    #TODO: move to main.py
    logging.info("[Charac]: " + str(currentCharacter) + ": " + "[Status]: floor1")
    return True