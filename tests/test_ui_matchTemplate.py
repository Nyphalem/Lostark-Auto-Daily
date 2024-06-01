import unittest
import argparse
import sys, os

import pyautogui
import time
import win32gui
import logging

import cv2
import numpy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils
from originConfig import config


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


time_script = 0


class TestUI_matchTemplate(unittest.TestCase):

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
    python -m unittest tests.test_ui_matchTemplate.TestUI_matchTemplate.test_detectUI_portal
    '''
    def test_detectUI_portal(self):
        while (1):
            currentTime = int(time.time_ns() / 1000000)
            diffTime = currentTime - self.startTime
            if diffTime >= self.coninueTime:
                break

            screenshot = pyautogui.screenshot(region=(0,0,1920,1080))
            screenshot = cv2.cvtColor(numpy.array(screenshot), 0)
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

            aim = "screenshots\chaos-portal.png"
            template_img = cv2.imread(aim, 0)
            result = cv2.matchTemplate(screenshot, template_img, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val > 0.4:
                logging.info("[Test]: portal: {" + str(max_loc[0]) + ", " + str(max_loc[1]) + "}")
            else:
                logging.info("[Test]: portal: {" + "NA" + "}")


    def test_detectUI_portalBottom(self):
        while (1):
            currentTime = int(time.time_ns() / 1000000)
            diffTime = currentTime - self.startTime
            if diffTime >= self.coninueTime:
                break

            screenshot = pyautogui.screenshot(region=(0,0,1920,1080))
            screenshot = cv2.cvtColor(numpy.array(screenshot), 0)
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

            aim = "screenshots\chaos-portal-bottom.png"
            template_img = cv2.imread(aim, 0)
            result = cv2.matchTemplate(screenshot, template_img, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val > 0.6:
                logging.info("[Test]: portal: {" + str(max_loc[0]) + ", " + str(max_loc[1]) + "}")
            else:
                logging.info("[Test]: portal: {" + "NA" + "}")


def waitForSwitchToLostArk():
    logging.info("[Test]: start after 2s")
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