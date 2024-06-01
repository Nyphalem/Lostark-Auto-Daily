import unittest
import argparse
import sys, os

import pyautogui
import time
import win32gui
import logging

import main

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


time_script = 0


class TestMain(unittest.TestCase):

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
    python -m unittest tests.test_main_function.TestMain.test_main_disenchant
    '''
    def test_main_disenchant(self):
        main.doDisenchant()

    '''
    python -m unittest tests.test_main_function.TestMain.test_main_repair
    '''
    def test_main_repair(self):
        main.doRepairMasyaf()


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