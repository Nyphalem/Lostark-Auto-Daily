import pyautogui
import time
import random
from utils import *
import argparse
from characters import *
from abilities import *


key_list = ['q', 'r', 'w', 'e', 'a', 's', 'd', 'f', 'x']
key_list_ult = ['q', 'r', 'w', 'e', 'a', 's', 'd', 'f', 'x', 'v']

key_list_demonic = ['q', 'r', 'w', 'e', 'a', 's', 'd', 'f']
key_list_demonic_z = ['q', 'r', 'w', 'e', 'a', 's']
key_list_demonic_z_reverse = ['s', 'a', 'e', 'w', 'r', 'q']

abilityScreenshots = []

characterIndex = 0


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


def useAbilities(key_list, characterClass):
    if characterClass == "bard":
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
                    return
        pyautogui.keyDown("g")
        time.sleep(random.uniform(0.3, 0.5))
        pyautogui.keyUp("g")
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
        return
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
            return
        if z_active != None:
            pyautogui.keyDown("g")
            time.sleep(random.uniform(0.3, 0.5))
            pyautogui.keyUp("g")
            for ability in key_list_demonic_z:
                pyautogui.press(ability)
                time.sleep(random.uniform(0.0, 0.1))
            for ability in key_list_demonic_z_reverse:
                pyautogui.press(ability)
                time.sleep(random.uniform(0.0, 0.1))
            return
        if z_fade != None:
            size = len(key_list_demonic)
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
                        return
            pyautogui.keyDown("g")
            time.sleep(random.uniform(0.3, 0.5))
            pyautogui.keyUp("g")
            pyautogui.keyDown(key_list_demonic[click_random])
            time.sleep(random.uniform(0.3, 0.5))
            pyautogui.keyUp(key_list_demonic[click_random])
            return


def checkBlackScreen():
    x, y = (710, 50)
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


def checkAsh():
    ash = pyautogui.locateCenterOnScreen(
        "./screenshots/chaos-ash.png",
        region=config["regions"]["center"],
        confidence=0.75
    )
    if ash != None:
        print("checkAsh: {hit: " + x + y + "}")
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
        return True
    elif towerTop != None:
        x, y = towerTop
        print("checkTower: {" + "towerTop image x: {} y: {}".format(x, y) + "}")
        return True
    elif towerBot != None:
        x, y = towerBot
        print("checkTower: {" + "towerBot image x: {} y: {}".format(x, y) + "}")
        return True


def combatInFloor1():
    print("------------combatInFloor1------------")
    while (1):
        checkHealth()

        useAbilities(key_list, characters[characterIndex]["class"])

        if checkBlackScreen():
            return


def combatInFloor2():
    print("------------combatInFloor2------------")
    prepareUltCnt = 0
    while (1):
        checkHealth()

        useAbilities(key_list, characters[characterIndex]["class"])

        prepareUltCnt += 1
        if prepareUltCnt == 10:
            break

    pyautogui.keyDown("v")
    time.sleep(random.uniform(0.3, 0.5))
    pyautogui.keyUp("v")

    while (1):
        checkHealth()
        checkBoss()

        useAbilities(key_list, characters[characterIndex]["class"])

        if checkBlackScreen():
            return


def combatInFloor3():
    print("------------combatInFloor3------------")
    while (1):
        checkHealth()
        checkAsh()
        checkTower()

        useAbilities(key_list_ult, characters[characterIndex]["class"])

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
                    return


def stub():
    time.sleep(2)
    mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
    time.sleep(2)
    pydirectinput.click(button="right")
    saveAbilitiesScreenshots(characters[characterIndex]["class"])
    combatInFloor1()
    combatInFloor2()
    combatInFloor3()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Optional app description")
    parser.add_argument("--ci", type=int, help="character index")
    args = parser.parse_args()
    if args.ci:
        characterIndex = args.ci

    stub()
