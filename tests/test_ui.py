import unittest
import argparse
import sys, os

import pyautogui
import time
import win32gui
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils
from originConfig import config


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


time_script = 0


class TestUI(unittest.TestCase):

    def setUp(self):
        waitForSwitchToLostArk()
        hwnd = win32gui.GetForegroundWindow()
        correctWindow = check_hwnd(hwnd)
        #self.assertTrue(correctWindow)

        if time_script == 0:
            self.coninueTime = 3
        else:
            self.coninueTime = time_script
        self.coninueTime = self.coninueTime * 1000 # s->ms
        logging.info("[Test]: continue time: {" + str(self.coninueTime) + "ms}")

        print("----------------------------------------------------------------------")
        print(".")
        self.startTime = int(time.time_ns() / 1000000)

    '''
    python -m unittest tests.test_ui.TestUI.test_detectUI_bag
    '''
    def test_detectUI_bag(self):
        while(1):
            currentTime = int(time.time_ns() / 1000000)
            diffTime = currentTime - self.startTime
            if diffTime >= self.coninueTime:
                break

            try:
                bagExist = pyautogui.locateCenterOnScreen(
                    "./screenshots/bag.png",
                    confidence=0.8,
                    region=config["regions"]["whole-game"],
                    grayscale=True
                )
                if bagExist != None:
                    x, y = bagExist
                    logging.info("[Test]: [test_detectUI_bag]: bag.png: {" + str(x) + "," + str(y) + "}")
                else:
                    logging.info("[Test]: [test_detectUI_bag]: bag.png: {NONE}" )
            except pyautogui.ImageNotFoundException:
                logging.info("[Test]: [test_detectUI_bag]: bag.png: {NONE}" )

            utils.sleepClickOrPress()

    '''
    python -m unittest tests.test_ui.TestUI.test_detectUI_chaostimeout
    '''
    def test_detectUI_chaostimeout(self):
        while(1):
            currentTime = int(time.time_ns() / 1000000)
            diffTime = currentTime - self.startTime
            if diffTime >= self.coninueTime:
                break

            try:
                timeout = pyautogui.locateCenterOnScreen(
                    "./screenshots/chaos-timeout.png",
                    region=config["regions"]["chaos-remain-time"],
                    confidence=0.9
                )
                if timeout != None:
                    x, y = timeout
                    logging.info("[Test]: [test_detectUI_chaostimeout]: chaos-timeout.png: {" + str(x) + "," + str(y) + "}")
                else:
                    logging.info("[Test]: [test_detectUI_chaostimeout]: chaos-timeout.png: {NONE}" )
            except pyautogui.ImageNotFoundException:
                logging.info("[Test]: [test_detectUI_chaostimeout]: chaos-timeout.png: {NONE}" )

            utils.sleepClickOrPress()


def waitForSwitchToLostArk():
    logging.info("[Test]: start after 2s")
    pyautogui.click(x=1085, y=647, clicks=1, button='right')
    time.sleep(2)


def check_hwnd(hwnd):
    title = win32gui.GetWindowText(hwnd)
    if "命运方舟" not in title:
        logging.info(f"[Test]: not in game!!!!!")
        return False
    return True


def parse_test_args():
    parser = argparse.ArgumentParser(description='Test:UI.')
    parser.add_argument('--time', type=int, required=True, help='test continue time')
    args, remaining_argv = parser.parse_known_args()
    return args, sys.argv[:1] + remaining_argv


if __name__ == '__main__':
    args, remaining_argv = parse_test_args()
    if args.time != None:
        time_script = args.time
    sys.argv = remaining_argv

    # run unittest
    unittest.main()