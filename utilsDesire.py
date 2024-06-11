# -*- coding : utf--8 -*-
import pyautogui
import time
import random
import win32gui
import logging
from utils import *


key_list = ['q', 'r', 'w', 'e', 'a', 's', 'd', 'f', 'v', 'x']
key_list_demon = ['w', 'e', 'a', 's', 'd', 'f', 'v']


def check_hwnd(hwnd):
    title = win32gui.GetWindowText(hwnd)
    if "命运方舟" not in title:
        logging.info(f"焦点窗口非命运方舟")
        exit(1)


def waitForSwitchToLostArk():
    logging.info("2秒后开刷")
    pyautogui.click(x=1085, y=647, clicks=1, button='right')
    time.sleep(2)


def click_all():
    # automatically open inventory
    bagExist = pyautogui.locateCenterOnScreen(
        "./screenshots/bag.png",
        region=config["regions"]["whole-game"],
        confidence=0.8,
        grayscale=True
    )
    if bagExist == None:
        pyautogui.keyDown("i")
        sleepClickOrPress()
        pyautogui.keyUp("i")
    sleepClickOrPressLong()

    i = 0
    logging.info("------------------------------------")
    while (1):
        bagExist = pyautogui.locateCenterOnScreen(
            "./screenshots/bag.png",
            region=config["regions"]["whole-game"],
            confidence=0.8,
            grayscale=True
        )
        if bagExist == None:
            logging.info("------------------------------------")
            logging.info("5秒后返回领地并停止程序")
            sleepCommonProcess()
            pyautogui.keyDown("f2")
            sleepClickOrPress()
            pyautogui.keyUp("f2")
            sleepTransportLoading()
            break

        i = i + 1
        size = len(key_list)
        click_random = random.randint(0, size-1)
        pyautogui.click(x=1085, y=647, clicks=0, button='right')
        pyautogui.keyDown(key_list[click_random])
        sleepClickOrPress()
        pyautogui.keyUp(key_list[click_random])

        if i % 1000 == 0:
            logging.info("尝试返回领地")
            sleepCommonProcess()
            pyautogui.keyDown("f2")
            sleepClickOrPress()
            pyautogui.keyUp("f2")
            sleepTransportLoading()

            bagExist = pyautogui.locateCenterOnScreen(
                "./screenshots/bag.png",
                region=config["regions"]["whole-game"],
                confidence=0.7,
                grayscale=True
            )
            if not bagExist == None:
                i -= 1
                continue
            else:
                logging.info("成功返回领地！")

            logging.info("move!")
            sleepClickOrPressLong()
            pyautogui.leftClick(x=960, y=540, interval=0.0, duration=0.0)
            sleepClickOrPressLong()
            pyautogui.leftClick(x=929, y=523, interval=0.0, duration=0.0)
            sleepWink()
            logging.info("炮管冷却完毕")

            bagExist = pyautogui.locateCenterOnScreen(
                "./screenshots/bag.png",
                region=config["regions"]["whole-game"],
                confidence=0.8,
                grayscale=True
            )
            if bagExist == None:
                pyautogui.keyDown("f5")
                sleepClickOrPress()
                pyautogui.keyUp("f5")
                logging.info("返回战场")
                sleepTransportLoading()

            bagExist = pyautogui.locateCenterOnScreen(
                "./screenshots/bag.png",
                region=config["regions"]["whole-game"],
                confidence=0.8,
                grayscale=True
            )
            if bagExist == None:
                sleepCommonProcess()
                pyautogui.keyDown("i")
                sleepClickOrPress()
                pyautogui.keyUp("i")

            i = 0


def desire():
    waitForSwitchToLostArk()
    hwnd = win32gui.GetForegroundWindow()
    check_hwnd(hwnd)
    click_all()


if __name__ == '__main__':
    desire()
