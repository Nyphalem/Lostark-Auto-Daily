import pyautogui
import time
import random
from utils import *
import argparse
from personalCharacters import *
from originConfigAbilities import *
import math


key_list = ['q', 'r', 'w', 'e', 'a', 's', 'd', 'f', 'x']
key_list_ult = ['q', 'r', 'w', 'e', 'a', 's', 'd', 'f', 'x', 'v']

key_list_demonic = ['q', 'r', 'w', 'e', 'a', 's', 'd', 'f']
key_list_demonic_z = ['q', 'r', 'w', 'e', 'a', 's']
key_list_demonic_z_reverse = ['s', 'a', 'e', 'w', 'r', 'q']

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
            sleep(200, 300)


def usbAbilitiesCommon(key_list):
    pyautogui.keyDown("g")
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
            else:
                time.sleep(random.uniform(0.3, 0.5))
    pyautogui.keyUp(key_list[click_random])
    time.sleep(random.uniform(0.3, 0.5))
    pyautogui.keyUp("g")
    return True


def useAbilities(key_list, characterClass):
    if characterClass != "demonic":
        if usbAbilitiesCommon(key_list):
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
            time.sleep(random.uniform(0.3, 0.5))
            pyautogui.keyUp("z")
            sleepClickOrPressList()
            return True
        if z_active != None:
            for ability in key_list_demonic_z:
                pyautogui.press(ability)
                time.sleep(random.uniform(0.0, 0.1))
            pyautogui.keyDown("g")
            time.sleep(random.uniform(0.3, 0.5))
            pyautogui.keyUp("g")
            for ability in key_list_demonic_z_reverse:
                pyautogui.press(ability)
                time.sleep(random.uniform(0.0, 0.1))
            pyautogui.keyDown("g")
            time.sleep(random.uniform(0.3, 0.5))
            pyautogui.keyUp("g")
            return True
        if z_fade != None:
            usbAbilitiesCommon(key_list_demonic)
            return True
    return False


def checkBlackScreen():
    x, y = (131, 1103)
    r, g, b = pyautogui.pixel(x, y)
    if r + g + b < 60:
        print("checkBlackScreen: {hit}")
        mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
        return True


def checkHealth():
    if config["useHealthPot"] == False:
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
            print("checkHealth: {health pot pressed}")
            pydirectinput.press(config["healthPot"])
    return


def checkDeath():
    return


def checkTimeout():
    return


def checkAsh():
    ash = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-ash.png",
        region=config["regions"]["center"],
        confidence=0.75
    )
    if ash != None:
        x, y = ash
        mouseMoveTo(x=x, y=y)
        sleepClickOrPress()
        pydirectinput.click(x=x, y=y, button="left")
        sleepClickOrPress()
        pydirectinput.press("g")
        sleepClickOrPressLong()
    else:
        return


def checkBoss():
    bossBar = pyautogui.locateOnScreen(
        "./screenshots/chaos-bossBar.png", confidence=0.7
    )
    if bossBar != None:
        pyautogui.press("v")


def checkChaosFinish():
    chaosFinish = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-finish.png",
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
            region=config["regions"]["portal"],
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
                region=config["regions"]["portal"],
                confidence=0.7
            )
            if chaosExit2 != None:
                x, y = chaosExit2
                mouseMoveTo(x=x, y=y)
                sleepClickOrPressLong()
                pydirectinput.click(x=x, y=y, button="left")
                print("timeout!")
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
        print("checkTower: {" + "tower image x: {} y: {}".format(x, y) + "}")
        return x, y
    elif towerTop != None:
        x, y = towerTop
        print("checkTower: {" + "towerTop image x: {} y: {}".format(x, y) + "}")
        return x, y
    elif towerBot != None:
        x, y = towerBot
        print("checkTower: {" + "towerBot image x: {} y: {}".format(x, y) + "}")
        return x, y
    return -1, -1


def calculateMinimapRelative(x, y):
    selfLeft = config["minimapCenterX"]
    selfTop = config["minimapCenterY"]

    x = x - selfLeft
    y = y - selfTop

    dist = 200
    if y < 0:
        dist = -dist
    if x == 0:
        if y < 0:
            newY = y - abs(dist)
        else:
            newY = y + abs(dist)
        # print("relative to center pos newX: 0 newY: {}".format(int(newY)))
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
    newX = (newY - y) / k + x

    if newX < 0 and abs(newX) > config["clickableAreaX"]:
        newX = -config["clickableAreaX"]
        if newY < 0:
            newY = newY + abs(dist) * 0.25
        else:
            newY = newY - abs(dist) * 0.25
    elif newX > 0 and abs(newX) > config["clickableAreaX"]:
        newX = config["clickableAreaX"]
        if newY < 0:
            newY = newY + abs(dist) * 0.25
        else:
            newY = newY - abs(dist) * 0.25
    if newY < 0 and abs(newY) > config["clickableAreaY"]:
        newY = -config["clickableAreaY"]
        if newX < 0:
            newX = newX + abs(dist) * 0.7
        else:
            newX = newX - abs(dist) * 0.7
    elif newY > 0 and abs(newY) > config["clickableAreaY"]:
        newY = config["clickableAreaY"]
        if newX < 0:
            newX = newX + abs(dist) * 0.7
        else:
            newX = newX - abs(dist) * 0.7

    r_x = int(newX) + config["screenCenterX"]
    r_y = int(newY) + config["screenCenterY"]
    return r_x, r_y


def clickTower():
    riftCore1 = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-riftcore1.png",
        confidence=0.6,
        region=config["regions"]["portal"],
    )
    riftCore2 = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-riftcore2.png",
        confidence=0.6,
        region=config["regions"]["portal"],
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
        print("clicked rift core")
        sleep(100, 120)
        pydirectinput.press(config["meleeAttack"])
        sleep(300, 360)
        pydirectinput.press(config["meleeAttack"])
        sleep(300, 360)
        pydirectinput.press(config["meleeAttack"])
        sleep(100, 120)
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
        print("clicked rift core")
        sleep(100, 120)
        pydirectinput.press(config["meleeAttack"])
        sleep(300, 360)
        pydirectinput.press(config["meleeAttack"])
        sleep(300, 360)
        pydirectinput.press(config["meleeAttack"])
        sleep(100, 120)
        pydirectinput.press(config["meleeAttack"])
        mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])


def checkMob():
    mob = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-mob.png",
        confidence=0.8,
        region=config["regions"]["minimap"],
    )
    if mob != None:
        print("Mob!!!")
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

    print("random move to x: {} y: {}".format(x, y))
    pydirectinput.click(x=x, y=y, button=config["move"])
    sleep(200, 250)
    pydirectinput.click(x=x, y=y, button=config["move"])
    sleep(200, 250)
    pydirectinput.click(
        x=config["screenCenterX"], y=config["screenCenterY"], button=config["move"]
    )
    sleep(100, 150)


def combatInFloor1():
    print("------------combatInFloor1------------")
    while (1):
        checkHealth()

        if useAbilities(key_list, characters[characterIndex]["class"]):
            if characters[characterIndex]["class"] != "bard":
                if not checkMob():
                    randomMove()

        if checkBlackScreen():
            return

        if checkTimeout() == "TIMEOUT":
            return "TIMEOUT"


def combatInFloor2():
    print("------------combatInFloor2------------")
    prepareUltCnt = 0
    while (1):
        checkHealth()

        if useAbilities(key_list, characters[characterIndex]["class"]):
            if characters[characterIndex]["class"] != "bard":
                if not checkMob():
                    randomMove()

        prepareUltCnt += 1
        if prepareUltCnt == 10:
            break

    pyautogui.keyDown("v")
    time.sleep(random.uniform(0.3, 0.5))
    pyautogui.keyUp("v")

    while (1):
        prepareUltCnt += 1
        checkHealth()
        checkBoss()

        if useAbilities(key_list, characters[characterIndex]["class"]):
            if characters[characterIndex]["class"] != "bard":
                if not checkMob():
                    randomMove()

        if checkBlackScreen() and prepareUltCnt > 30:
            return

    if checkTimeout() == "TIMEOUT":
        return "TIMEOUT"


def combatInFloor3():
    print("------------combatInFloor3------------")
    prepareUltCnt = 0
    while (1):
        prepareUltCnt += 1
        checkHealth()
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

        if useAbilities(key_list_ult, characters[characterIndex]["class"]):
            if not checkMob():
                randomMove()

        if checkChaosFinish():
            return

        if prepareUltCnt >= 30 and checkTimeout() == "TIMEOUT":
            return "TIMEOUT"


def stub():
    time.sleep(2)
    mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
    time.sleep(2)
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
