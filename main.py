from config import config
from abilities import abilities
import pyautogui
import pydirectinput
import time
import argparse
from datetime import date
from datetime import datetime
import logging
from utils import *
from utilsChaos import *

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
    sleepCommonProcess()
    mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
    sleepClickOrPress()
    pydirectinput.click(button="right")
    sleepCommonProcess()

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
            mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
            sleepClickOrPress()
            # switch character
            if states["multiCharacterMode"]:
                if sum(states["multiCharacterModeState"]) == 0:
                    logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[Chaos]: {finish}")

                    # daily quest
                    if needDoDailyQuest():
                        doGuildDonation()
                        doIvnaDaily()
                        update_status_value(config_file_path, 'need_do_dailyQuest', False)

                    # weekly quest
                    if needDoWeeklyQuest():
                        acceptIvnaWeekly()
                        acceptGuildQuest()
                        doGuildVoyage()
                        update_status_value(config_file_path, 'need_do_weeklyQuest', False)

                    # back to manor
                    pydirectinput.press("f2")
                    sleepTransportLoading()

                    # finish all characters' daily and switch to character #1 to desire island
                    states["multiCharacterMode"] = False
                    states["multiCharacterModeState"] = []
                    sleepCommonProcess()
                    if skip_desire:
                        switchToCharacter(0)
                    else:
                        switchToCharacter(1)
                    sleepCommonProcess()

                    logging.info("执行时间: " + str(processMin) + "m " + str(processSec) + "s " + str(processMsc) + "ms")
                    print("------------------------------------")
                    print("所有角色打卡完毕")
                    print("------------------------------------")

                elif states["multiCharacterModeState"][states["currentCharacter"]] <= 0:
                    logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[Chaos]: {finish}")

                    # daily quest
                    if needDoDailyQuest():
                        doGuildDonation()
                        doIvnaDaily()

                    # weekly quest
                    if needDoWeeklyQuest():
                        acceptIvnaWeekly()
                        acceptGuildQuest()
                        doGuildVoyage()

                    # back to manor
                    pydirectinput.press("f2")
                    sleepTransportLoading()

                    # switch to the next character
                    nextIndex = (states["currentCharacter"] + 1) % len(
                        states["multiCharacterModeState"]
                    )
                    logging.info(
                        "[Charac]: <{}>: [Switch]: <{}>".format(
                            states["currentCharacter"], nextIndex
                        )
                    )
                    sleepCommonProcess()
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
                    sleepClickOrPress()
                    startTime = int(time.time_ns() / 1000000)
                    if states["multiCharacterModeState"][states["currentCharacter"]] == 2:
                        logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[Chaos]: {start}")

            # 生命周期最后：刷渴望岛
            if not states["multiCharacterMode"]:
                if not skip_desire:
                    desire_island_key_list = [[1698,347],[1475,576],[920,675]]
                    for key in desire_island_key_list:
                        x = key[0]
                        y = key[1]
                        mouseMoveTo(x=x, y=y)
                        sleepClickOrPressLong()
                        pydirectinput.click(x=x, y=y, button="left")
                        sleepClickOrPressLong()
                    desire.desire()
                    sleepCommonProcess()
                return

            #TODO: need reserve this?
            states["instanceStartTime"] = int(time.time_ns() / 1000000)
            states["abilityScreenshots"] = []
            states["bossBarLocated"] = False

        logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[Chaos]: {enter}")
        #TODO: enable this -> autoChaos()
        states["multiCharacterModeState"][states["currentCharacter"]] -= 1
        logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[Chaos]: {exit}")


#===========================================================================
# Common Action functions
#===========================================================================
def doFarmingInMasyaf():
    pydirectinput.keyDown('f2')
    sleepClickOrPress()
    pydirectinput.keyUp('f2')
    sleepTransportLoading()

    # open dash board
    pydirectinput.keyDown('ctrl')
    sleepClickOrPress()
    pydirectinput.keyDown('1')
    sleepClickOrPress()
    pydirectinput.keyUp('ctrl')
    sleepClickOrPress()
    pydirectinput.keyUp('1')
    sleepClickOrPress()

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
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPressList()
    sleepCommonProcess()
    pydirectinput.keyDown('esc')
    sleepClickOrPress()
    pydirectinput.keyUp('esc')
    sleepCommonProcess()

    # farm
    farm_key_list = [[252,301],[216,382],[956,947],[911,676],[971,746],
                        [1291,950],[737,845],[914,651]]
    for key in farm_key_list:
        x = key[0]
        y = key[1]
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPressList()
    sleepCommonProcess()
    pydirectinput.keyDown('esc')
    sleepClickOrPress()
    pydirectinput.keyUp('esc')
    sleepClickOrPress()
    pydirectinput.keyDown('esc')
    sleepClickOrPress()
    pydirectinput.keyUp('esc')
    sleepCommonProcess()
    pydirectinput.keyDown('esc')
    sleepClickOrPress()
    pydirectinput.keyUp('esc')


def doGuildDonation():
    logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[GuildDonation]: {start}")
    sleepClickOrPress()
    pydirectinput.keyDown("alt")
    sleepClickOrPress()
    pydirectinput.press("u")
    sleepClickOrPress()
    pydirectinput.keyUp("alt")
    sleepCommonProcess()

    ok = pyautogui.locateCenterOnScreen(
        "./screenshots/ok.png",
        region=config["regions"]["center"],
        confidence=0.75
    )

    if ok != None:
        x, y = ok
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
    sleepCommonProcess()

    mouseMoveTo(x=1600, y=970)
    sleepClickOrPress()
    pydirectinput.click(button="left")
    sleepClickOrPress()
    pydirectinput.click(button="left")
    sleepClickOrPress()
    pydirectinput.click(button="left")
    sleepClickOrPress()

    # donoate silver
    mouseMoveTo(x=700, y=595)
    sleepClickOrPress()
    pydirectinput.click(button="left")
    sleepClickOrPress()
    pydirectinput.click(button="left")
    sleepClickOrPress()
    pydirectinput.click(button="left")
    sleepClickOrPress()

    pydirectinput.press("esc")
    sleepCommonProcess()

    supportResearch = pyautogui.locateCenterOnScreen(
        "./screenshots/supportResearch.png",
        confidence=0.8,
    )

    if supportResearch != None:
        x, y = supportResearch
        logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[GuildDonation]: supportResearch")
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.click(button="left")
        sleepClickOrPress()
        pydirectinput.click(button="left")
        sleepClickOrPress()
        pydirectinput.click(button="left")
        sleepCommonProcess()

        canSupportResearch = pyautogui.locateCenterOnScreen(
            "./screenshots/canSupportResearch.png",
            confidence=0.8,
        )

        if canSupportResearch != None:
            x, y = canSupportResearch
            mouseMoveTo(x=x, y=y)
            sleepClickOrPress()
            pydirectinput.click(button="left")
            sleepClickOrPress()
            pydirectinput.click(button="left")
            sleepClickOrPress()
            pydirectinput.click(button="left")
            sleepClickOrPress()

            mouseMoveTo(x=910, y=780)
            sleepClickOrPress()
            pydirectinput.click(button="left")
            sleepClickOrPress()
            pydirectinput.click(button="left")
            sleepClickOrPress()
            pydirectinput.click(button="left")
            sleepClickOrPress()
        else:
            pydirectinput.press("esc")
            sleepClickOrPress()

    sleepCommonProcess()
    pydirectinput.press("esc")
    sleepCommonProcess()
    logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[GuildDonation]: {finish}")


def doIvnaDaily():
    logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[IvnaDaily]: {start}")
    sleepClickOrPress()
    pydirectinput.keyDown("alt")
    sleepClickOrPress()
    pydirectinput.press("j")
    sleepClickOrPress()
    pydirectinput.keyUp("alt")
    sleepCommonProcess()

    # accept quest
    acceptQuest_key_list = [[1280,378],[1280,456]]
    for key in acceptQuest_key_list:
        x = key[0]
        y = key[1]
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPress()
    pydirectinput.press("esc")
    sleepCommonProcess()

    # finish quest #1
    pydirectinput.press("5")
    sleepCommonProcess()
    quest1_key_list = [[1698,347],[1475,413],[920,675],[1650,420],[356,772]]
    i = 0
    for key in quest1_key_list:
        i += 1
        x = key[0]
        y = key[1]
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPressList()
        if i == 3:
            sleepTransportLoading()
    rainbow = pyautogui.locateCenterOnScreen(
        "./screenshots/rainbow-interface.png",
        confidence=0.7,
        grayscale=True
    )
    if not rainbow == None:
        pydirectinput.press("esc")
        sleepClickOrPressLong()

    # finish quest #2
    quest2_key_list = [[1698,347],[1474,490],[920,675]]
    i = 0
    for key in quest2_key_list:
        i += 1
        x = key[0]
        y = key[1]
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPressList()
    sleepTransportLoading()
    pydirectinput.press("f4")
    sleepSongSky()
    pydirectinput.press("f4")
    sleepSongSky()
    pydirectinput.press("g")
    sleepClickOrPressLong()
    pydirectinput.press("g")
    sleepClickOrPressLong()
    pydirectinput.press("g")
    sleepClickOrPressLong()
    pydirectinput.press("g")
    sleepCommonProcess()

    logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[IvnaDaily]: {finish}")
    return


def acceptIvnaWeekly():
    logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[IvnaWeekly]: {accpet}")
    sleepClickOrPress()
    pydirectinput.keyDown("alt")
    sleepClickOrPress()
    pydirectinput.press("j")
    sleepClickOrPress()
    pydirectinput.keyUp("alt")
    sleepCommonProcess()

    # accept quest
    acceptQuest_key_list = [[583,193],[1280,360],[1280,440],[1280,513]]
    for key in acceptQuest_key_list:
        x = key[0]
        y = key[1]
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPress()
    pydirectinput.press("esc")
    sleepCommonProcess()

    return


def acceptGuildQuest():
    logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[GuildQuest]: {accpet}")
    sleepClickOrPress()
    pydirectinput.keyDown("alt")
    sleepClickOrPress()
    pydirectinput.press("j")
    sleepClickOrPress()
    pydirectinput.keyUp("alt")
    sleepCommonProcess()

    #TODO: check have cube
    #logging.info("not set guild quest already")
    #manageGuildQuest()

    # accept quest
    acceptQuest_key_list = [[890,193],[1280,516],[1280,593],[1280,666]]
    for key in acceptQuest_key_list:
        x = key[0]
        y = key[1]
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPressList()
    pydirectinput.press("esc")
    sleepCommonProcess()

    return


def manageGuildQuest():
    logging.info("TODO: manageGuildQuest")
    return


def doGuildVoyage():
    if states["currentCharacter"] == 1:
        return
    logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[GuildVoyage]: {start}")

    # complete guild voyage
    sleepCommonProcess()
    quest1_key_list = [[1698,347],[1475,585],[920,675]]
    i = 0
    for key in quest1_key_list:
        i += 1
        x = key[0]
        y = key[1]
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPressList()
        if i == 3:
            sleepTransportLoading()
    rainbow = pyautogui.locateCenterOnScreen(
        "./screenshots/rainbow-interface.png",
        confidence=0.7,
        grayscale=True
    )
    if not rainbow == None:
        pydirectinput.press("esc")
        sleepClickOrPressLong()

    pydirectinput.press("m")
    sleepClickOrPressLong()

    voyage = pyautogui.locateOnScreen(
        "./screenshots/voyage-location.png",
        confidence=0.9,
        grayscale=True
    )
    if voyage == None:
        pydirectinput.press("f2")
        sleepTransportLoading()
    else:
        x1, y1, w1, h1 = voyage
        x = x1 + w1 + 10
        y = y1
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.keyDown("alt")
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPress()
        pydirectinput.keyUp("alt")
        pydirectinput.press("m")
        sleepVoyage()

        # back2city
        pydirectinput.press("f3")
        sleepTransportLoading()

        # completeQuest
        mouseMoveTo(x=1658, y=430)
        sleepClickOrPress()
        pydirectinput.click(x=1658, y=430, button="left")
        sleepClickOrPressLong()
        mouseMoveTo(x=360, y=780)
        sleepClickOrPress()
        pydirectinput.click(x=360, y=780, button="left")
        sleepClickOrPressLong()

        # repair ship
        pydirectinput.press("m")
        sleepClickOrPressLong()
        pydirectinput.click(x=1095, y=945, button="left")
        sleepClickOrPressLong()
        ok = pyautogui.locateCenterOnScreen(
            "./screenshots/ok.png",
            confidence=0.7,
            grayscale=True
        )
        if ok == None:
            logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[GuildVoyage]: {Error: repair ship no ok}")
            pydirectinput.press("esc")
            sleepClickOrPressLong()
            pydirectinput.press("esc")
            sleepClickOrPressLong()
        else:
            x, y = ok
            mouseMoveTo(x=x, y=y)
            pydirectinput.click(x=x, y=y, button="left")
            sleepTransportLoading()
            pydirectinput.click(x=1130, y=1050, button="left")
            sleepClickOrPressLong()
            ok = pyautogui.locateCenterOnScreen(
                "./screenshots/ok.png",
                confidence=0.7,
                grayscale=True
            )
            if ok != None:
                x, y = ok
                mouseMoveTo(x=x, y=y)
                pydirectinput.click(x=x, y=y, button="left")
                sleepClickOrPressLong()
                pydirectinput.click(x=1815, y=1065, button="left")
                sleepClickOrPressLong()
                pydirectinput.press("f2")
                sleepTransportLoading()

    return


def switchToCharacter(index):
    sleepClickOrPressLong()
    pydirectinput.press("esc")
    sleepClickOrPressLong()
    mouseMoveTo(x=config["charSwitchX"], y=config["charSwitchY"])
    sleepClickOrPressLong()
    pydirectinput.click(x=config["charSwitchX"], y=config["charSwitchY"], button="left")
    sleepClickOrPressLong()

    mouseMoveTo(
        x=config["charPositions"][index][0],
        y=config["charPositions"][index][1]
    )
    sleepClickOrPressLong()
    pydirectinput.click(
        x=config["charPositions"][index][0],
        y=config["charPositions"][index][1],
        button="left",
    )
    sleepClickOrPressLong()

    mouseMoveTo(x=config["charSelectConnectX"], y=config["charSelectConnectY"])
    sleepClickOrPressLong()
    pydirectinput.click(
        x=config["charSelectConnectX"], y=config["charSelectConnectY"], button="left"
    )
    sleepClickOrPressLong()

    mouseMoveTo(x=config["charSelectOkX"], y=config["charSelectOkY"])
    sleepClickOrPressLong()
    pydirectinput.click(
        x=config["charSelectOkX"], y=config["charSelectOkY"], button="left"
    )
    sleepClickOrPressLong()

    states["currentCharacter"] = index

    # wait black screen
    sleepTransportLoading()


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


if __name__ == "__main__":
    states = newStates.copy()
    main()
