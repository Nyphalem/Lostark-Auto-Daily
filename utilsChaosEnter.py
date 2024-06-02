import pyautogui
import pydirectinput
import logging
from originConfig import config
from utils import *

def chaosEnter(currentCharacter):
    sleepCommonProcess()

    # select chaos dungeon level based on current Character
    _curr = config["characters"][currentCharacter]
    chaosTabPosition = {
        # punika
        1100: [[1320, 270], [410, 382+20]],
        1310: [[1320, 270], [410, 455+20]],
        1325: [[1320, 270], [410, 525+20]],
        1340: [[1320, 270], [410, 580+20]],
        1355: [[1320, 270], [410, 655+20]],
        1370: [[1320, 270], [410, 731+20]],
        1385: [[1320, 270], [410, 796+20]],
        1400: [[1320, 270], [410, 865+20]],
        # south vern
        1415: [[1560, 265], [410, 382+20]],
        1445: [[1560, 265], [410, 455+20]],
        1475: [[1560, 265], [410, 525+20]],
        1490: [[1560, 265], [410, 580+20]],
        1520: [[1560, 265], [410, 655+20]],
        1540: [[1560, 265], [410, 731+20]],
        1560: [[1560, 265], [410, 796+20]],
    }
    if _curr["ilvl-aor"] not in chaosTabPosition:
        logging.info("[Charac]: <" + str(currentCharacter) + ">: " + "[Chaos]: {LV too low, cannot enter}")
        return False

    logging.info("[Charac]: <" + str(currentCharacter) + ">: " + "[Chaos]: {Choose}")
    pydirectinput.keyDown("alt")
    sleepClickOrPress()
    pydirectinput.press("q")
    sleepClickOrPress()
    pydirectinput.keyUp("alt")
    sleepClickOrPressLong()

    mouseMoveTo(x=886, y=316)
    sleepClickOrPress()
    pydirectinput.click(x=886, y=316, button="left")
    sleepClickOrPress()
    mouseMoveTo(x=886, y=316)
    sleepClickOrPress()
    pydirectinput.click(x=886, y=316, button="left")
    sleepClickOrPressLong()

    mouseMoveTo(
        x=chaosTabPosition[_curr["ilvl-aor"]][0][0],
        y=chaosTabPosition[_curr["ilvl-aor"]][0][1],
    )
    sleepClickOrPressLong()
    pydirectinput.click(
        x=chaosTabPosition[_curr["ilvl-aor"]][0][0],
        y=chaosTabPosition[_curr["ilvl-aor"]][0][1],
        button="left",
    )
    sleepClickOrPressLong()
    mouseMoveTo(
        x=chaosTabPosition[_curr["ilvl-aor"]][1][0],
        y=chaosTabPosition[_curr["ilvl-aor"]][1][1],
    )
    sleepClickOrPressLong()
    pydirectinput.click(
        x=chaosTabPosition[_curr["ilvl-aor"]][1][0],
        y=chaosTabPosition[_curr["ilvl-aor"]][1][1],
        button="left",
    )
    sleepClickOrPressLong()

    enterButton = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-enter.png",
        confidence=0.75,
    )
    if enterButton != None:
        x, y = enterButton
        mouseMoveTo(x=x, y=y)
        sleepClickOrPressLong()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPressLong()

        # press confirm
        mouseMoveTo(x=914, y=638)
        sleepClickOrPressLong()
        pydirectinput.click(x=914, y=638, button="left")
        sleepClickOrPressLong()
        logging.info("[Charac]: <" + str(currentCharacter) + ">: " + "[Chaos]: {Enter}")
        sleepTransportLoading()
        return True

    logging.info("[Charac]: <" + str(currentCharacter) + ">: " + "[Chaos]: {Not Enter}")
    return False