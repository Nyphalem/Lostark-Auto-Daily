# -*- coding : utf--8 -*-
import pyautogui
import time
import random
import win32gui

key_list = ['q', 'w', 'e', 'r', 'a', 's', 'd', 'f', 'v','x']

def check_hwnd(hwnd):
    title = win32gui.GetWindowText(hwnd)
    if "命运方舟" not in title:
        print(f"焦点窗口非命运方舟")
        exit(1)

def waitForSwitchToLostArk():
    print("5秒内请切换至命运方舟")
    time.sleep(5)

def click_all():
    i = 0
    while (1):
        i = i + 1

        size = len(key_list)
        click_random = random.randint(0, size-1)

        if click_random == 5:
            pyautogui.click(x=1327, y=575, clicks=1, button='right')
        else:
            pyautogui.click(x=1327, y=575, clicks=0, button='right')
        pyautogui.keyDown(key_list[click_random])
        time.sleep(random.uniform(0.3, 0.5))
        pyautogui.keyUp(key_list[click_random])

        if i % 100 == 0:
            pyautogui.leftClick(x=1540, y=562, interval=0.0, duration=0.0)
            time.sleep(random.uniform(1.3, 2.5))
            pyautogui.leftClick(x=932, y=804, interval=0.0, duration=0.0)
            time.sleep(random.uniform(1.3, 2.5))
            print(i)
            i = 0

def main():
    waitForSwitchToLostArk()
    hwnd = win32gui.GetForegroundWindow()
    check_hwnd(hwnd)
    #global config
    #config = loadConfig() 
    #config["hwnd"] = hwnd
    click_all()
    # get_cursor_position()

if __name__ == '__main__':
    main()
