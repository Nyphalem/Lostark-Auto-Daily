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
        # north vern
        250: [[360, 270], [410, 382+20]],
        500: [[360, 270], [410, 455+20]],
        545: [[360, 270], [410, 525+20]],
        590: [[360, 270], [410, 580+20]],
        # Lohendire
        635: [[600, 270], [410, 382+20]],
        680: [[600, 270], [410, 455+20]],
        725: [[600, 270], [410, 525+20]],
        765: [[600, 270], [410, 580+20]],
        # Yoen
        805: [[830, 270], [410, 382+20]],
        845: [[830, 270], [410, 455+20]],
        885: [[830, 270], [410, 525+20]],
        925: [[830, 270], [410, 580+20]],
        # Feiton
        960: [[1077, 270], [410, 382+20]],
        995: [[1077, 270], [410, 455+20]],
        1030: [[1077, 270], [410, 525+20]],
        1065: [[1077, 270], [410, 580+20]],
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

    chaos_level = 0
    for index, key in enumerate(chaosTabPosition):
        if _curr["ilvl-aor"] == key:
            chaos_level = key
            break
        else:
            if index == 0:
                continue
            else:
                if _curr["ilvl-aor"] < key:
                    previous_key = list(chaosTabPosition.keys())[index - 1]
                    if _curr["ilvl-aor"] > previous_key:
                        chaos_level = previous_key
                    break

    if chaos_level == 0:
        max_level = max(chaosTabPosition.keys())
        if _curr["ilvl-aor"] > max_level:
            chaos_level = max_level

    if chaos_level == 0 or chaos_level not in chaosTabPosition:
        logging.info("[角色]: <" + str(currentCharacter+1) + ">: " + "[混沌地牢]: {错误：装备等级无效}")
        return False

    logging.info("[角色]: <" + str(currentCharacter+1) + ">: " + "[混沌地牢]: {选择}")
    pydirectinput.keyDown("alt")
    sleepClickOrPress()
    pydirectinput.press("q")
    sleepClickOrPress()
    pydirectinput.keyUp("alt")
    sleepClickOrPressLong()

    mouseMoveTo(x=886, y=316)
    sleepClickOrPress()
    pydirectinput.click(x=886, y=316, button="left")
    sleepClickOrPressLong()

    mouseMoveTo(
        x=chaosTabPosition[chaos_level][0][0],
        y=chaosTabPosition[chaos_level][0][1],
    )
    sleepClickOrPress()
    pydirectinput.click(
        x=chaosTabPosition[chaos_level][0][0],
        y=chaosTabPosition[chaos_level][0][1],
        button="left",
    )
    sleepClickOrPressLong()
    mouseMoveTo(
        x=chaosTabPosition[chaos_level][1][0],
        y=chaosTabPosition[chaos_level][1][1],
    )
    sleepClickOrPress()
    pydirectinput.click(
        x=chaosTabPosition[chaos_level][1][0],
        y=chaosTabPosition[chaos_level][1][1],
        button="left",
    )
    sleepCommonProcess()

    enterButton = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-enter.png",
        region=config["regions"]["whole-game"],
        grayscale=True,
        confidence=0.7,
    )
    if enterButton != None:
        x, y = enterButton
        mouseMoveTo(x=x, y=y)
        sleepClickOrPressLong()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPressLong()

        # press confirm
        enterConfirmButton = pyautogui.locateCenterOnScreen(
            "./screenshots/chaos-enter-confirm.png",
            region=config["regions"]["whole-game"],
            confidence=0.9,
        )
        if enterConfirmButton != None:
            x, y = enterConfirmButton
            mouseMoveTo(x=x, y=y)
            sleepClickOrPressLong()
            pydirectinput.click(x=x, y=y, button="left")
            sleepClickOrPressLong()
            logging.info("[角色]: <" + str(currentCharacter+1) + ">: " + "[混沌地牢]: {进入}: " + str(chaos_level))
            sleepTransportLoading()
            return True
        else:
            for i in range(3):
                pydirectinput.keyDown('esc')
                sleepClickOrPress()
                pydirectinput.keyUp('esc')
                sleepClickOrPress()
                logging.info("[角色]: <" + str(currentCharacter+1) + ">: " + "[混沌地牢]: {无可用次数}")
                return False


    logging.info("[角色]: <" + str(currentCharacter+1) + ">: " + "[混沌地牢]: {未进入}")
    return False