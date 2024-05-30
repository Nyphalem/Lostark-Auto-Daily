import pyautogui
import time
import random
from utils import *
import argparse
from personalCharacters import *
from originConfigAbilities import *
import math


key_list_common = ['q', 'r', 'w', 'e', 'a', 's', 'd', 'f', 'x']
key_list_common_ult = ['q', 'r', 'w', 'e', 'a', 's', 'd', 'f', 'x', 'v']

key_list_holyknight = ['q', 'r', 'w', 'e', 'a', 's', 'd', 'f']

key_list_demonic = ['q', 'r', 'w', 'e', 'a', 's', 'd', 'f']
key_list_demonic_z = ['q', 'r', 'w', 'e', 'a', 's']
key_list_demonic_z_reverse = ['s', 'a', 'e', 'w', 'r', 'q']

key_list_gunslinger = ['q', 'r', 'w', 'e', 'a', 's']

key_list_slayer = ['q', 'r', 'w', 'e', 'a', 's', 'd', 'f']

key_list_aeromancer = ['q', 'r', 'w', 'e', 'a', 's', 'd', 'f']

key_list_blade = ['q', 'r', 'w', 'e', 'a', 's', 'd', 'f']


# global constant
abilityScreenshots = []
characterIndex = 0


# script constant
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


def usbAbilitiesCommon(key_list):
    sleepClickOrPress()
    pyautogui.keyDown(config["interact"])
    sleepClickOrPress()
    pyautogui.keyUp(config["interact"])
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
                return False
    pyautogui.keyDown(key_list[click_random])
    for ability in abilityScreenshots:
        if key_list[click_random] == ability["key"]:
            if ability["cast"] == True:
                time.sleep(random.uniform(ability["castTime"], ability["castTime"] + 0.5))
            elif ability["hold"] == True and ability["holdTime"] != None:
                time.sleep(random.uniform(ability["holdTime"], ability["holdTime"] + 0.5))
            elif ability["doubleClick"] == True:
                for i in range(10):
                    sleepWink()
                    pyautogui.keyUp(key_list[click_random])
                    pyautogui.keyDown(key_list[click_random])
                sleepClickOrPress()
            else:
                sleepClickOrPress()
    pyautogui.keyUp(key_list[click_random])
    return True


def useAbilities(key_list, characterClass):
    if characterClass == "bard":
        if usbAbilitiesCommon(key_list):
            return True
    if characterClass == "holyknight":
        # TODO: check for enable z
        if False:
            pyautogui.keyDown("z")
            sleepClickOrPress()
            pyautogui.keyUp("z")
        if usbAbilitiesCommon(key_list_holyknight):
            return True
    if characterClass == "gunslinger":
        # TODO: tuning
        if usbAbilitiesCommon(key_list_gunslinger):
            return True
    if characterClass == "slayer":
        # TODO: check for enable z
        if False:
            pyautogui.keyDown("z")
            sleepClickOrPress()
            pyautogui.keyUp("z")
        if usbAbilitiesCommon(key_list_slayer):
            return True
    if characterClass == "aeromancer":
        # TODO: tuning
        if usbAbilitiesCommon(key_list_aeromancer):
            return True
    if characterClass == "blade":
        # TODO: tuning
        if usbAbilitiesCommon(key_list_blade):
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
            sleepClickOrPress()
            pyautogui.keyUp("z")
            sleepClickOrPressList()
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
            usbAbilitiesCommon(key_list_demonic)
            return True
    return False


def checkBlackScreen():
    x, y = (131, 1103)
    r, g, b = pyautogui.pixel(x, y)
    if r + g + b < 60:
        logging.info("[Chaos]: [black screen]")
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
            logging.info("[Chaos]: [health potion]")
            pydirectinput.press(config["healthPot"])
    return


def checkDeath():
    revive = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-revive.png",
        region=config["regions"]["whole-game"],
        confidence=0.9
    )
    if revive != None:
        x, y = revive
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPressLong()


def checkPortal():
    # TODO: check portal in minimap and move to portal
    return


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


def checkBoss():
    # TODO: check boss in minimap and move to boss
    bossBar = pyautogui.locateOnScreen(
        "./screenshots/chaos-bossBar.png",
        region=config["regions"]["whole-game"],
        confidence=0.7
    )
    if bossBar != None:
        pyautogui.press(config["awakening"])


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
                logging.info("[Chaos]: [timeout]")
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
        logging.info("[Chaos]: [tower]: " + "image x: {} y: {}".format(x, y))
        return x, y
    elif towerTop != None:
        x, y = towerTop
        logging.info("[Chaos]: [tower]: " + "TOP image x: {} y: {}".format(x, y))
        return x, y
    elif towerBot != None:
        x, y = towerBot
        logging.info("[Chaos]: [tower]: " + "BOT image x: {} y: {}".format(x, y))
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
        logging.info("[Chaos]: [tower]: break tower")
        pydirectinput.press(config["meleeAttack"])
        sleepClickOrPress()
        pydirectinput.press(config["meleeAttack"])
        sleepClickOrPress()
        pydirectinput.press(config["meleeAttack"])
        sleepClickOrPress()
        pydirectinput.press(config["meleeAttack"])
        mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
    elif riftCore2 != None:
        x, y = riftCore2
        if y > 650 or x < 400 or x > 1500:
            return
        click_x = x
        click_y = y + 190
        pydirectinput.click(
            x=click_x, y=click_y, button=config["move"]
        )
        logging.info("[Chaos]: [tower]: break tower")
        pydirectinput.press(config["meleeAttack"])
        sleepClickOrPress()
        pydirectinput.press(config["meleeAttack"])
        sleepClickOrPress()
        pydirectinput.press(config["meleeAttack"])
        sleepClickOrPress()
        pydirectinput.press(config["meleeAttack"])
        mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])


def checkMob():
    mob = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-mob.png",
        confidence=0.8,
        region=config["regions"]["minimap"],
    )
    if mob != None:
        logging.info("[Chaos]: [mob]")
        x, y = mob
        realX, realY = calculateMinimapRelative(x, y)
        sleepClickOrPress()
        pydirectinput.click(x=realX, y=realY, button="left")
        sleepClickOrPressLong()
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

    logging.info("[Chaos]: [random move]: x: {} y: {}".format(x, y))
    pydirectinput.click(x=x, y=y, button=config["move"])
    sleepClickOrPress()
    pydirectinput.click(x=x, y=y, button=config["move"])
    sleepClickOrPress()
    pydirectinput.click(
        x=config["screenCenterX"], y=config["screenCenterY"], button=config["move"]
    )
    sleepClickOrPress()


def combatInFloor1():
    logging.info("---------------Floor1---------------")
    while (1):
        checkHealth()
        checkDeath()

        if useAbilities(key_list_common, characters[characterIndex]["class"]):
            if characters[characterIndex]["class"] != "bard":
                if not checkMob():
                    randomMove()

        if checkBlackScreen():
            return

        if checkTimeout() == "TIMEOUT":
            return "TIMEOUT"


def combatInFloor2():
    logging.info("---------------Floor2---------------")
    prepareUltCnt = 0
    while (1):
        checkHealth()
        checkDeath()

        if useAbilities(key_list_common, characters[characterIndex]["class"]):
            if characters[characterIndex]["class"] != "bard":
                if not checkMob():
                    randomMove()

        prepareUltCnt += 1
        if prepareUltCnt == 10:
            break

    pyautogui.keyDown("v")
    sleepClickOrPress()
    pyautogui.keyUp("v")

    while (1):
        prepareUltCnt += 1
        checkHealth()
        checkBoss()

        if useAbilities(key_list_common, characters[characterIndex]["class"]):
            if characters[characterIndex]["class"] != "bard":
                if not checkMob():
                    randomMove()

        if checkBlackScreen():
            return

        if checkTimeout() == "TIMEOUT" and prepareUltCnt > 30:
            return "TIMEOUT"


def combatInFloor3():
    logging.info("---------------Floor3---------------")
    prepareUltCnt = 0
    i = 0
    while (1):
        prepareUltCnt += 1
        checkHealth()
        checkDeath()
        checkAsh()

        # Tower
        x, y = checkTower()
        if x != -1 and y != -1:
            realX, realY = calculateMinimapRelative(x, y)
            sleepClickOrPress()
            pydirectinput.click(x=realX, y=realY, button="left")
            sleepClickOrPressList()
            mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
        clickTower()

        if useAbilities(key_list_common_ult, characters[characterIndex]["class"]):
            checkMob()
            i += 1
            if i == 3:
                randomMove()
                i = 0

        if checkChaosFinish():
            sleepTransportLoading()
            return

        if prepareUltCnt >= 30 and checkTimeout() == "TIMEOUT":
            sleepTransportLoading()
            return "TIMEOUT"


def chaosCombat(index):
    characterIndex = index
    sleepClickOrPress()
    mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
    sleepClickOrPress()
    saveAbilitiesScreenshots(characters[characterIndex]["class"])
    pydirectinput.click(button="right")
    if combatInFloor1() == "TIMEOUT":
        return
    if combatInFloor2() == "TIMEOUT":
        return
    combatInFloor3()
    return


def stub():
    mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
    sleepClickOrPressLong()
    pydirectinput.click(button="right")
    saveAbilitiesScreenshots(characters[characterIndex]["class"])
    if layer == -1:
        if combatInFloor1() == "TIMEOUT":
            return
        if combatInFloor2() == "TIMEOUT":
            return
    combatInFloor3()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Optional app description")
    parser.add_argument("--ci", type=int, help="character index")
    parser.add_argument("--l", type=int, help="character index")
    args = parser.parse_args()
    if args.ci:
        characterIndex = args.ci
    if args.l:
        layer = args.l

    stub()
