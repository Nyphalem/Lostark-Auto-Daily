import sys
import threading
import time
import inspect
import ctypes
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QTextEdit, QPushButton, QPlainTextEdit, QRadioButton, QLabel, QLineEdit, QButtonGroup
from PySide6.QtGui import QGuiApplication, QFont

import main
import logging
import utils


class LogThread(threading.Thread):
    def __init__(self, log_widget):
        super().__init__()
        self.log_widget = log_widget
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.log_widget.append("helloworld")
            time.sleep(1)

    def stop(self):
        self.running = False


class ToolThread(threading.Thread):
    def run(self):
        main.main()


class PyLogHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        log_message = self.format(record)
        self.text_widget.appendPlainText(log_message)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("命运方舟打卡工具")

        screen_coor_x = 0
        screen_coor_y = 0
        screen = QGuiApplication.primaryScreen()
        screen = screen.size()
        screen_coor_x, screen_coor_y = screen.width(), screen.height()
        screen_coor_x -= (400 + 20)
        screen_coor_y -= (600 + 80)
        self.setGeometry(screen_coor_x, screen_coor_y, 400, 600)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.tool_tab = self.create_tab_tool()
        self.daily_tab = self.create_tab_daily()
        self.weekly_tab = self.create_tab_weekly()

        self.tab_widget.addTab(self.tool_tab, "打卡工具")
        self.tab_widget.addTab(self.daily_tab, "TEST1")
        self.tab_widget.addTab(self.weekly_tab, "TEST2")

        self.daily_thread = None
        self.weekly_thread = None


    def create_tab_tool(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.log_text_tool = QPlainTextEdit()
        self.log_text_tool.setReadOnly(True)
        self.log_text_tool.setStyleSheet("background-color: black; color: white;")
        font = QFont()
        font.setPointSize(8)
        font.setFamilies
        self.log_text_tool.setFont(font)
        self.redirect_logging(self.log_text_tool)

        start_button = QPushButton("开始")
        stop_button = QPushButton("终止")

        start_button.clicked.connect(self.startToolThread)
        stop_button.clicked.connect(self.stopToolThread)

        # param: "start_charac_index"
        layout_start_charac = QHBoxLayout()
        layout_start_charac_title = QLabel()
        layout_start_charac_title.setText("起始角色编号：")
        layout_start_charac_value = QLineEdit()
        layout_start_charac_cache = utils.read_status_value(utils.param_file_path, "start_charac_index")
        layout_start_charac_value.setText(str(layout_start_charac_cache))

        layout_start_charac.addWidget(layout_start_charac_title)
        layout_start_charac.addWidget(layout_start_charac_value)

        # param: "need_loop"
        layout_need_loop = QHBoxLayout()
        layout_need_loop_title = QLabel()
        layout_need_loop_title.setText("所有角色轮刷：")
        layout_need_loop_yes = QRadioButton(f"是")
        layout_need_loop_no = QRadioButton(f"否")
        layout_need_loop_judge = QButtonGroup(self)
        layout_need_loop_judge.addButton(layout_need_loop_yes)
        layout_need_loop_judge.addButton(layout_need_loop_no)
        layout_need_loop_cache = utils.read_status_value(utils.param_file_path, "need_loop")
        if layout_need_loop_cache:
            layout_need_loop_yes.setChecked(True)
        else:
            layout_need_loop_no.setChecked(True)
        layout_need_loop_yes.toggled.connect(on_need_loop_toggled)

        layout_need_loop.addWidget(layout_need_loop_title)
        layout_need_loop.addWidget(layout_need_loop_yes)
        layout_need_loop.addWidget(layout_need_loop_no)

        # param: "need_chaos"
        layout_need_chaos = QHBoxLayout()
        layout_need_chaos_title = QLabel()
        layout_need_chaos_title.setText("混沌地牢轮刷：")
        layout_need_chaos_yes = QRadioButton(f"是")
        layout_need_chaos_no = QRadioButton(f"否")
        layout_need_chaos_judge = QButtonGroup(self)
        layout_need_chaos_judge.addButton(layout_need_chaos_yes)
        layout_need_chaos_judge.addButton(layout_need_chaos_no)
        layout_need_chaos_cache = utils.read_status_value(utils.param_file_path, "need_chaos")
        if layout_need_chaos_cache:
            layout_need_chaos_yes.setChecked(True)
        else:
            layout_need_chaos_no.setChecked(True)
        layout_need_chaos_yes.toggled.connect(on_need_chaos_toggled)

        layout_need_chaos.addWidget(layout_need_chaos_title)
        layout_need_chaos.addWidget(layout_need_chaos_yes)
        layout_need_chaos.addWidget(layout_need_chaos_no)

        # param: "need_chaos_all_class"
        layout_need_chaos_all_class = QHBoxLayout()
        layout_need_chaos_all_class_title = QLabel()
        layout_need_chaos_all_class_title.setText("混沌地牢全职：")
        layout_need_chaos_all_class_yes = QRadioButton(f"是")
        layout_need_chaos_all_class_no = QRadioButton(f"否")
        layout_need_chaos_all_class_judge = QButtonGroup(self)
        layout_need_chaos_all_class_judge.addButton(layout_need_chaos_all_class_yes)
        layout_need_chaos_all_class_judge.addButton(layout_need_chaos_all_class_no)
        layout_need_chaos_all_class_cache = utils.read_status_value(utils.param_file_path, "need_chaos_all_class")
        if layout_need_chaos_all_class_cache:
            layout_need_chaos_all_class_yes.setChecked(True)
        else:
            layout_need_chaos_all_class_no.setChecked(True)
        layout_need_chaos_all_class_yes.toggled.connect(on_need_chaos_all_class_toggled)

        layout_need_chaos_all_class.addWidget(layout_need_chaos_all_class_title)
        layout_need_chaos_all_class.addWidget(layout_need_chaos_all_class_yes)
        layout_need_chaos_all_class.addWidget(layout_need_chaos_all_class_no)

        # param: "need_repair"
        layout_need_repair = QHBoxLayout()
        layout_need_repair_title = QLabel()
        layout_need_repair_title.setText("全部修理装备：")
        layout_need_repair_yes = QRadioButton(f"是")
        layout_need_repair_no = QRadioButton(f"否")
        layout_need_repair_judge = QButtonGroup(self)
        layout_need_repair_judge.addButton(layout_need_repair_yes)
        layout_need_repair_judge.addButton(layout_need_repair_no)
        layout_need_repair_cache = utils.read_status_value(utils.param_file_path, "need_repair")
        if layout_need_repair_cache:
            layout_need_repair_yes.setChecked(True)
        else:
            layout_need_repair_no.setChecked(True)
        layout_need_repair_yes.toggled.connect(on_need_repair_toggled)

        layout_need_repair.addWidget(layout_need_repair_title)
        layout_need_repair.addWidget(layout_need_repair_yes)
        layout_need_repair.addWidget(layout_need_repair_no)

        # param: "need_sort_bag"
        layout_need_sort_bag = QHBoxLayout()
        layout_need_sort_bag_title = QLabel()
        layout_need_sort_bag_title.setText("全部整理背包：")
        layout_need_sort_bag_yes = QRadioButton(f"是")
        layout_need_sort_bag_no = QRadioButton(f"否")
        layout_need_sort_bag_judge = QButtonGroup(self)
        layout_need_sort_bag_judge.addButton(layout_need_sort_bag_yes)
        layout_need_sort_bag_judge.addButton(layout_need_sort_bag_no)
        layout_need_sort_bag_cache = utils.read_status_value(utils.param_file_path, "need_sort_bag")
        if layout_need_sort_bag_cache:
            layout_need_sort_bag_yes.setChecked(True)
        else:
            layout_need_sort_bag_no.setChecked(True)
        layout_need_sort_bag_yes.toggled.connect(on_need_sort_bag_toggled)

        layout_need_sort_bag.addWidget(layout_need_sort_bag_title)
        layout_need_sort_bag.addWidget(layout_need_sort_bag_yes)
        layout_need_sort_bag.addWidget(layout_need_sort_bag_no)

        # param: "need_disenchant"
        layout_need_disenchant = QHBoxLayout()
        layout_need_disenchant_title = QLabel()
        layout_need_disenchant_title.setText("全部一键分解：")
        layout_need_disenchant_yes = QRadioButton(f"是")
        layout_need_disenchant_no = QRadioButton(f"否")
        layout_need_disenchant_judge = QButtonGroup(self)
        layout_need_disenchant_judge.addButton(layout_need_disenchant_yes)
        layout_need_disenchant_judge.addButton(layout_need_disenchant_no)
        layout_need_disenchant_cache = utils.read_status_value(utils.param_file_path, "need_disenchant")
        if layout_need_disenchant_cache:
            layout_need_disenchant_yes.setChecked(True)
        else:
            layout_need_disenchant_no.setChecked(True)
        layout_need_disenchant_yes.toggled.connect(on_need_disenchant_toggled)

        layout_need_disenchant.addWidget(layout_need_disenchant_title)
        layout_need_disenchant.addWidget(layout_need_disenchant_yes)
        layout_need_disenchant.addWidget(layout_need_disenchant_no)

        # param: "need_buy_potion"
        layout_need_buy_potion = QHBoxLayout()
        layout_need_buy_potion_title = QLabel()
        layout_need_buy_potion_title.setText("全部购买血药：")
        layout_need_buy_potion_yes = QRadioButton(f"是")
        layout_need_buy_potion_no = QRadioButton(f"否")
        layout_need_buy_potion_judge = QButtonGroup(self)
        layout_need_buy_potion_judge.addButton(layout_need_buy_potion_yes)
        layout_need_buy_potion_judge.addButton(layout_need_buy_potion_no)
        layout_need_buy_potion_cache = utils.read_status_value(utils.param_file_path, "need_buy_potion")
        if layout_need_buy_potion_cache:
            layout_need_buy_potion_yes.setChecked(True)
        else:
            layout_need_buy_potion_no.setChecked(True)
        layout_need_buy_potion_yes.toggled.connect(on_need_buy_potion_toggled)

        layout_need_buy_potion.addWidget(layout_need_buy_potion_title)
        layout_need_buy_potion.addWidget(layout_need_buy_potion_yes)
        layout_need_buy_potion.addWidget(layout_need_buy_potion_no)

        # param: "need_desire"
        layout_need_desire = QHBoxLayout()
        layout_need_desire_title = QLabel()
        layout_need_desire_title.setText("渴望岛岛之心：")
        layout_need_desire_yes = QRadioButton(f"是")
        layout_need_desire_no = QRadioButton(f"否")
        layout_need_desire_judge = QButtonGroup(self)
        layout_need_desire_judge.addButton(layout_need_desire_yes)
        layout_need_desire_judge.addButton(layout_need_desire_no)
        layout_need_desire_cache = utils.read_status_value(utils.param_file_path, "need_desire")
        if layout_need_desire_cache:
            layout_need_desire_yes.setChecked(True)
        else:
            layout_need_desire_no.setChecked(True)
        layout_need_desire_yes.toggled.connect(on_need_desire_toggled)

        layout_need_desire.addWidget(layout_need_desire_title)
        layout_need_desire.addWidget(layout_need_desire_yes)
        layout_need_desire.addWidget(layout_need_desire_no)

        # param: "need_2K_coor_fix"
        layout_need_2K_coor_fix = QHBoxLayout()
        layout_need_2K_coor_fix_title = QLabel()
        layout_need_2K_coor_fix_title.setText("低分辨率补偿：")
        layout_need_2K_coor_fix_yes = QRadioButton(f"是")
        layout_need_2K_coor_fix_no = QRadioButton(f"否")
        layout_need_2K_coor_fix_judge = QButtonGroup(self)
        layout_need_2K_coor_fix_judge.addButton(layout_need_2K_coor_fix_yes)
        layout_need_2K_coor_fix_judge.addButton(layout_need_2K_coor_fix_no)
        layout_need_2K_coor_fix_cache = utils.read_status_value(utils.param_file_path, "need_2K_coor_fix")
        if layout_need_2K_coor_fix_cache:
            layout_need_2K_coor_fix_yes.setChecked(True)
        else:
            layout_need_2K_coor_fix_no.setChecked(True)
        layout_need_2K_coor_fix_yes.toggled.connect(on_need_2K_coor_fix_toggled)

        layout_need_2K_coor_fix.addWidget(layout_need_2K_coor_fix_title)
        layout_need_2K_coor_fix.addWidget(layout_need_2K_coor_fix_yes)
        layout_need_2K_coor_fix.addWidget(layout_need_2K_coor_fix_no)

        # Whole layout
        layout.addLayout(layout_start_charac)
        layout.addLayout(layout_need_loop)
        layout.addLayout(layout_need_chaos)
        layout.addLayout(layout_need_chaos_all_class)
        layout.addLayout(layout_need_repair)
        layout.addLayout(layout_need_sort_bag)
        layout.addLayout(layout_need_disenchant)
        layout.addLayout(layout_need_buy_potion)
        layout.addLayout(layout_need_desire)
        layout.addLayout(layout_need_2K_coor_fix)

        layout.addWidget(self.log_text_tool)
        layout.addWidget(start_button)
        layout.addWidget(stop_button)

        tab.setLayout(layout)
        return tab

    def redirect_logging(self, text_edit):
        logging.basicConfig(
            stream=sys.stdout,
            level=logging.INFO,
            format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        logger = logging.getLogger()
        logHandler = PyLogHandler(text_edit)
        logger.addHandler(logHandler)

    def startToolThread(self):
        self.toolThread = ToolThread()
        self.toolThread.start()

    def stopToolThread(self):
        if self.toolThread:
            self._async_raise(self.toolThread.ident, SystemExit)

    def _async_raise(self, tid, exctype):
        """Raises an exception in the threads with id tid"""
        if not inspect.isclass(exctype):
            raise TypeError("Only types can be raised (not instances)")
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

# test snippet
    def create_tab_daily(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.log_text_daily = QTextEdit()
        self.log_text_daily.setReadOnly(True)
        self.log_text_daily.setStyleSheet("background-color: black; color: white;")

        start_button = QPushButton("开始")
        stop_button = QPushButton("结束")

        start_button.clicked.connect(self.start_logging_daily)
        stop_button.clicked.connect(self.stop_logging_daily)

        layout.addWidget(self.log_text_daily)
        layout.addWidget(start_button)
        layout.addWidget(stop_button)

        tab.setLayout(layout)
        return tab

    def create_tab_weekly(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.log_text_weekly = QTextEdit()
        self.log_text_weekly.setReadOnly(True)
        self.log_text_weekly.setStyleSheet("background-color: black; color: white;")

        start_button = QPushButton("开始")
        stop_button = QPushButton("结束")

        start_button.clicked.connect(self.start_logging_weekly)
        stop_button.clicked.connect(self.stop_logging_weekly)

        layout.addWidget(self.log_text_weekly)
        layout.addWidget(start_button)
        layout.addWidget(stop_button)

        tab.setLayout(layout)
        return tab

    def start_logging_daily(self):
        if self.daily_thread is None or not self.daily_thread.is_alive():
            self.daily_thread = LogThread(self.log_text_daily)
            self.daily_thread.start()

    def start_logging_weekly(self):
        if self.weekly_thread is None or not self.weekly_thread.is_alive():
            self.weekly_thread = LogThread(self.log_text_weekly)
            self.weekly_thread.start()

    def stop_logging_daily(self):
        if self.daily_thread:
            self.daily_thread.stop()
            self.daily_thread = None

    def stop_logging_weekly(self):
        if self.weekly_thread:
            self.weekly_thread.stop()
            self.weekly_thread = None


def on_need_loop_toggled(checked):
    utils.update_status_value(utils.param_file_path, "need_loop", checked)

def on_need_chaos_toggled(checked):
    utils.update_status_value(utils.param_file_path, "need_chaos", checked)

def on_need_chaos_all_class_toggled(checked):
    utils.update_status_value(utils.param_file_path, "need_chaos_all_class", checked)

def on_need_repair_toggled(checked):
    utils.update_status_value(utils.param_file_path, "need_repair", checked)

def on_need_sort_bag_toggled(checked):
    utils.update_status_value(utils.param_file_path, "need_sort_bag", checked)

def on_need_disenchant_toggled(checked):
    utils.update_status_value(utils.param_file_path, "need_disenchant", checked)

def on_need_buy_potion_toggled(checked):
    utils.update_status_value(utils.param_file_path, "need_buy_potion", checked)

def on_need_desire_toggled(checked):
    utils.update_status_value(utils.param_file_path, "need_desire", checked)

def on_need_2K_coor_fix_toggled(checked):
    utils.update_status_value(utils.param_file_path, "need_2K_coor_fix", checked)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())