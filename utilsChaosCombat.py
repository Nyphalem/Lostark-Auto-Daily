import pyautogui
import time
import random
from utils import *
import argparse
from personalCharacters import *
from originConfigAbilities import *
import math
import copy


key_list_common = ['q', 'r', 'w', 'e', 'a', 's', 'd', 'f']
key_list_common_ult = ['q', 'r', 'w', 'e', 'a', 's', 'd', 'f', 'v']

key_list_demonic = ['q', 'r', 'w', 'e', 'a', 's', 'd', 'f']
key_list_demonic_z = ['q', 'r', 'w', 'e', 'a', 's']
key_list_demonic_z_reverse = ['s', 'a', 'e', 'w', 'r', 'q']

key_list_process_cache = list()

# global constant
abilityScreenshots = []
levelStarttime = {}
characterIndex = 0
layer = -1
log_verbose = False


def logv(str):
    global log_verbose
    if log_verbose:
        logging.info(str)


def saveAbilitiesScreenshots(characterClass):
    if characterClass in abilities:
        for ability in abilities[characterClass]:
            left = ability["position"]["left"]
            top = ability["position"]["top"]
            width = ability["position"]["width"]
            height = ability["position"]["height"]
            im = pyautogui.screenshot(region=(left, top, width, height))
            abilityScreenshots.append(
                {
                    "key": ability["key"],
                    "image": im,
                    "cast": ability["cast"],
                    "castTime": ability["castTime"],
                    "hold": ability["hold"],
                    "holdTime": ability["holdTime"],
                    "doubleClick": ability["doubleClick"],
                    "directional": ability["directional"],
                    "position": ability["position"],
                }
            )
            sleepWink()


def usbAbilitiesCommon(key_list):
    global key_list_process_cache

    logv("[ChaosDebug]: -> usbAbilitiesCommon()")

    avail_ability = True

    pyautogui.mouseDown(button="right")

    if len(key_list_process_cache) == 0:
        key_list_process_cache = copy.copy(key_list)
    click_random = random.choice(key_list_process_cache)
    key_list_process_cache.remove(click_random)

    for ability in abilityScreenshots:
        if click_random == ability["key"]:
            left = ability["position"]["left"]
            top = ability["position"]["top"]
            width = ability["position"]["width"]
            height = ability["position"]["height"]
            ability_ready = pyautogui.locateCenterOnScreen(
                ability["image"],
                confidence=0.9,
                region=(left, top, width, height),
            )
            if ability_ready == None:
                pydirectinput.mouseUp(button="right")
                logv("[ChaosDebug]: <- usbAbilitiesCommon() in cooldown")
                avail_ability = False

    pyautogui.mouseUp(button="right")

    logv("[ChaosDebug]: -> usbAbilitiesCommon() choose ability")

    pyautogui.keyDown(click_random)
    for ability in abilityScreenshots:
        if click_random == ability["key"]:
            if ability["cast"] == True:
                logv("[ChaosDebug]: -> usbAbilitiesCommon() use cast")
                time.sleep(random.uniform(ability["castTime"], ability["castTime"] + 0.3))
                pyautogui.keyUp(click_random)
            elif ability["hold"] == True and ability["holdTime"] != None:
                logv("[ChaosDebug]: -> usbAbilitiesCommon() use hold")
                time.sleep(random.uniform(ability["holdTime"], ability["holdTime"] + 0.3))
                pyautogui.keyUp(click_random)
            elif ability["doubleClick"] == True:
                logv("[ChaosDebug]: -> usbAbilitiesCommon() use doubleclick")
                for i in range(5):
                    pyautogui.keyUp(click_random)
                    pyautogui.keyDown(click_random)
                pyautogui.keyUp(click_random)
            else:
                logv("[ChaosDebug]: -> usbAbilitiesCommon() use normal")
                pyautogui.keyUp(click_random)

    logv("[ChaosDebug]: <- usbAbilitiesCommon()")

    return avail_ability


def useAbilities(key_list, characterClass):
    logv("[ChaosDebug]: -> useAbilities()")

    avail_ability = False

    if characterClass == "bard":
        pydirectinput.press("x")
        if usbAbilitiesCommon(key_list):
            avail_ability = True
    if characterClass == "holyknight":
        # TODO: check for enable z
        if False:
            pyautogui.keyDown("z")
            sleepClickOrPress()
            pyautogui.keyUp("z")
        if usbAbilitiesCommon(key_list):
            avail_ability = True
    if characterClass == "demonic":
        z_full = pyautogui.locateCenterOnScreen(
            ".\screenshots\chaos-class\demonic\z-full.png",
            confidence=0.8,
            region = (869, 981, 286, 130)
        )
        z_active = pyautogui.locateCenterOnScreen(
            ".\screenshots\chaos-class\demonic\z-active.png",
            confidence=0.8,\
            region = (869, 981, 286, 130)
        )
        if z_full != None:
            pyautogui.keyDown("z")
            sleepClickOrPressLong()
            pyautogui.keyUp("z")
            avail_ability = True
        elif z_active != None:
            for ability in key_list_demonic_z:
                pyautogui.press(ability)
            for ability in key_list_demonic_z_reverse:
                pyautogui.press(ability)
            avail_ability = True
        else:
            if usbAbilitiesCommon(key_list_demonic):
                avail_ability = True
    if characterClass == "slayer":
        pydirectinput.press("z")
        if usbAbilitiesCommon(key_list):
            avail_ability = True
    if characterClass == "sorceress":
        if usbAbilitiesCommon(key_list):
            avail_ability = True
    if characterClass == "aeromancer":
        z_full = pyautogui.locateCenterOnScreen(
            ".\\screenshots\\chaos-class\\aeromancer\\z-full.png",
            confidence=0.9,
            region = (800, 800, 350, 350)
        )
        if z_full != None:
            pyautogui.keyDown("z")
            sleepClickOrPressLong()
            pyautogui.keyUp("z")
            avail_ability = True
        else:
            if usbAbilitiesCommon(key_list):
                avail_ability = True
    if characterClass == "blade":
        # TODO: tuning
        if usbAbilitiesCommon(key_list):
            avail_ability = True

    logv("[ChaosDebug]: <- useAbilities()")

    return avail_ability


def checkBlackScreen():
    x1, y1 = (131, 1103)
    x2, y2 = (195, 1103)
    r1, g1, b1 = pyautogui.pixel(x1, y1)
    r2, g2, b2 = pyautogui.pixel(x2, y2)
    if r1 + g1 + b1 < 60 and r2 + g2 + b2 < 60:
        logv("[ChaosDebug]: -> BLACK")
        mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
        return True

    return False


def checkHealth():
    if config["healthPotUse"] == False:
        return
    if not checkBlackScreen():
        x = int(
            config["healthCheckX"]
            + (857 - config["healthCheckX"]) * config["healthPotAtPercent"]
        )
        y = config["healthCheckY"]
        r1, g, b = pyautogui.pixel(x, y)
        r2, g, b = pyautogui.pixel(x - 2, y)
        r3, g, b = pyautogui.pixel(x + 2, y)
        if r1 < 30 or r2 < 30 or r3 < 30:
            logv("[ChaosDebug]: -> HEALTH")
            pydirectinput.press(config["healthPot"])

    return


def checkDeath():
    revive = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-revive.png",
        region=config["regions"]["whole-game"],
        confidence=0.6
    )
    if revive != None:
        logv("[ChaosDebug]: -> DEATH")
        x, y = revive
        sleepClickOrPress()
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPress()
        mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])

    return


def checkPortal():
    logv("[ChaosDebug]: -> checkPortal()")

    x = -1
    y = -1

    portal_pic = [
        "./screenshots/chaos-portal.png",
        "./screenshots/chaos-portal-top.png",
        "./screenshots/chaos-portal-bottom.png",
        "./screenshots/chaos-portal-left.png",
        "./screenshots/chaos-portal-right.png"
    ]

    for i in range(len(portal_pic)):
        p_temp = pyautogui.locateCenterOnScreen(
            portal_pic[i],
            region=config["regions"]["minimap"],
            confidence=0.6
        )
        if p_temp != None:
            logv("[ChaosDebug]: -> PORTAL")
            x_m, y_m = p_temp
            if i == 1:
                y_m += 4
            if i == 2:
                y_m -= 4
            if i == 3:
                x_m += 2
            if i == 4:
                x_m -= 2
            x, y = calculateMinimapRelative(x_m, y_m)

    logv("[ChaosDebug]: <- checkPortal()")

    return x, y


def checkAsh():
    ash = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-ash.png",
        region=config["regions"]["whole-game"],
        confidence=0.7
    )
    if ash != None:
        logv("[ChaosDebug]: -> ASH")
        x, y = ash
        mouseMoveTo(x=x, y=y)
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPress()
        pydirectinput.press(config["interact"])
        mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
        logv("[ChaosDebug]: -> ASH TOUCHED!!!")

    return


def checkBossToAwk():
    bossBar = pyautogui.locateOnScreen(
        "./screenshots/chaos-bossBar.png",
        region=config["regions"]["whole-game"],
        confidence=0.7
    )
    if bossBar != None:
        pyautogui.press(config["awakening"])
        return True

    return False


def checkBoss():
    boss = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-boss.png",
        region=config["regions"]["minimap"],
        confidence=0.6
    )
    if boss != None:
        logv("[ChaosDebug]: -> BOSS")
        x, y = boss
        realX, realY = calculateMinimapRelative(x, y)
        pydirectinput.click(x=realX, y=realY, button="left")
        sleepClickOrPress()
        logv("[ChaosDebug]: -> BOSS MOVED!!!")

    return


def checkChaosFinish():
    chaosFinish = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-finish.png",
        region=config["regions"]["whole-game"],
        confidence=0.7
    )
    if chaosFinish != None:
        x, y = chaosFinish
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPressLong()
        chaosExit1 = pyautogui.locateCenterOnScreen(
            "./screenshots/chaos-exit1.png",
            region=config["regions"]["whole-game"],
            confidence=0.7
        )
        if chaosExit1 != None:
            x, y = chaosExit1
            mouseMoveTo(x=x, y=y)
            sleepClickOrPress()
            pydirectinput.click(x=x, y=y, button="left")
            sleepClickOrPressLong()
            chaosExit2 = pyautogui.locateCenterOnScreen(
                "./screenshots/chaos-exit2.png",
                region=config["regions"]["whole-game"],
                confidence=0.7
            )
            if chaosExit2 != None:
                x, y = chaosExit2
                mouseMoveTo(x=x, y=y)
                sleepClickOrPressLong()
                pydirectinput.click(x=x, y=y, button="left")
                return True

    return False


def checkTimeout(layer):
    logv("[ChaosDebug]: -> checkTimeout()")

    timeout = None

    if layer in levelStarttime:
        starttime = levelStarttime[layer]
        currenttime = int(time.time_ns() / 1000000)
        if (currenttime - starttime) > (5 * (60+1) * 1000):
            chaosExit1 = pyautogui.locateCenterOnScreen(
                "./screenshots/chaos-exit1.png",
                region=config["regions"]["whole-game"],
                confidence=0.7
            )
            if chaosExit1 != None:
                x, y = chaosExit1
                mouseMoveTo(x=x, y=y)
                sleepClickOrPress()
                pydirectinput.click(x=x, y=y, button="left")
                sleepClickOrPressLong()
                chaosExit2 = pyautogui.locateCenterOnScreen(
                    "./screenshots/chaos-exit2.png",
                    region=config["regions"]["whole-game"],
                    confidence=0.7
                )
                if chaosExit2 != None:
                    x, y = chaosExit2
                    mouseMoveTo(x=x, y=y)
                    sleepClickOrPressLong()
                    pydirectinput.click(x=x, y=y, button="left")
                    logv("[ChaosDebug]: -> TIMEOUT")
                    timeout = "TIMEOUT"

    logv("[ChaosDebug]: <- checkTimeout()")

    return timeout


def checkLongL2():
    starttime = levelStarttime[2]
    currenttime = int(time.time_ns() / 1000000)
    if (currenttime - starttime) > (3 * 60 * 1000):
        return True

    return False


def checkTower():
    logv("[ChaosDebug]: -> checkTower()")

    x_m = -1
    y_m = -1

    tower_pic = [
        "./screenshots/chaos-tower.png",
        "./screenshots/chaos-tower-top.png",
        "./screenshots/chaos-tower-bottom.png",
        "./screenshots/chaos-tower-left.png",
        "./screenshots/chaos-tower-right.png"
    ]

    for i in range(len(tower_pic)):
        t_temp = pyautogui.locateCenterOnScreen(
            tower_pic[i],
            region=config["regions"]["minimap"],
            confidence=0.7
        )
        if t_temp != None:
            logv("[ChaosDebug]: -> TOWER")
            x_m, y_m = t_temp
            if i == 0:
                y_m += 2
            if i == 1:
                y_m += 7
            if i == 3:
                x_m += 2
                y_m += 2
            if i == 4:
                x_m -= 2
                y_m += 2
            break

    logv("[ChaosDebug]: <- checkTower()")

    return x_m, y_m


def calculateMinimapRelative(x, y, tiny=False):
    selfLeft = config["minimapCenterX"]
    selfTop = config["minimapCenterY"]

    x = x - selfLeft
    y = y - selfTop

    if not tiny:
        dist = 300
    else:
        dist = 20
    if y < 0:
        dist = -dist
    if x == 0:
        if y < 0:
            newY = y - abs(dist)
        else:
            newY = y + abs(dist)
        r_x = 0 + config["screenCenterX"]
        r_y = int(newY) + config["screenCenterY"]
        return r_x, r_y
    if y == 0:
        if x < 0:
            newX = x - abs(dist)
        else:
            newX = x + abs(dist)
        r_x = int(newX) + config["screenCenterX"]
        r_y = 0 + config["screenCenterY"]
        return r_x, r_y

    k = y / x
    newY = y + dist
    newX = newY / k

    radius = math.sqrt(newX**2 + newY**2)
    if radius > config["clickableArea"]:
        newY = newY * config["clickableArea"] / radius
        newX = newX * config["clickableArea"] / radius

    r_x = int(newX) + config["screenCenterX"]
    r_y = int(newY) + config["screenCenterY"]

    return r_x, r_y


def clickTower():
    logv("[ChaosDebug]: -> clickTower()")

    riftCore1 = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-riftcore1.png",
        confidence=0.6,
        region=config["regions"]["whole-game"],
    )
    if riftCore1 != None:
        x, y = riftCore1
        if y > 650 or x < 400 or x > 1500:
            return
        click_x = x
        click_y = y + 190
        pydirectinput.click(
            x=click_x, y=click_y, button=config["move"]
        )
        logv("[ChaosDebug]: -> clickTower() riftCore1")
        pydirectinput.press(config["meleeAttack"])
        sleepClickOrPress()
        pydirectinput.press(config["meleeAttack"])
        sleepClickOrPress()
        pydirectinput.press(config["meleeAttack"])
        sleepClickOrPress()
        pydirectinput.press(config["meleeAttack"])
        mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
    else:
        riftCore2 = pyautogui.locateCenterOnScreen(
            "./screenshots/chaos-riftcore2.png",
            confidence=0.6,
            region=config["regions"]["whole-game"],
        )
        if riftCore2 != None:
            x, y = riftCore2
            if y > 650 or x < 400 or x > 1500:
                return
            click_x = x
            click_y = y + 190
            pydirectinput.click(
                x=click_x, y=click_y, button=config["move"]
            )
            logv("[ChaosDebug]: -> clickTower() riftCore2")
            pydirectinput.press(config["meleeAttack"])
            sleepClickOrPress()
            pydirectinput.press(config["meleeAttack"])
            sleepClickOrPress()
            pydirectinput.press(config["meleeAttack"])
            sleepClickOrPress()
            pydirectinput.press(config["meleeAttack"])
            mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])

    logv("[ChaosDebug]: <- clickTower()")

    return


def checkMob(move=True):
    mob = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-mob.png",
        confidence=0.8,
        region=config["regions"]["minimap"],
    )
    if mob != None:
        logv("[ChaosDebug]: -> MOB")
        x, y = mob
        if not move:
            realX, realY = calculateMinimapRelative(x, y, True)
            mouseMoveTo(x=realX, y=realY)
            logv("[ChaosDebug]: -> MOB DIRECTED!!!")
        else:
            realX, realY = calculateMinimapRelative(x, y)
            pydirectinput.click(x=realX, y=realY, button="left")
            sleepClickOrPress()
            mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
            logv("[ChaosDebug]: -> MOB MOVED!!!")
        return True

    return False


def randomMove():
    x = random.randint(
        config["screenCenterX"] - config["clickableAreaX"],
        config["screenCenterX"] + config["clickableAreaX"],
    )
    y = random.randint(
        config["screenCenterY"] - config["clickableAreaY"],
        config["screenCenterY"] + config["clickableAreaY"],
    )

    pydirectinput.click(x=x, y=y, button=config["move"])
    sleepClickOrPress()
    mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
    logv("[ChaosDebug]: -> RAMDOM MOVED!!!")

    return


def randomMouseMove():
    logv("[ChaosDebug]: -> randomMouseMove()")
    mouse_random_x = random.randint(-40, 20)
    mouse_random_y = random.randint(-40, 20)

    x = config["screenCenterX"] + mouse_random_x
    y = config["screenCenterY"] + mouse_random_y

    mouseMoveTo(x=x, y=y)

    return


def combatInFloor1():
    global characterIndex

    logging.info("[Charac]: <" + str(characterIndex) + ">: " + "[Chaos]: {Layer 1}")

    levelStarttime[1] = int(time.time_ns() / 1000000)

    while (1):
        skipAblities = False

        checkHealth()
        checkDeath()

        if not characters[characterIndex]["class"] in classes_stance:
            x, y = checkPortal()
            if x != -1 and y != -1:
                pydirectinput.click(x=x, y=y, button="left")
                pydirectinput.press(config["interact"])
                sleepWink()
                if checkBlackScreen():
                    return
                skipAblities = True
        else:
            pydirectinput.press(config["interact"])
            sleepWink()
            if checkBlackScreen():
                return

        if not skipAblities:
            if not characters[characterIndex]["class"] in classes_stance:
                if not checkMob(False):
                    randomMouseMove()
                    if checkBlackScreen():
                        return

            useAbilities(key_list_common, characters[characterIndex]["class"])

        pydirectinput.press(config["interact"])
        sleepWink()
        if checkBlackScreen():
            return

        if checkTimeout(1) == "TIMEOUT":
            sleepTransportLoading()
            return "TIMEOUT"


def combatInFloor2():
    global characterIndex

    logging.info("[Charac]: <" + str(characterIndex) + ">: " + "[Chaos]: {Layer 2}")

    prepareUltCnt = 0
    bossMode = False

    levelStarttime[2] = int(time.time_ns() / 1000000)
    while (1):
        prepareUltCnt += 1
        if prepareUltCnt == 10:
            break

        checkHealth()
        checkDeath()
        checkAsh()

        if not characters[characterIndex]["class"] in classes_stance:
            if not checkMob(False):
                randomMouseMove()

        useAbilities(key_list_common, characters[characterIndex]["class"])

    pydirectinput.press(config["awakening"])

    while (1):
        prepareUltCnt += 1

        skipAblities = False

        checkHealth()
        checkDeath()

        if characters[characterIndex]["class"] not in classes_stance \
            or checkLongL2():
            checkBoss()
            x, y = checkPortal()
            if x != -1 and y != -1:
                pydirectinput.click(x=x, y=y, button="left")
                pydirectinput.press(config["interact"])
                sleepWink()
                if checkBlackScreen():
                    return
                skipAblities = True
        else:
            pydirectinput.press(config["interact"])
            sleepWink()
            if checkBlackScreen():
                return

        if checkBossToAwk():
            bossMode = True

        if not skipAblities:
            if not characters[characterIndex]["class"] in classes_stance:
                if bossMode or not checkMob(False):
                    randomMouseMove()

            useAbilities(key_list_common, characters[characterIndex]["class"])

        pydirectinput.press(config["interact"])
        sleepWink()
        if checkBlackScreen():
            return

        if prepareUltCnt >= 30 and checkTimeout(2) == "TIMEOUT":
            sleepTransportLoading()
            return "TIMEOUT"


def combatInFloor3():
    global characterIndex

    logging.info("[Charac]: <" + str(characterIndex) + ">: " + "[Chaos]: {Layer 3}")

    prepareTimeoutCnt = 0
    moveCnt = 0
    findTowerCnt = 0
    breakTowerCnt = 0

    levelStarttime[3] = int(time.time_ns() / 1000000)

    while (1):
        prepareTimeoutCnt += 1

        skipAblities = False

        checkHealth()
        checkDeath()
        checkAsh()

        # Tower
        x, y = checkTower()
        if x != -1 and y != -1:
            findTowerCnt += 1
            realX, realY = calculateMinimapRelative(x, y)
            sleepClickOrPress()
            pydirectinput.click(x=realX, y=realY, button="left")
            sleepClickOrPressLong()
            breakTowerCnt = 5

            clickTower()

            mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])

            if findTowerCnt == 3:
                randomMove()
                findTowerCnt = 0
            skipAblities = True

        if breakTowerCnt > 0:
            breakTowerCnt -= 1

        if not skipAblities:
            if breakTowerCnt <= 0:
                if not checkMob():
                    moveCnt += 1
                    if moveCnt == 5:
                        randomMove()
                        moveCnt = 0
            useAbilities(key_list_common_ult, characters[characterIndex]["class"])


        if checkChaosFinish():
            sleepTransportLoading()
            return

        if prepareTimeoutCnt >= 30 and checkTimeout(3) == "TIMEOUT":
            sleepTransportLoading()
            return "TIMEOUT"


def chaosCombat(index):
    global characterIndex

    characterIndex = index

    mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
    pydirectinput.click(button="right")

    sleepClickOrPress()

    saveAbilitiesScreenshots(characters[characterIndex]["class"])

    if combatInFloor1() == "TIMEOUT":
        logging.info("[Charac]: <" + str(characterIndex) + ">: " + "[Chaos]: {TIMEOUT!!!}")
        return False
    if combatInFloor2() == "TIMEOUT":
        logging.info("[Charac]: <" + str(characterIndex) + ">: " + "[Chaos]: {TIMEOUT!!!}")
        return False
    if combatInFloor3() == "TIMEOUT":
        logging.info("[Charac]: <" + str(characterIndex) + ">: " + "[Chaos]: {TIMEOUT!!!}")
        return False

    logging.info("[Charac]: <" + str(characterIndex) + ">: " + "[Chaos]: {Exit}")

    return True


def stub():
    global characterIndex
    global layer

    mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
    pydirectinput.click(button="right")

    sleepClickOrPress()

    saveAbilitiesScreenshots(characters[characterIndex]["class"])

    if layer != 2 and layer != 3:
        if combatInFloor1() == "TIMEOUT":
            return
    if layer != 3:
        if combatInFloor2() == "TIMEOUT":
            return
    combatInFloor3()

    return


def main():
    global characterIndex
    global layer
    global log_verbose
    parser = argparse.ArgumentParser(description="Optional app description")
    parser.add_argument("--ci", type=int, help="character index")
    parser.add_argument("--l", type=int, help="layer index")
    parser.add_argument("--v", action="store_true", help="verbos log")
    args = parser.parse_args()
    if args.ci:
        characterIndex = args.ci
    if args.l:
        layer = args.l
    if args.v:
        log_verbose = True

    stub()


if __name__ == '__main__':
    main()

