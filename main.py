from config import config
from abilities import abilities
import pyautogui
import pydirectinput
import time
import random
import math
import argparse
from datetime import date
from datetime import datetime
import json
import logging

import desire

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

config_file_path = 'config.json'

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


def main():
    print("------------------------------------")
    print("5秒后开始")
    print("------------------------------------")

    # Instantiate the parser
    parser = argparse.ArgumentParser(description="Optional app description")
    parser.add_argument("--all", action="store_true", help="A boolean switch")
    parser.add_argument("--skip", action="store_true", help="A boolean switch")
    args = parser.parse_args()

    skip_desire = False

    # cold init
    sleep(5000, 5500)
    mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
    sleep(200, 300)
    pydirectinput.click(button="right")
    sleep(3000, 4000)

    # check cmd parameter
    if args.all:
        states["multiCharacterMode"] = True
        for i in range(len(config["characters"])):
            states["multiCharacterModeState"].append(2)
        print(
            "runs on all characters: {}".format(
                states["multiCharacterModeState"]
            )
        )

    if args.skip:
        skip_desire = True

    # Farm in Masyaf
    print("------------------------------------")
    if needDoFarmingInMasyaf():
        print("Farming in Masyaf")
        doFarmingInMasyaf()
        update_status_value(config_file_path, 'need_do_farmingInMasyaf', False)
    else:
        print("Skip Farming in Masyaf")
    print("------------------------------------")

    # save bot start time
    states["botStartTime"] = int(time.time_ns() / 1000000)

    # main process
    while True:
        if states["status"] == "inCity":
            sleep(1000, 1200)

            mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
            sleep(100, 200)

            repair()

            # switch character
            if states["multiCharacterMode"]:
                if sum(states["multiCharacterModeState"]) == 0:
                    repair()

                    # daily quest
                    if needDoDailyQuest():
                        doGuildDonation()
                        doIvnaDaily()
                        update_status_value(config_file_path, 'need_do_dailyQuest', False)

                    # weekly quest
                    if needDoWeeklyQuest():
                        acceptIvnaWeekly()
                        acceptGuildCube()
                        acceptGuildVoyage()
                        doGuildVoyage()
                        update_status_value(config_file_path, 'need_do_weeklyQuest', False)

                    # back to city
                    pydirectinput.press("f2")
                    sleep(20000, 22000)

                    # finish all characters' daily and switch to character #1 to desire island
                    states["multiCharacterMode"] = False
                    states["multiCharacterModeState"] = []
                    sleep(3400, 3600)
                    if skip_desire:
                        switchToCharacter(0)
                    else:
                        switchToCharacter(1)
                    sleep(3400, 3600)

                    print("------------------------------------")
                    print("所有角色打卡完毕")
                    print("------------------------------------")

                elif states["multiCharacterModeState"][states["currentCharacter"]] <= 0:
                    logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[Chaos]: {finish}")

                    repair()

                    if needDoDailyQuest():
                        doGuildDonation()
                        doIvnaDaily()

                    # weekly quest
                    if needDoWeeklyQuest():
                        acceptIvnaWeekly()
                        acceptGuildCube()
                        acceptGuildVoyage()
                        doGuildVoyage()

                    # back to Masyaf
                    pydirectinput.press("f2")
                    sleep(20000, 22000)

                    # switch to the next character
                    nextIndex = (states["currentCharacter"] + 1) % len(
                        states["multiCharacterModeState"]
                    )
                    logging.info(
                        "[Charac]: <{}>: [Switch]: <{}>".format(
                            states["currentCharacter"], nextIndex
                        )
                    )
                    sleep(3400, 3600)
                    switchToCharacter(nextIndex)

                    # caculate process time
                    endTime = int(time.time_ns() / 1000000)
                    processTime = endTime - startTime
                    processMsc = processTime % 1000
                    processTime = int(processTime / 1000)
                    processSec = processTime % 60
                    processTime = int(processTime / 60)
                    processMin = processTime
                    logging.info("执行时间: " + str(processMin) + "m " + str(processSec) + "s " + str(processMsc) + "ms")
                    print("------------------------------------")
                    continue
                else:
                    sleep(500, 600)
                    startTime = int(time.time_ns() / 1000000)
                    if states["multiCharacterModeState"][states["currentCharacter"]] == 2:
                        logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[Chaos]: {start}")
                    #TODO: enable this -> enterChaos()

            # 生命周期最后：最后切换的账号无限刷
            if not states["multiCharacterMode"]:
                if not skip_desire:
                    desire_island_key_list = [[1698,347],[1475,576],[920,675]]
                    for key in desire_island_key_list:
                        x = key[0]
                        y = key[1]
                        mouseMoveTo(x=x, y=y)
                        sleep(1020, 1200)
                        pydirectinput.click(x=x, y=y, button="left")
                        sleep(1020, 1200)
                    desire.desire()
                    sleep(3400, 3600)
                return

            # save instance start time
            states["instanceStartTime"] = int(time.time_ns() / 1000000)
            # initialize new states
            states["abilityScreenshots"] = []
            states["bossBarLocated"] = False


        #TODO: enable this -> fight chaos
        logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[Chaos]: {enter}")
        states["multiCharacterModeState"][states["currentCharacter"]] -= 1
        logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[Chaos]: {exit}")
        '''
        elif states["status"] == "floor1":
            logging.info("floor1")
            sleep(1000, 1300)
            # wait for loading
            waitForLoading()
            mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
            sleep(100, 200)
            if checkTimeout():
                quitChaos()
                continue
            sleep(1000, 1200)
            logging.info("floor1 loaded")

            # saving clean abilities icons
            saveAbilitiesScreenshots()

            # do floor one
            doFloor1()
        elif states["status"] == "floor2":
            logging.info("floor2")
            sleep(1000, 1300)
            # wait for loading
            waitForLoading()
            mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
            sleep(100, 200)
            if checkTimeout():
                quitChaos()
                continue
            logging.info("floor2 loaded")
            # do floor two
            doFloor2()
        elif states["status"] == "floor3":
            logging.info("floor3")
            sleep(1000, 1300)
            # wait for loading
            waitForLoading()
            mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
            sleep(100, 200)
            if checkTimeout():
                quitChaos()
                continue
            logging.info("floor3 loaded")
            mouseMoveTo(x=760, y=750)
            sleep(100, 120)
            pydirectinput.click(button=config["move"])
            sleep(200, 300)
            pydirectinput.click(button=config["move"])
            sleep(200, 300)
            if checkTimeout() or states["floor3Mode"] == False:
                quitChaos()
                continue
            doFloor3()
        '''


#===========================================================================
# Chaos Dungeon Action functions
#===========================================================================
def enterChaos():
    blackScreenStartTime = int(time.time_ns() / 1000000)
        # wait for last run black screen

    while True:
        im = pyautogui.screenshot(region=(1652, 168, 240, 210))
        r, g, b = im.getpixel((1772 - 1652, 272 - 168))
        if r + g + b > 10:
            break
        sleep(200, 300)

        currentTime = int(time.time_ns() / 1000000)
        if currentTime - blackScreenStartTime > config["blackScreenTimeLimit"]:
            logging.info("[Error] [Misc]: black screen too long time")
            return
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
        _curr = config["characters"][states["currentCharacter"]]
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
        if states["multiCharacterMode"]:
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

    states["status"] = "floor1"
    logging.info("[Charac]: " + str(states["currentCharacter"]) + ": " + "[Status]: floor1")
    return


#===========================================================================
# Common Action functions
#===========================================================================
def doFarmingInMasyaf():
    pydirectinput.keyDown('f2')
    sleep(300, 400)
    pydirectinput.keyUp('f2')

    sleep(20000, 21000)

    # open dash board
    pydirectinput.keyDown('ctrl')
    sleep(300, 400)
    pydirectinput.keyDown('1')
    sleep(300, 400)
    pydirectinput.keyUp('ctrl')
    sleep(300, 400)
    pydirectinput.keyUp('1')

    # quest
    qutst_key_list = [[143,300],[216,382],[988,256],[966,912],
                      [678,390],[1845,420],[969,762],
                      [678,390],[1593,685],[1779,920],[941,677],
                      [685,463],[1593,685],[1779,920],[941,677],
                      [599,534],[1593,685],[1779,920],[941,677]]
    for key in qutst_key_list:
        x = key[0]
        y = key[1]
        mouseMoveTo(x=x, y=y)
        sleep(300, 400)
        pydirectinput.click(x=x, y=y, button="left")
        sleep(300, 400)
        pydirectinput.click(x=x, y=y, button="left")
        sleep(2000, 2500)
    sleep(3000,4000)
    pydirectinput.keyDown('esc')
    sleep(300, 400)
    pydirectinput.keyUp('esc')
    sleep(10000,11000)

    # farm
    farm_key_list = [[252,301],[216,382],[956,947],[911,676],[971,746],
                     [1291,950],[737,845],[914,651]]
    for key in farm_key_list:
        x = key[0]
        y = key[1]
        mouseMoveTo(x=x, y=y)
        sleep(300, 400)
        pydirectinput.click(x=x, y=y, button="left")
        sleep(300, 400)
        pydirectinput.click(x=x, y=y, button="left")
        sleep(2000, 2500)
    sleep(3000,4000)
    pydirectinput.keyDown('esc')
    sleep(300, 400)
    pydirectinput.keyUp('esc')
    sleep(300, 400)
    pydirectinput.keyDown('esc')
    sleep(300, 400)
    pydirectinput.keyUp('esc')

    sleep(1000, 2000)
    pydirectinput.keyDown('esc')
    sleep(300, 400)
    pydirectinput.keyUp('esc')


def doGuildDonation():
    logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[GuildDonation]: {start}")
    sleep(300, 400)
    pydirectinput.keyDown("alt")
    sleep(300, 400)
    pydirectinput.press("u")
    sleep(300, 400)
    pydirectinput.keyUp("alt")
    sleep(4100, 5200)

    ok = pyautogui.locateCenterOnScreen(
        "./screenshots/ok.png",
        region=config["regions"]["center"],
        confidence=0.75
    )

    if ok != None:
        x, y = ok
        mouseMoveTo(x=x, y=y)
        sleep(300, 400)
        pydirectinput.click(x=x, y=y, button="left")
        sleep(300, 400)
        pydirectinput.click(x=x, y=y, button="left")
    sleep(1500, 1600)

    mouseMoveTo(x=1600, y=970)
    sleep(500, 600)
    pydirectinput.click(button="left")
    sleep(500, 600)
    pydirectinput.click(button="left")
    sleep(500, 600)
    pydirectinput.click(button="left")
    sleep(500, 600)

    # donoate silver
    mouseMoveTo(x=700, y=595)
    sleep(500, 600)
    pydirectinput.click(button="left")
    sleep(500, 600)
    pydirectinput.click(button="left")
    sleep(500, 600)
    pydirectinput.click(button="left")
    sleep(500, 600)

    pydirectinput.press("esc")
    sleep(3500, 3600)

    supportResearch = pyautogui.locateCenterOnScreen(
        "./screenshots/supportResearch.png",
        confidence=0.8,
    )

    if supportResearch != None:
        x, y = supportResearch
        logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[GuildDonation]: supportResearch")
        mouseMoveTo(x=x, y=y)
        sleep(500, 600)
        pydirectinput.click(button="left")
        sleep(500, 600)
        pydirectinput.click(button="left")
        sleep(500, 600)
        pydirectinput.click(button="left")
        sleep(1500, 1600)

        canSupportResearch = pyautogui.locateCenterOnScreen(
            "./screenshots/canSupportResearch.png",
            confidence=0.8,
        )

        if canSupportResearch != None:
            x, y = canSupportResearch
            mouseMoveTo(x=x, y=y)
            sleep(500, 600)
            pydirectinput.click(button="left")
            sleep(500, 600)
            pydirectinput.click(button="left")
            sleep(500, 600)
            pydirectinput.click(button="left")
            sleep(500, 600)

            mouseMoveTo(x=910, y=780)
            sleep(500, 600)
            pydirectinput.click(button="left")
            sleep(500, 600)
            pydirectinput.click(button="left")
            sleep(500, 600)
            pydirectinput.click(button="left")
            sleep(500, 600)
        else:
            pydirectinput.press("esc")
            sleep(800, 900)

    sleep(2800, 2900)
    pydirectinput.press("esc")
    sleep(800, 900)

    logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[GuildDonation]: {finish}")


def doIvnaDaily():
    logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[IvnaDaily]: {start}")
    sleep(300, 400)
    pydirectinput.keyDown("alt")
    sleep(300, 400)
    pydirectinput.press("j")
    sleep(300, 400)
    pydirectinput.keyUp("alt")
    sleep(4100, 5200)

    # accept quest
    acceptQuest_key_list = [[1280,378],[1280,456]]
    for key in acceptQuest_key_list:
        x = key[0]
        y = key[1]
        mouseMoveTo(x=x, y=y)
        sleep(300, 400)
        pydirectinput.click(x=x, y=y, button="left")
        sleep(300, 400)
    pydirectinput.press("esc")
    sleep(2000, 2500)

    # finish quest #1
    pydirectinput.press("5")
    sleep(3000, 3500)
    quest1_key_list = [[1698,347],[1475,413],[920,675],[1650,420],[356,772]]
    i = 0
    for key in quest1_key_list:
        i += 1
        x = key[0]
        y = key[1]
        mouseMoveTo(x=x, y=y)
        sleep(1020, 1200)
        pydirectinput.click(x=x, y=y, button="left")
        sleep(1020, 1200)
        if i == 3:
            sleep(20000, 22000)
    rainbow = pyautogui.locateCenterOnScreen(
        "./screenshots/rainbow-interface.png",
        confidence=0.7,
        grayscale=True
    )
    if not rainbow == None:
        pydirectinput.press("esc")
        sleep(800, 900)

    # finish quest #2
    quest2_key_list = [[1698,347],[1474,490],[920,675]]
    i = 0
    for key in quest2_key_list:
        i += 1
        x = key[0]
        y = key[1]
        mouseMoveTo(x=x, y=y)
        sleep(1020, 1200)
        pydirectinput.click(x=x, y=y, button="left")
        sleep(1020, 1200)
    sleep(20000, 22000)
    pydirectinput.press("f4")
    sleep(20000, 22000)
    pydirectinput.press("f4")
    sleep(11000, 13000)
    pydirectinput.press("g")
    sleep(1000, 2000)
    pydirectinput.press("g")
    sleep(1000, 2000)
    pydirectinput.press("g")
    sleep(1000, 2000)
    pydirectinput.press("g")
    sleep(3000, 4000)

    logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[IvnaDaily]: {finish}")
    return


def acceptIvnaWeekly():
    if states["currentCharacter"] == 6 or states["currentCharacter"] == 7:
        return
    logging.info("TODO: acceptIvnaWeekly")

    return


def acceptGuildCube():
    if states["currentCharacter"] == 6 or states["currentCharacter"] == 7:
        return
    logging.info("TODO: acceptGuildCube")
    if True:
        logging.info("not set guild quest already")
        manageGuildQuest()
    return


def manageGuildQuest():
    if states["currentCharacter"] == 6 or states["currentCharacter"] == 7:
        return
    logging.info("TODO: manageGuildQuest")
    return


def acceptGuildVoyage():
    if states["currentCharacter"] == 6 or states["currentCharacter"] == 7:
        return
    logging.info("TODO: acceptGuildVoyage")
    return


def doGuildVoyage():
    if states["currentCharacter"] == 6 or states["currentCharacter"] == 7:
        return
    logging.info("TODO: doGuildVoyage")
    return


def switchToCharacter(index):
    sleep(1500, 1600)
    pydirectinput.press("esc")
    sleep(2500, 2600)
    mouseMoveTo(x=config["charSwitchX"], y=config["charSwitchY"])
    sleep(1500, 1600)
    mouseMoveTo(x=config["charSwitchX"], y=config["charSwitchY"])
    mouseMoveTo(x=config["charSwitchX"], y=config["charSwitchY"])
    sleep(1500, 1600)
    pydirectinput.click(x=config["charSwitchX"], y=config["charSwitchY"], button="left")
    sleep(1500, 1600)
    pydirectinput.click(x=config["charSwitchX"], y=config["charSwitchY"], button="left")
    sleep(500, 600)
    pydirectinput.click(x=config["charSwitchX"], y=config["charSwitchY"], button="left")
    sleep(200, 300)

    '''
    mouseMoveTo(x=1260, y=392)
    sleep(1500, 1600)
    pydirectinput.click(x=1260, y=392, button="left")
    sleep(1500, 1600)
    pydirectinput.click(x=1260, y=392, button="left")
    sleep(1500, 1600)
    pydirectinput.click(x=1260, y=392, button="left")
    sleep(500, 600)
    pydirectinput.click(x=1260, y=392, button="left")
    sleep(1500, 1600)
    pydirectinput.click(x=1260, y=392, button="left")
    sleep(1500, 1600)
    if index > 8:
        # mouseMoveTo(
        #     x=config["charPositions"][index][0], y=config["charPositions"][index][1]
        # )
        # pyautogui.scroll(-5)
        # sleep(1500, 1600)
        mouseMoveTo(x=1260, y=638)
        sleep(1500, 1600)
        pydirectinput.click(x=1260, y=638, button="left")
        sleep(1500, 1600)
        pydirectinput.click(x=1260, y=638, button="left")
        sleep(1500, 1600)
        pydirectinput.click(x=1260, y=638, button="left")
        sleep(500, 600)
        pydirectinput.click(x=1260, y=638, button="left")
        sleep(1500, 1600)
        pydirectinput.click(x=1260, y=638, button="left")
        sleep(1500, 1600)
    '''

    mouseMoveTo(
        x=config["charPositions"][index][0], y=config["charPositions"][index][1]
    )
    sleep(1500, 1600)
    pydirectinput.click(
        x=config["charPositions"][index][0],
        y=config["charPositions"][index][1],
        button="left",
    )
    sleep(1500, 1600)
    pydirectinput.click(
        x=config["charPositions"][index][0],
        y=config["charPositions"][index][1],
        button="left",
    )
    sleep(500, 600)
    mouseMoveTo(
        x=config["charPositions"][index][0], y=config["charPositions"][index][1]
    )
    sleep(500, 600)
    pydirectinput.click(
        x=config["charPositions"][index][0],
        y=config["charPositions"][index][1],
        button="left",
    )
    sleep(1200, 1300)
    pydirectinput.click(
        x=config["charPositions"][index][0],
        y=config["charPositions"][index][1],
        button="left",
    )
    sleep(1500, 1600)
    pydirectinput.click(
        x=config["charPositions"][index][0],
        y=config["charPositions"][index][1],
        button="left",
    )
    sleep(1500, 1600)

    mouseMoveTo(x=config["charSelectConnectX"], y=config["charSelectConnectY"])
    sleep(1500, 1600)
    pydirectinput.click(
        x=config["charSelectConnectX"], y=config["charSelectConnectY"], button="left"
    )
    sleep(200, 300)
    pydirectinput.click(
        x=config["charSelectConnectX"], y=config["charSelectConnectY"], button="left"
    )
    sleep(500, 600)
    pydirectinput.click(
        x=config["charSelectConnectX"], y=config["charSelectConnectY"], button="left"
    )
    sleep(200, 300)
    pydirectinput.click(
        x=config["charSelectConnectX"], y=config["charSelectConnectY"], button="left"
    )
    sleep(500, 600)
    pydirectinput.click(
        x=config["charSelectConnectX"], y=config["charSelectConnectY"], button="left"
    )
    sleep(1000, 1000)

    mouseMoveTo(x=config["charSelectOkX"], y=config["charSelectOkY"])
    sleep(1500, 1600)
    pydirectinput.click(
        x=config["charSelectOkX"], y=config["charSelectOkY"], button="left"
    )
    sleep(200, 300)
    pydirectinput.click(
        x=config["charSelectOkX"], y=config["charSelectOkY"], button="left"
    )
    sleep(1500, 1600)
    pydirectinput.click(
        x=config["charSelectOkX"], y=config["charSelectOkY"], button="left"
    )
    sleep(200, 300)
    pydirectinput.click(
        x=config["charSelectOkX"], y=config["charSelectOkY"], button="left"
    )
    sleep(500, 600)

    states["currentCharacter"] = index
    states["abilityScreenshots"] = []

    # wait black screen
    sleep(20000, 22000)


def needDoWeeklyQuest():
    now = datetime.now()
    day_of_week_weeklyQuest = now.weekday()

    weekly_quest_status = read_status_value(config_file_path, 'need_do_weeklyQuest')

    if day_of_week_weeklyQuest == 2: # Monday is 0
        if weekly_quest_status:
            return True
        else:
            logging.info("weekly quest already done in Wednesday")
            return False
    else:
        update_status_value(config_file_path, 'need_do_weeklyQuest', True)
        return False


def needDoFarmingInMasyaf():
    now = datetime.now()
    day_of_week_farmingInMasyaf = now.weekday()
    prev_day_of_week_farmingInMasyaf = read_status_value(config_file_path, 'day_of_week_farmingInMasyaf')
    if not day_of_week_farmingInMasyaf == prev_day_of_week_farmingInMasyaf:
        update_status_value(config_file_path, 'day_of_week_farmingInMasyaf', day_of_week_farmingInMasyaf)
        update_status_value(config_file_path, 'need_do_farmingInMasyaf', True)

    need_do_farmingInMasyaf = read_status_value(config_file_path, 'need_do_farmingInMasyaf')
    if need_do_farmingInMasyaf:
        return True
    else:
        return False


def needDoDailyQuest():
    now = datetime.now()
    day_of_week_dailyQuest = now.weekday()
    prev_day_of_week_dailyQuest = read_status_value(config_file_path, 'day_of_week_dailyQuest')
    if not day_of_week_dailyQuest == prev_day_of_week_dailyQuest:
        update_status_value(config_file_path, 'day_of_week_dailyQuest', day_of_week_dailyQuest)
        update_status_value(config_file_path, 'need_do_dailyQuest', True)

    need_do_dailyQuest = read_status_value(config_file_path, 'need_do_dailyQuest')
    if need_do_dailyQuest:
        return True
    else:
        return False


def repair():
    # TODO: if config["auraRepair"]:
        # TODO: doAuraRepair(True)
    # TODO: else:
        # TODO: doCityRepair()
    # sleep(1400, 1600)
    return


#===========================================================================
# Utils functions
#===========================================================================
def sleep(min, max):
    sleepTime = random.randint(min, max) / 1000.0
    if sleepTime < 0:
        return
    time.sleep(sleepTime)


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


if __name__ == "__main__":
    states = newStates.copy()
    main()
