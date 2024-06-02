from originConfig import config
import pyautogui
import pydirectinput
import time
import argparse
from datetime import timedelta
from datetime import datetime
from utils import *
from utilsChaosEnter import *
from utilsChaosCombat import *
import logging
import utilsDesire


def main():
    logging.info("------------------------------------")
    logging.info("5秒后开始")
    logging.info("------------------------------------")

    # Instantiate the parser
    parser = argparse.ArgumentParser(description="脚本可选开关")
    parser.add_argument("--all", action="store_true", help="所有号都运行")
    parser.add_argument("--start", type=int, help="从哪个号开始运行")
    parser.add_argument("--desire", action="store_true", help="日常做完刷渴望岛")
    parser.add_argument("--chaos", action="store_true", help="打混沌地牢")
    parser.add_argument("--repair", action="store_true", help="修理")
    parser.add_argument("--disenchant", action="store_true", help="分解")
    parser.add_argument("--buypotion", action="store_true", help="买药")
    args = parser.parse_args()

    need_desire = False

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
            if args.start and i < args.start:
                states["multiCharacterModeState"].append(0)
            else:
                states["multiCharacterModeState"].append(2)
    if args.desire:
        need_desire = True
    if args.start:
        states["currentCharacter"] = args.start

    logging.info(states["multiCharacterModeState"])
    logging.info("------------------------------------")

    # Farm in Masyaf
    if needDoFarmingInMasyaf():
        logging.info("领地日常")
        doFarmingInMasyaf()
        update_status_value(config_file_path, 'need_do_farmingInMasyaf', False)
    else:
        logging.info("跳过领地日常")
    logging.info("------------------------------------")

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
                        doBuypotion()
                        update_status_value(config_file_path, 'need_do_weeklyQuest', False)

                    # back to Masyaf
                    pydirectinput.press("f2")
                    sleepTransportLoading()

                    # finish all characters' daily and：
                    # 1.switch to character #1 to desire island
                    # 2.switch to character #0 to terminate
                    states["multiCharacterMode"] = False
                    states["multiCharacterModeState"] = []
                    sleepCommonProcess()
                    if need_desire:
                        logging.info(
                            "[Charac]: <{}>: [Switch]: <{}>".format(
                                states["currentCharacter"], 1
                            )
                        )
                        switchToCharacter(1)
                    else:
                        logging.info(
                            "[Charac]: <{}>: [Switch]: <{}>".format(
                                states["currentCharacter"], 0
                            )
                        )
                        switchToCharacter(0)
                    sleepCommonProcess()

                    # caculate process time
                    endTime = int(time.time_ns() / 1000000)
                    processTime = endTime - startTime
                    processMsc = processTime % 1000
                    processTime = int(processTime / 1000)
                    processSec = processTime % 60
                    processTime = int(processTime / 60)
                    processMin = processTime
                    logging.info("执行时间: " + str(processMin) + "m " + str(processSec) + "s " + str(processMsc) + "ms")
                    logging.info("------------------------------------")
                    logging.info("又是成功偷懒的快乐一天！！！")
                    if sum(states["chaosTimeoutCnt"]):
                        logging.info("Chaos Timeout Cnt: {}".format(states["chaosTimeoutCnt"]))
                        logging.info("Chaos Timeout Cnt Total: " + str(sum(states["chaosTimeoutCnt"].values())))
                    logging.info("------------------------------------")

                elif states["multiCharacterModeState"][states["currentCharacter"]] <= 0:
                    # daily quest
                    if needDoDailyQuest():
                        doGuildDonation()
                        doIvnaDaily()

                    # weekly quest
                    if needDoWeeklyQuest():
                        acceptIvnaWeekly()
                        acceptGuildQuest()
                        doGuildVoyage()
                        doBuypotion()

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
                    logging.info("------------------------------------")
                    continue
                else:
                    sleepClickOrPress()
                    startTime = int(time.time_ns() / 1000000)
                    if states["multiCharacterModeState"][states["currentCharacter"]] == 2:
                        logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[Chaos]: {start}")

            # 生命周期最后：刷渴望岛
            if not states["multiCharacterMode"]:
                if need_desire:
                    desire_island_key_list = [[1698,347],[1475,576],[920,675]]
                    for key in desire_island_key_list:
                        x = key[0]
                        y = key[1]
                        mouseMoveTo(x=x, y=y)
                        sleepClickOrPressLong()
                        pydirectinput.click(x=x, y=y, button="left")
                        sleepClickOrPressLong()
                    utilsDesire.desire()
                    sleepCommonProcess()
                return

        if args.chaos:
            if chaosEnter(states["currentCharacter"]):
                if not chaosCombat(states["currentCharacter"]):
                    if states["currentCharacter"] not in states["chaosTimeoutCnt"]:
                        states["chaosTimeoutCnt"][states["currentCharacter"]] = 1
                    else:
                        states["chaosTimeoutCnt"][states["currentCharacter"]] += 1
        states["multiCharacterModeState"][states["currentCharacter"]] -= 1

        if states["multiCharacterModeState"][states["currentCharacter"]] <= 0:
            if args.repair:
                doRepairMasyaf()
            if args.disenchant:
                doDisenchant()
            if args.buypotion:
                doBuypotion()
            logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[Chaos]: {finish}")


#===========================================================================
# Detail Action functions
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
                        [685,463],[1845,420],[969,762],
                        [685,463],[1593,685],[1779,920],[941,677],
                        [599,534],[1845,420],[969,762],
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
    sleepClickOrPress()
    manor_manage = pyautogui.locateCenterOnScreen(
        "./screenshots/manor-c1.png",
        confidence=0.9
    )
    if manor_manage != None:
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
        region=config["regions"]["whole-game"],
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

    mouseMoveTo(x=682, y=174)
    sleepClickOrPress()
    pydirectinput.click(button="left")
    sleepClickOrPress()

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

    # donoate token
    mouseMoveTo(x=1230, y=605)
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
        region=config["regions"]["whole-game"],
        confidence=0.8,
    )

    if supportResearch != None:
        x, y = supportResearch
        logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[GuildDonation]: {supportResearch}")
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
    acceptQuest_key_list = [[418,192],[1280,378],[1280,456]]
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

    logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[IvnaWeekly]: {acceptFinish}")
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

    mouseMoveTo(x=890, y=193)
    sleepClickOrPress()
    pydirectinput.click(x=890, y=193, button="left")
    sleepCommonProcess()
    guildQuestAvailable = pyautogui.locateCenterOnScreen(
        "./screenshots/accept-guildquest.png",
        confidence=0.7,
        region=(354, 643, 1000, 200),
    )
    if guildQuestAvailable == None:
        #manage guild quest
        sleepClickOrPress()
        pydirectinput.press("esc")
        sleepClickOrPress()
        manageGuildQuest()
        sleepClickOrPress()
        pydirectinput.keyDown("alt")
        sleepClickOrPress()
        pydirectinput.press("j")
        sleepClickOrPress()
        pydirectinput.keyUp("alt")
        sleepCommonProcess()

    # accept quest
    acceptQuest_key_list = [[890,193],[1280,593],[1280,593],[1280,666]]
    for key in acceptQuest_key_list:
        x = key[0]
        y = key[1]
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPressList()
    pydirectinput.press("esc")
    sleepCommonProcess()

    logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[GuildQuest]: {accpetFinish}")
    return


def manageGuildQuest():
    logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[GuildQuest]: {manage}")
    sleepClickOrPress()
    pydirectinput.keyDown("alt")
    sleepClickOrPress()
    pydirectinput.press("u")
    sleepClickOrPress()
    pydirectinput.keyUp("alt")
    sleepCommonProcess()

    manageQuest_key_list = [[994,172],[1612,230],[584,228],[400,289],
                            [1030,356],[916,635],[1030,458],[916,635],[1030,553],[916,635]]
    for key in manageQuest_key_list:
        x = key[0]
        y = key[1]
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPressList()

    pydirectinput.press("esc")
    sleepCommonProcess()
    pydirectinput.press("esc")
    sleepCommonProcess()

    logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[GuildQuest]: {manageFinish}")
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
            esc_exist = pyautogui.locateCenterOnScreen(
                "./screenshots/esc-exist.png",
                confidence=0.7,
                grayscale=True
            )
            if not esc_exist == None:
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

    logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[GuildVoyage]: {finish}")
    return


def needDoWeeklyQuest():
    now = datetime.now()
    now -= timedelta(hours = 6)
    day_of_week_weeklyQuest = now.weekday()

    weekly_quest_status = read_status_value(config_file_path, 'need_do_weeklyQuest')

    if day_of_week_weeklyQuest == 2: # Monday is 0
        if weekly_quest_status:
            return True
        else:
            logging.info("[Error]: weekly quest already done in Wednesday")
            return False
    else:
        update_status_value(config_file_path, 'need_do_weeklyQuest', True)
        return False


def needDoFarmingInMasyaf():
    now = datetime.now()
    now -= timedelta(hours = 6)
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
    now -= timedelta(hours = 6)
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


def doRepairMasyaf():
    try:
        logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[Chaos]: {repair}")
    except:
        logging.info("testcase")

    pydirectinput.press("f2")
    sleepTransportLoading()

    # move to blackmith
    repair_teleport = pyautogui.locateCenterOnScreen(
        "./screenshots/repair-teleport.png",
        confidence=0.7,
    )
    if repair_teleport != None:
        x, y = repair_teleport
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPressLong()
        repair_teleport_farmerland = pyautogui.locateCenterOnScreen(
            "./screenshots/repair-teleport-farmerland.png",
            confidence=0.7,
        )
        if repair_teleport_farmerland != None:
            x, y = repair_teleport_farmerland
            mouseMoveTo(x=x, y=y)
            sleepClickOrPress()
            pydirectinput.click(x=x, y=y, button="left")
            sleepClickOrPressLong()
            repair_teleport_farmerland_confirm = pyautogui.locateCenterOnScreen(
                "./screenshots/repair-teleport-farmerland-confirm.png",
                confidence=0.7,
            )
            if repair_teleport_farmerland_confirm != None:
                x, y = repair_teleport_farmerland_confirm
                mouseMoveTo(x=x, y=y)
                sleepClickOrPress()
                pydirectinput.click(x=x, y=y, button="left")
                sleepCommonProcess()
                mouseMoveTo(x=50, y=520)
                sleepClickOrPress()
                pydirectinput.click(x=50, y=520, button="left")
                sleepCommonProcess()
                mouseMoveTo(x=450, y=521)
                sleepClickOrPress()
                pydirectinput.click(x=450, y=521, button="left")
                sleepCommonProcess()
                mouseMoveTo(x=1146, y=177)
                sleepClickOrPress()
                pydirectinput.click(x=1146, y=177, button="left")
                sleepCommonProcess()

    # repair
    pyautogui.keyDown(config["interact"])
    sleepClickOrPress()
    pyautogui.keyUp(config["interact"])
    sleepClickOrPressLong()
    repair_ui = pyautogui.locateCenterOnScreen(
        "./screenshots/repair-ui-1.png",
        confidence=0.7,
    )
    if repair_ui != None:
        x, y = repair_ui
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPressLong()

    pydirectinput.press("esc")
    sleepClickOrPressLong()

    mouseMoveTo(x=822, y=845)
    sleepClickOrPress()
    pydirectinput.click(x=822, y=845, button="left")
    sleepClickOrPressLong()

    return


def doDisenchant():
    try:
        logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[Chaos]: {bag neaten}")
    except:
        logging.info("testcase")

    # open bag
    sleepClickOrPress()
    pydirectinput.press("i")
    sleepClickOrPressLong()
    bag_sort = pyautogui.locateCenterOnScreen(
        "./screenshots/bag-sort.png",
        confidence=0.7,
        grayscale=True
    )
    if bag_sort == None:
        pydirectinput.press("i")

    # disenchant
    disenchant = pyautogui.locateCenterOnScreen(
        "./screenshots/bag-disenchant.png",
        confidence=0.7,
        grayscale=True
    )
    if disenchant != None:
        x, y = disenchant
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPressLong()

        disenchant_lv1 = pyautogui.locateCenterOnScreen(
            "./screenshots/bag-disenchant-lv1.png",
            confidence=0.7,
            grayscale=True
        )
        if disenchant_lv1 != None:
            x, y = disenchant_lv1
            mouseMoveTo(x=x, y=y)
            sleepClickOrPress()
            pydirectinput.click(x=x, y=y, button="left")
            sleepClickOrPressLong()

        disenchant_lv2 = pyautogui.locateCenterOnScreen(
            "./screenshots/bag-disenchant-lv2.png",
            confidence=0.7,
            grayscale=True
        )
        if disenchant_lv2 != None:
            x, y = disenchant_lv2
            mouseMoveTo(x=x, y=y)
            sleepClickOrPress()
            pydirectinput.click(x=x, y=y, button="left")
            sleepClickOrPressLong()

        disenchant_lv3 = pyautogui.locateCenterOnScreen(
            "./screenshots/bag-disenchant-lv3.png",
            confidence=0.7,
            grayscale=True
        )
        if disenchant_lv3 != None:
            x, y = disenchant_lv3
            mouseMoveTo(x=x, y=y)
            sleepClickOrPress()
            pydirectinput.click(x=x, y=y, button="left")
            sleepClickOrPressLong()

        disenchant_lv4 = pyautogui.locateCenterOnScreen(
            "./screenshots/bag-disenchant-lv4.png",
            confidence=0.7,
            grayscale=True
        )
        if disenchant_lv4 != None:
            x, y = disenchant_lv4
            mouseMoveTo(x=x, y=y)
            sleepClickOrPress()
            pydirectinput.click(x=x, y=y, button="left")
            sleepClickOrPressLong()

        disenchant_pro = pyautogui.locateCenterOnScreen(
            "./screenshots/bag-disenchant-process.png",
            confidence=0.7,
            grayscale=True
        )
        if disenchant_pro != None:
            x, y = disenchant_pro
            mouseMoveTo(x=x, y=y)
            sleepClickOrPress()
            pydirectinput.click(x=x, y=y, button="left")
            sleepClickOrPressLong()

            confirm = pyautogui.locateCenterOnScreen(
                "./screenshots/bag-disenchant-confirm.png",
                confidence=0.7,
                grayscale=True
            )
            if confirm != None:
                x, y = confirm
                mouseMoveTo(x=x, y=y)
                sleepClickOrPress()
                pydirectinput.click(x=x, y=y, button="left")
                sleepClickOrPressLong()
            pydirectinput.press("esc")
            sleepClickOrPressLong()

    # sort bag
    bag_sort = pyautogui.locateCenterOnScreen(
        "./screenshots/bag-sort.png",
        confidence=0.7,
        grayscale=True
    )
    if bag_sort != None:
        x, y = bag_sort
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPressLong()

    # close bag
    pydirectinput.press("i")
    sleepClickOrPressLong()

    # confirm bag closed
    bag_sort = pyautogui.locateCenterOnScreen(
        "./screenshots/bag-sort.png",
        confidence=0.7,
        grayscale=True
    )
    if bag_sort != None:
        pydirectinput.press("i")


def doBuypotion():
    try:
        logging.info("[Charac]: <" + str(states["currentCharacter"]) + ">: " + "[Chaos]: {buy potion}")
    except:
        logging.info("testcase")

    pydirectinput.press("f2")
    sleepTransportLoading()

    # move to blackmith
    repair_teleport = pyautogui.locateCenterOnScreen(
        "./screenshots/repair-teleport.png",
        confidence=0.7,
    )
    if repair_teleport != None:
        x, y = repair_teleport
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPressLong()
        repair_teleport_farmerland = pyautogui.locateCenterOnScreen(
            "./screenshots/repair-teleport-farmerland.png",
            confidence=0.7,
        )
        if repair_teleport_farmerland != None:
            x, y = repair_teleport_farmerland
            mouseMoveTo(x=x, y=y)
            sleepClickOrPress()
            pydirectinput.click(x=x, y=y, button="left")
            sleepClickOrPressLong()
            repair_teleport_farmerland_confirm = pyautogui.locateCenterOnScreen(
                "./screenshots/repair-teleport-farmerland-confirm.png",
                confidence=0.7,
            )
            if repair_teleport_farmerland_confirm != None:
                x, y = repair_teleport_farmerland_confirm
                mouseMoveTo(x=x, y=y)
                sleepClickOrPress()
                pydirectinput.click(x=x, y=y, button="left")
                sleepCommonProcess()

                move_list = [[92,722],[100,662],[693,207],
                            [236,546],[395,481],[245,460]]
                for move in move_list:
                    mouseMoveTo(x=move[0], y=move[1])
                    sleepClickOrPress()
                    pydirectinput.click(x=move[0], y=move[1], button="left")
                    sleepCommonProcess()

                pyautogui.keyDown(config["interact"])
                sleepClickOrPress()
                pyautogui.keyUp(config["interact"])
                sleepClickOrPressLong()

                mouseMoveTo(x=217, y=305)
                sleepClickOrPress()
                pydirectinput.click(x=217, y=305, button="left")
                sleepClickOrPressLong()

                pyautogui.keyDown("shift")
                sleepClickOrPress()
                pydirectinput.click(x=217, y=305, button="right")
                sleepClickOrPress()
                pyautogui.keyUp("shift")

                pyautogui.press("9")
                sleepClickOrPress()
                pyautogui.press("9")
                sleepClickOrPress()

                buypotion_confirm = pyautogui.locateCenterOnScreen(
                    "./screenshots/buypotion-confirm.png",
                    confidence=0.7,
                )
                if buypotion_confirm != None:
                    x, y = buypotion_confirm
                    mouseMoveTo(x=x, y=y)
                    sleepClickOrPress()
                    pydirectinput.click(x=x, y=y, button="left")
                    sleepClickOrPressLong()
                    buypotion_buy = pyautogui.locateCenterOnScreen(
                        "./screenshots/buypotion-buy.png",
                        confidence=0.7,
                    )
                    if buypotion_buy != None:
                        x, y = buypotion_buy
                        mouseMoveTo(x=x, y=y)
                        sleepClickOrPress()
                        pydirectinput.click(x=x, y=y, button="left")
                        sleepClickOrPressLong()

                        pydirectinput.press("esc")
                        sleepClickOrPressLong()


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


if __name__ == "__main__":
    states = newStates.copy()
    main()
