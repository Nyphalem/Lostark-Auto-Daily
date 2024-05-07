# -*- coding : utf--8 -*-
import pyautogui
import time
import random
import win32gui
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


key_list = ['q', 'r', 'w', 'e', 'a', 's', 'd', 'f', 'v', 'x']
key_list_demon = ['w', 'e', 'a', 's', 'd', 'f', 'v']


def check_hwnd(hwnd):
    title = win32gui.GetWindowText(hwnd)
    if "命运方舟" not in title:
        logging.info(f"焦点窗口非命运方舟")
        exit(1)


def waitForSwitchToLostArk():
    logging.info("5秒后开刷！！！")
    pyautogui.click(x=1085, y=647, clicks=1, button='right')
    time.sleep(5)


def click_all():
    # automatically open inventory
    bagExist = pyautogui.locateCenterOnScreen(
        "./screenshots/bag.png",
        confidence=0.6,
        grayscale=True
    )
    if bagExist == None:
        pyautogui.keyDown("i")
        time.sleep(random.uniform(0.3, 0.5))
        pyautogui.keyUp("i")

    i = 0
    print("---------------------------")
    while (1):
        bagExist = pyautogui.locateCenterOnScreen(
            "./screenshots/bag.png",
            confidence=0.6,
            grayscale=True
        )

        if bagExist == None:
            print("---------------------------")
            logging.info("5秒后返回领地并停止程序")
            time.sleep(random.uniform(5,5.5))
            pyautogui.keyDown("f2")
            time.sleep(random.uniform(0.3, 0.5))
            pyautogui.keyUp("f2")
            time.sleep(random.uniform(10, 12))
            break

        i = i + 1
        size = len(key_list)
        click_random = random.randint(0, size-1)
        #'''
        pyautogui.click(x=1085, y=647, clicks=0, button='right')
        pyautogui.keyDown(key_list[click_random])
        time.sleep(random.uniform(0.3, 0.5))
        pyautogui.keyUp(key_list[click_random])
        #'''
        '''
        if i % 20 == 0:
            pyautogui.click(x=906, y=397, clicks=1, button='left')
            time.sleep(random.uniform(0.3, 0.5))
        '''
        if i % 1000 == 0:
            logging.info("尝试返回领地")
            time.sleep(random.uniform(5,5.5))
            pyautogui.keyDown("f2")
            time.sleep(random.uniform(0.3, 0.5))
            pyautogui.keyUp("f2")
            time.sleep(random.uniform(20, 22))

            bagExist = pyautogui.locateCenterOnScreen(
                "./screenshots/bag.png",
                confidence=0.9,
            )
            if not bagExist == None:
                i -= 1
                continue
            else:
                logging.info("成功返回领地！")

            logging.info("move!")
            time.sleep(random.uniform(1.3, 2.5))
            pyautogui.leftClick(x=960, y=540, interval=0.0, duration=0.0)
            time.sleep(random.uniform(1.3, 2.5))
            pyautogui.leftClick(x=929, y=523, interval=0.0, duration=0.0)
            time.sleep(random.uniform(100,200))
            logging.info("炮管冷却完毕")

            bagExist = pyautogui.locateCenterOnScreen(
                "./screenshots/bag.png",
                confidence=0.6,
                grayscale=True
            )
            if bagExist == None:
                pyautogui.keyDown("f5")
                time.sleep(random.uniform(0.3, 0.5))
                pyautogui.keyUp("f5")
                logging.info("返回战场")
                time.sleep(random.uniform(20, 22))

            bagExist = pyautogui.locateCenterOnScreen(
                "./screenshots/bag.png",
                confidence=0.6,
                grayscale=True
            )
            if bagExist == None:
                time.sleep(random.uniform(5,5.5))
                pyautogui.keyDown("i")
                time.sleep(random.uniform(0.3, 0.5))
                pyautogui.keyUp("i")

            i = 0


def desire():
    waitForSwitchToLostArk()
    hwnd = win32gui.GetForegroundWindow()
    check_hwnd(hwnd)
    #global config
    #config = loadConfig()
    #config["hwnd"] = hwnd
    click_all()
    # get_cursor_position()


if __name__ == '__main__':
    desire()
