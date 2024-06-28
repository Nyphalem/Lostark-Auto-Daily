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
import sys


def main():
    # 配置logging模块
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    logging.info("------------------------------------")
    logging.info("5秒后开始")
    logging.info("------------------------------------")

    # check tool parameter
    parser = argparse.ArgumentParser(description="脚本可选开关")
    parser.add_argument("--start", type=int, help="从哪个号开始运行")
    args = parser.parse_args()

    start_charac_index = read_status_value(param_file_path, "start_charac_index") - 1
    if start_charac_index < 0:
        start_charac_index = 0
    if args.start:
        start_charac_index = args.start - 1
    need_loop = read_status_value(param_file_path, "need_loop")
    need_chaos = read_status_value(param_file_path, "need_chaos")
    need_chaos_all_class = read_status_value(param_file_path, "need_chaos_all_class")
    need_repair = read_status_value(param_file_path, "need_repair")
    need_sort_bag = read_status_value(param_file_path, "need_sort_bag")
    need_disenchant = read_status_value(param_file_path, "need_disenchant")
    need_buy_potion = read_status_value(param_file_path, "need_buy_potion")
    need_desire = read_status_value(param_file_path, "need_desire")
    need_2K_coor_fix = read_status_value(param_file_path, "need_2K_coor_fix")

    if need_loop:
        states["multiCharacterMode"] = True
        for i in range(len(config["characters"])):
            if start_charac_index and i < start_charac_index:
                states["multiCharacterModeState"].append(0)
            else:
                states["multiCharacterModeState"].append(2)

    states["currentCharacter"] = start_charac_index

    if need_2K_coor_fix:
        mouseMoveTo(x=960, y=20)
        pyautogui.dragRel(0,-20,duration=0.3)
        mouseMoveTo(x=960, y=20)
        pyautogui.dragRel(0,11,duration=0.3)
        mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])

    logging.info(states["multiCharacterModeState"])
    logging.info("------------------------------------")

    # cold init
    sleepCommonProcess()
    mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
    sleepClickOrPress()
    pydirectinput.click(button="right")
    sleepCommonProcess()

    logging.info("返回领地")
    pydirectinput.press("f2")
    sleepTransportLoading()
    logging.info("------------------------------------")

    # Farm in Masyaf
    if needDoFarmingInMasyaf():
        logging.info("领地日常")
        doFarmingInMasyaf()
        update_status_value(config_file_path, 'need_do_farmingInMasyaf', False)
    else:
        logging.info("跳过领地日常")

    # auto daily process
    if needDoDailyQuest() or needDoWeeklyQuest():
        startTime = 0

        logging.info("------------------------------------")
        logging.info("日常任务开始")

        while True:
            logging.info("-----------------C%d-----------------" \
                        % (states["currentCharacter"]+1))
            mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
            sleepClickOrPress()

            # back to Masyaf
            pydirectinput.press("f2")
            sleepTransportLoading()

            # daily quest
            if needDoDailyQuest():
                doGuildDonation()
                doIvnaDaily()

            # weekly quest
            if needDoWeeklyQuest():
                acceptIvnaWeekly()
                acceptGuildQuest()
                doGuildVoyage()

            # back to Masyaf
            pydirectinput.press("f2")
            sleepTransportLoading()


            # switch to the next character
            nextIndex = states["currentCharacter"] + 1
            if nextIndex == len(states["multiCharacterModeState"]):
                nextIndex = 0
            logging.info(
                "[角色]: <{}>: [切换]: <{}>".format(
                    states["currentCharacter"]+1, nextIndex+1
                )
            )
            switchToCharacter(nextIndex)
            if nextIndex == 0:
                break

        update_status_value(config_file_path, 'need_do_dailyQuest', False)
        update_status_value(config_file_path, 'need_do_weeklyQuest', False)
        logging.info("------------------------------------")
        logging.info("日常任务结束")


    # auto chaos process
    if need_chaos:
        startTime = 0

        logging.info("------------------------------------")
        logging.info("混沌地牢开始")
        logging.info("-----------------C%d-----------------" \
                    % (states["currentCharacter"]+1))
        while True:
            if states["status"] == "inCity":
                mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
                sleepClickOrPress()
                # switch character
                if states["multiCharacterMode"]:
                    if sum(states["multiCharacterModeState"]) == 0:
                        # finish all characters' chaos and：
                        # 1.switch to character #1 to desire island
                        # 2.switch to character #0 to terminate
                        states["multiCharacterMode"] = False
                        states["multiCharacterModeState"] = []
                        if need_desire:
                            logging.info(
                                "[角色]: <{}>: [切换]: <{}>".format(
                                    states["currentCharacter"]+1, 2
                                )
                            )
                            switchToCharacter(1)
                        else:
                            logging.info(
                                "[角色]: <{}>: [切换]: <{}>".format(
                                    states["currentCharacter"]+1, 1
                                )
                            )
                            switchToCharacter(0)

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
                        logging.info("混沌地牢结束")
                        if sum(states["chaosTimeoutCnt"]):
                            logging.info("混沌地牢超时计数: {}".format(states["chaosTimeoutCnt"]))
                            logging.info("混沌地牢超时总数: " + str(sum(states["chaosTimeoutCnt"].values())))
                        logging.info("------------------------------------")

                    elif states["multiCharacterModeState"][states["currentCharacter"]] <= 0:
                        # switch to the next character
                        nextIndex = (states["currentCharacter"] + 1) % len(
                            states["multiCharacterModeState"]
                        )
                        logging.info(
                            "[角色]: <{}>: [切换]: <{}>".format(
                                states["currentCharacter"]+1, nextIndex+1
                            )
                        )
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
                        logging.info("-----------------C%d-----------------" % (nextIndex+1))
                        continue
                    else:
                        sleepClickOrPress()
                        if states["multiCharacterModeState"][states["currentCharacter"]] == 2:
                            startTime = int(time.time_ns() / 1000000)
                            doRepairMasyaf()
                            logging.info("[角色]: <" + str(states["currentCharacter"]+1) + ">: " + "[混沌地牢]: {开始}")

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

            if need_chaos:
                if need_chaos_all_class or config["characters"][states["currentCharacter"]]["class"] in classes_stance:
                    if chaosEnter(states["currentCharacter"]):
                        if not chaosCombat(states["currentCharacter"]):
                            if states["currentCharacter"] not in states["chaosTimeoutCnt"]:
                                states["chaosTimeoutCnt"][states["currentCharacter"]] = 1
                            else:
                                states["chaosTimeoutCnt"][states["currentCharacter"]] += 1
            states["multiCharacterModeState"][states["currentCharacter"]] -= 1

            sleepCommonProcess()

            if states["multiCharacterModeState"][states["currentCharacter"]] <= 0:
                if need_repair:
                    doRepairMasyaf()
                if need_disenchant:
                    doDisenchant()
                if need_sort_bag:
                    doSortBag()
                if need_buy_potion:
                    doBuypotion()
                logging.info("[角色]: <" + str(states["currentCharacter"]+1) + ">: " + "[混沌地牢]: {结束}")

                chaos_quest_done = pyautogui.locateCenterOnScreen(
                    "./screenshots/chaos-quest-done.png",
                    region=config["regions"]["whole-game"],
                    confidence=0.9,
                    grayscale=True
                )
                if chaos_quest_done != None:
                    x, y = chaos_quest_done
                    sleepClickOrPress()
                    mouseMoveTo(x=x, y=y)
                    sleepClickOrPress()
                    pydirectinput.click(x=x, y=y, button="left")
                    sleepClickOrPress()
                    chaos_quest_done_confirm = pyautogui.locateCenterOnScreen(
                        "./screenshots/chaos-quest-done-confirm.png",
                        region=config["regions"]["whole-game"],
                        confidence=0.9,
                        grayscale=True
                    )
                    if chaos_quest_done_confirm != None:
                        x, y = chaos_quest_done_confirm
                        sleepClickOrPress()
                        mouseMoveTo(x=x, y=y)
                        sleepClickOrPress()
                        pydirectinput.click(x=x, y=y, button="left")
                        sleepClickOrPress()
                        logging.info("[角色]: <" + str(states["currentCharacter"]+1) + ">: " + "[混沌地牢]: {交任务}")

    logging.info("------------------------------------")
    logging.info("又是成功偷懒的快乐一天！！！")
    logging.info("------------------------------------")

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
                        [678,390],[1593,685],[1845,420],[969,762],
                        [678,390],[1593,685],[1779,920],[941,677],
                        [685,463],[1593,685],[1845,420],[969,762],
                        [685,463],[1593,685],[1779,920],[941,677],
                        [599,534],[1593,685],[1845,420],[969,762],
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
        region=config["regions"]["whole-game"],
        confidence=0.9
    )
    if manor_manage != None:
        pydirectinput.keyDown('esc')
        sleepClickOrPress()
        pydirectinput.keyUp('esc')


def doGuildDonation():
    logging.info("[角色]: <" + str(states["currentCharacter"]+1) + ">: " + "[工会捐赠]: {开始}")
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
        logging.info("[角色]: <" + str(states["currentCharacter"]+1) + ">: " + "[工会捐赠]: {支援研究}")
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
            region=config["regions"]["whole-game"],
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
    logging.info("[角色]: <" + str(states["currentCharacter"]+1) + ">: " + "[工会捐赠]: {结束}")


def doIvnaDaily():
    logging.info("[角色]: <" + str(states["currentCharacter"]+1) + ">: " + "[每日委托]: {开始}")
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
        region=config["regions"]["whole-game"],
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

    logging.info("[角色]: <" + str(states["currentCharacter"]+1) + ">: " + "[每日委托]: {结束}")
    return


def acceptIvnaWeekly():
    logging.info("[角色]: <" + str(states["currentCharacter"]+1) + ">: " + "[每周委托]: {接受}")
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

    logging.info("[角色]: <" + str(states["currentCharacter"]+1) + ">: " + "[每周委托]: {结束}")
    return


def acceptGuildQuest():
    logging.info("[角色]: <" + str(states["currentCharacter"]+1) + ">: " + "[工会委托]: {接受}")
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

    logging.info("[角色]: <" + str(states["currentCharacter"]+1) + ">: " + "[工会委托]: {结束}")
    return


def manageGuildQuest():
    logging.info("[角色]: <" + str(states["currentCharacter"]+1) + ">: " + "[工会委托]: {部署}")
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

    logging.info("[角色]: <" + str(states["currentCharacter"]+1) + ">: " + "[工会委托]: {部署完毕}")
    return


def doGuildVoyage():
    logging.info("[角色]: <" + str(states["currentCharacter"]+1) + ">: " + "[工会航海]: {开始}")

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
        region=config["regions"]["whole-game"],
        confidence=0.7,
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
            region=config["regions"]["whole-game"],
            confidence=0.7,
            grayscale=True
        )
        if ok == None:
            logging.info("[角色]: <" + str(states["currentCharacter"]+1) + ">: " + "[工会航海]: {错误: 修船界面不可用}")
            pydirectinput.press("esc")
            sleepClickOrPressLong()
            pydirectinput.press("esc")
            sleepClickOrPressLong()
            esc_exist = pyautogui.locateCenterOnScreen(
                "./screenshots/esc-exist.png",
                region=config["regions"]["whole-game"],
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
                region=config["regions"]["whole-game"],
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

    logging.info("[角色]: <" + str(states["currentCharacter"]+1) + ">: " + "[工会航海]: {结束}")
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
            logging.info("[错误]: 周三已完成周常，不再做了")
            return False
    else:
        #logging.info("[错误]: 不是周三，不做周常")
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
        logging.info("[角色]: <" + str(states["currentCharacter"]+1) + ">: " + "[混沌地牢]: {修理}")
    except:
        logging.info("testcase")

    pydirectinput.press("f2")
    sleepTransportLoading()

    # move to blackmith
    repair_teleport = pyautogui.locateCenterOnScreen(
        "./screenshots/repair-teleport.png",
        region=config["regions"]["whole-game"],
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
            region=config["regions"]["whole-game"],
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
                region=config["regions"]["whole-game"],
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
        region=config["regions"]["whole-game"],
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
    sleepCommonProcess()

    return


def doSortBag():
    logging.info("[角色]: <" + str(states["currentCharacter"]+1) + ">: " + "[混沌地牢]: {整理背包}")
    # open bag
    sleepClickOrPress()
    pydirectinput.press("i")
    sleepClickOrPressLong()
    bag_sort = pyautogui.locateCenterOnScreen(
        "./screenshots/bag-sort.png",
        region=config["regions"]["whole-game"],
        confidence=0.7,
        grayscale=True
    )
    if bag_sort == None:
        pydirectinput.press("i")

    # sort bag
    bag_sort = pyautogui.locateCenterOnScreen(
        "./screenshots/bag-sort.png",
        region=config["regions"]["whole-game"],
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
    sleepCommonProcess()

    return


def doDisenchant():
    try:
        logging.info("[角色]: <" + str(states["currentCharacter"]+1) + ">: " + "[混沌地牢]: {一键分解}")
    except:
        logging.info("testcase")

    # open bag
    sleepClickOrPress()
    pydirectinput.press("i")
    sleepClickOrPressLong()
    bag_sort = pyautogui.locateCenterOnScreen(
        "./screenshots/bag-sort.png",
        region=config["regions"]["whole-game"],
        confidence=0.7,
        grayscale=True
    )
    if bag_sort == None:
        pydirectinput.press("i")

    # disenchant
    disenchant = pyautogui.locateCenterOnScreen(
        "./screenshots/bag-disenchant.png",
        region=config["regions"]["whole-game"],
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
            region=config["regions"]["whole-game"],
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
            region=config["regions"]["whole-game"],
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
            region=config["regions"]["whole-game"],
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
            region=config["regions"]["whole-game"],
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
            region=config["regions"]["whole-game"],
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
                region=config["regions"]["whole-game"],
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
            sleepCommonProcess()

    # close bag
    pydirectinput.press("i")
    sleepCommonProcess()

    return


def doBuypotion():
    try:
        logging.info("[角色]: <" + str(states["currentCharacter"]+1) + ">: " + "[混沌地牢]: {购买药水}")
    except:
        logging.info("testcase")

    pydirectinput.press("f2")
    sleepTransportLoading()

    # move to blackmith
    repair_teleport = pyautogui.locateCenterOnScreen(
        "./screenshots/repair-teleport.png",
        region=config["regions"]["whole-game"],
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
            region=config["regions"]["whole-game"],
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
                region=config["regions"]["whole-game"],
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
                    region=config["regions"]["whole-game"],
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
                        region=config["regions"]["whole-game"],
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
    pydirectinput.press("esc")
    sleepCommonProcess()

    while (1):
        switch = pyautogui.locateCenterOnScreen(
            "./screenshots/switch-charac-ui.png",
            region=config["regions"]["whole-game"],
            confidence=0.7,
        )
        if switch == None:
            pydirectinput.press("esc")
            sleepClickOrPressLong()
        else:
            break

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

    main()
