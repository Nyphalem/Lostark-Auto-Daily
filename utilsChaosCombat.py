import pyautogui
import time
import random
from utils import *
import argparse
from personalCharacters import *
from originConfigAbilities import *
import math


key_list_common = ['q', 'r', 'w', 'e', 'a', 's', 'd', 'f']
key_list_common_ult = ['q', 'r', 'w', 'e', 'a', 's', 'd', 'f', 'v']

key_list_demonic = ['q', 'r', 'w', 'e', 'a', 's', 'd', 'f']
key_list_demonic_z = ['q', 'r', 'w', 'e', 'a', 's']
key_list_demonic_z_reverse = ['s', 'a', 'e', 'w', 'r', 'q']


# global constant
abilityScreenshots = []
characterIndex = 0
layer = -1


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
            sleepClickOrPress()


def usbAbilitiesCommon(key_list, characterClass):
    pyautogui.keyDown(config["interact"])
    sleepClickOrPress()
    pyautogui.keyUp(config["interact"])

    pydirectinput.mouseDown(button="right")

    size = len(key_list)
    click_random = random.randint(0, size-1)
    for ability in abilityScreenshots:
        if key_list[click_random] == ability["key"]:
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
                return False

    pydirectinput.mouseUp(button="right")

    pyautogui.keyDown(key_list[click_random])

    for ability in abilityScreenshots:
        if key_list[click_random] == ability["key"]:
            if ability["cast"] == True:
                time.sleep(random.uniform(ability["castTime"], ability["castTime"] + 0.5))
                pyautogui.keyUp(key_list[click_random])
            elif ability["hold"] == True and ability["holdTime"] != None:
                time.sleep(random.uniform(ability["holdTime"], ability["holdTime"] + 0.5))
                pyautogui.keyUp(key_list[click_random])
            elif ability["doubleClick"] == True:
                for i in range(10):
                    sleepWink()
                    pyautogui.keyUp(key_list[click_random])
                    pyautogui.keyDown(key_list[click_random])
                sleepClickOrPress()
            else:
                sleepWink()
                pyautogui.keyUp(key_list[click_random])
                sleepClickOrPress()

    return True


def useAbilities(key_list, characterClass):
    if characterClass == "bard":
        pyautogui.keyDown("x")
        sleepWink()
        pyautogui.keyUp("x")
        sleepClickOrPress()
        if usbAbilitiesCommon(key_list, characterClass):
            return True
    if characterClass == "holyknight":
        # TODO: check for enable z
        if False:
            pyautogui.keyDown("z")
            sleepClickOrPress()
            pyautogui.keyUp("z")
        if usbAbilitiesCommon(key_list, characterClass):
            return True
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
        z_fade = pyautogui.locateCenterOnScreen(
            ".\screenshots\chaos-class\demonic\z-fade.png",
            confidence=0.8,
            region = (869, 981, 286, 130)
        )
        if z_full != None:
            pyautogui.keyDown("z")
            sleepWink()
            pyautogui.keyUp("z")
            sleepClickOrPress()
            return True
        if z_active != None:
            for ability in key_list_demonic_z:
                pyautogui.press(ability)
            pyautogui.keyDown(config["interact"])
            sleepClickOrPress()
            pyautogui.keyUp(config["interact"])
            for ability in key_list_demonic_z_reverse:
                pyautogui.press(ability)
            pyautogui.keyDown(config["interact"])
            sleepClickOrPress()
            pyautogui.keyUp(config["interact"])
            return True
        if z_fade != None:
            usbAbilitiesCommon(key_list_demonic, characterClass)
            return True
    if characterClass == "slayer":
        pyautogui.keyDown("z")
        sleepWink()
        pyautogui.keyUp("z")
        sleepClickOrPress()
        if usbAbilitiesCommon(key_list, characterClass):
            return True
    if characterClass == "sorceress":
        if usbAbilitiesCommon(key_list, characterClass):
            return True
    if characterClass == "aeromancer":
        # TODO: tuning
        if usbAbilitiesCommon(key_list, characterClass):
            return True
    if characterClass == "blade":
        # TODO: tuning
        if usbAbilitiesCommon(key_list, characterClass):
            return True
    return False


def checkBlackScreen():
    x1, y1 = (131, 1103)
    x2, y2 = (195, 1103)
    r1, g1, b1 = pyautogui.pixel(x1, y1)
    r2, g2, b2 = pyautogui.pixel(x2, y2)
    if r1 + g1 + b1 < 60 and r2 + g2 + b2 < 60:
        logging.info("[Chaos]: [black    ]")
        mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
        return True


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
            logging.info("[Chaos]: [health   ]")
            pydirectinput.press(config["healthPot"])
    return


def checkDeath():
    revive = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-revive.png",
        region=config["regions"]["whole-game"],
        confidence=0.6
    )
    if revive != None:
        logging.info("[Chaos]: [death    ]")
        x, y = revive
        sleepClickOrPress()
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPressLong()
        mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])


def checkPortal():
    portal = {}

    p_temp = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-portal.png",
        region=config["regions"]["minimap"],
        confidence=0.6
    )
    if p_temp != None:
        portal["0"] = p_temp

    p_temp = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-portal-top.png",
        region=config["regions"]["minimap"],
        confidence=0.6
    )
    if p_temp != None:
        portal["top"] = p_temp

    p_temp = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-portal-bottom.png",
        region=config["regions"]["minimap"],
        confidence=0.6
    )
    if p_temp != None:
        portal["bot"] = p_temp

    p_temp = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-portal-left.png",
        region=config["regions"]["minimap"],
        confidence=0.6
    )
    if p_temp != None:
        portal["left"] = p_temp

    p_temp = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-portal-right.png",
        region=config["regions"]["minimap"],
        confidence=0.6
    )
    if p_temp != None:
        portal["right"] = p_temp

    for key in portal:
        if portal[key] != None:
            logging.info("[Chaos]: [portal   ]")
            x_m, y_m = portal[key]
            if key == "top":
                y_m += 8
            if key == "bot":
                y_m -= 8
            if key == "left":
                x_m += 4
            if key == "right":
                x_m -= 4
            x, y = calculateMinimapRelative(x_m, y_m)
            sleepClickOrPress()
            mouseMoveTo(x=x, y=y)
            sleepClickOrPress()
            pydirectinput.click(x=x, y=y, button="left")
            sleepClickOrPressLong()
            mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
            return True

    return False


def checkAsh():
    ash = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-ash.png",
        region=config["regions"]["whole-game"],
        confidence=0.75
    )
    if ash != None:
        x, y = ash
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPressLong()
        pydirectinput.press(config["interact"])
        sleepClickOrPressLong()
    else:
        return


def checkBossToV():
    bossBar = pyautogui.locateOnScreen(
        "./screenshots/chaos-bossBar.png",
        region=config["regions"]["whole-game"],
        confidence=0.7
    )
    if bossBar != None:
        pyautogui.press(config["awakening"])


def checkBoss():
    boss = pyautogui.locateOnScreen(
        "./screenshots/chaos-boss.png",
        region=config["regions"]["minimap"],
        confidence=0.7
    )
    if boss != None:
        logging.info("[Chaos]: [Boss     ]")
        x, y = boss
        realX, realY = calculateMinimapRelative(x, y)
        sleepClickOrPress()
        pydirectinput.click(x=realX, y=realY, button="left")
        sleepClickOrPressLong()
        mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])


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


def checkTimeout():
    timeout = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-timeout.png",
        region=config["regions"]["chaos-remain-time"],
        confidence=0.9
    )
    if timeout != None:
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
                logging.info("[Chaos]: [timeout  ]")
                return "TIMEOUT"
    return None


def checkTower():
    tower = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-tower.png",
        region=config["regions"]["minimap"],
        confidence=0.7
    )
    towerTop = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-towerTop.png",
        region=config["regions"]["minimap"],
        confidence=0.7,
    )
    towerBot = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-towerBot.png",
        region=config["regions"]["minimap"],
        confidence=0.7,
    )
    if tower != None:
        x, y = tower
        logging.info("[Chaos]: [tower    ]: " + "image x: {} y: {}".format(x, y))
        return x, y+2
    elif towerTop != None:
        x, y = towerTop
        logging.info("[Chaos]: [tower    ]: " + "TOP image x: {} y: {}".format(x, y))
        return x, y+7
    elif towerBot != None:
        x, y = towerBot
        logging.info("[Chaos]: [tower    ]: " + "BOT image x: {} y: {}".format(x, y))
        return x, y
    return -1, -1


def calculateMinimapRelative(x, y):
    selfLeft = config["minimapCenterX"]
    selfTop = config["minimapCenterY"]

    x = x - selfLeft
    y = y - selfTop

    dist = 400
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
    riftCore1 = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-riftcore1.png",
        confidence=0.6,
        region=config["regions"]["whole-game"],
    )
    riftCore2 = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-riftcore2.png",
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
        logging.info("[Chaos]: [tower    ]: break tower")
        pydirectinput.press(config["meleeAttack"])
        sleepClickOrPress()
        pydirectinput.press(config["meleeAttack"])
        sleepClickOrPress()
        pydirectinput.press(config["meleeAttack"])
        sleepClickOrPress()
        pydirectinput.press(config["meleeAttack"])
        mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
        return True
    elif riftCore2 != None:
        x, y = riftCore2
        if y > 650 or x < 400 or x > 1500:
            return
        click_x = x
        click_y = y + 190
        pydirectinput.click(
            x=click_x, y=click_y, button=config["move"]
        )
        logging.info("[Chaos]: [tower    ]: break tower")
        pydirectinput.press(config["meleeAttack"])
        sleepClickOrPress()
        pydirectinput.press(config["meleeAttack"])
        sleepClickOrPress()
        pydirectinput.press(config["meleeAttack"])
        sleepClickOrPress()
        pydirectinput.press(config["meleeAttack"])
        mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
        return True

    return False


def checkMob():
    mob = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-mob.png",
        confidence=0.8,
        region=config["regions"]["minimap"],
    )
    if mob != None:
        logging.info("[Chaos]: [mob      ]")
        x, y = mob
        realX, realY = calculateMinimapRelative(x, y)
        sleepClickOrPress()
        pydirectinput.click(x=realX, y=realY, button="left")
        sleepClickOrPress()
        mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
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

    logging.info("[Chaos]: [rand move]: x: {} y: {}".format(x, y))
    pydirectinput.click(x=x, y=y, button=config["move"])
    sleepClickOrPress()
    pydirectinput.click(
        x=config["screenCenterX"], y=config["screenCenterY"], button=config["move"]
    )


def combatInFloor1():
    global characterIndex
    logging.info("------------Chaos Floor1------------")

    while (1):
        checkHealth()
        checkDeath()

        if not characters[characterIndex]["class"] in classes_stance:
            if checkPortal():
                continue

        useAbilities(key_list_common, characters[characterIndex]["class"])

        if checkBlackScreen():
            return

        if checkTimeout() == "TIMEOUT":
            sleepTransportLoading()
            return "TIMEOUT"


def combatInFloor2():
    global characterIndex
    logging.info("------------Chaos Floor2------------")

    prepareUltCnt = 0

    while (1):
        prepareUltCnt += 1
        if prepareUltCnt == 10:
            break

        checkHealth()
        checkDeath()

        if characters[characterIndex]["class"] not in classes_stance:
            if checkPortal():
                continue

        useAbilities(key_list_common, characters[characterIndex]["class"])

    pyautogui.keyDown("v")
    sleepClickOrPress()
    pyautogui.keyUp("v")

    while (1):
        prepareUltCnt += 1

        checkHealth()
        checkDeath()
        checkBossToV()

        if characters[characterIndex]["class"] not in classes_stance:
            if checkPortal():
                continue

        useAbilities(key_list_common, characters[characterIndex]["class"])

        if checkBlackScreen():
            return

        if prepareUltCnt >= 30 and checkTimeout() == "TIMEOUT":
            sleepTransportLoading()
            return "TIMEOUT"


def combatInFloor3():
    global characterIndex
    logging.info("------------Chaos Floor3------------")

    prepareUltCnt = 0
    moveCnt = 0
    findTowerCnt = 0

    while (1):
        prepareUltCnt += 1

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
            mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
            if findTowerCnt == 3:
                randomMove()
                findTowerCnt =0
            continue
        clickTower()

        if useAbilities(key_list_common_ult, characters[characterIndex]["class"]):
            checkMob()
            moveCnt += 1
            if moveCnt == 3:
                randomMove()
                moveCnt = 0

        if checkChaosFinish():
            sleepTransportLoading()
            return

        if prepareUltCnt >= 30 and checkTimeout() == "TIMEOUT":
            sleepTransportLoading()
            return "TIMEOUT"


def chaosCombat(index):
    global characterIndex
    characterIndex = index
    sleepClickOrPress()
    mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
    sleepClickOrPressLong()
    pydirectinput.click(button="right")
    saveAbilitiesScreenshots(characters[characterIndex]["class"])
    if combatInFloor1() == "TIMEOUT":
        logging.info("-------------Chaos Exit-------------")
        return False
    if combatInFloor2() == "TIMEOUT":
        logging.info("-------------Chaos Exit-------------")
        return False
    if combatInFloor3() == "TIMEOUT":
        logging.info("-------------Chaos Exit-------------")
        return False
    logging.info("-------------Chaos Exit-------------")
    return True


def stub():
    global characterIndex
    global layer
    mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
    sleepClickOrPressLong()
    pydirectinput.click(button="right")
    saveAbilitiesScreenshots(characters[characterIndex]["class"])
    if layer != 2 and layer != 3:
        if combatInFloor1() == "TIMEOUT":
            return
    if layer != 3:
        if combatInFloor2() == "TIMEOUT":
            return
    combatInFloor3()


def main():
    global characterIndex
    global layer
    parser = argparse.ArgumentParser(description="Optional app description")
    parser.add_argument("--ci", type=int, help="character index")
    parser.add_argument("--l", type=int, help="character index")
    args = parser.parse_args()
    if args.ci:
        characterIndex = args.ci
    if args.l:
        layer = args.l

    stub()


if __name__ == '__main__':
    main()

