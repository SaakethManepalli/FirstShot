from PySide6.QtWidgets import QWidget
from PySide6 import QtWidgets
from PySide6.QtCore import QThread, QObject
from ui_widget import Ui_Widget, MplCanvas
from win32api import GetKeyState
from LeftClickSS import take_screenshot
import time
import json
import server


class ScreenshotThread(QObject):
    def __init__(self, ctrl):
        QObject.__init__(self)
        self.ctrl = ctrl

    def run(self):
        self.ctrl['break'] = True
        start = 0

        while True:
            while not self.ctrl['break']:
                leftClick = GetKeyState(0x01)
                if leftClick < 0:
                    if time.time() - start > .3:
                        take_screenshot()
                    start = time.time()
                time.sleep(.001)


class Widget(QWidget, Ui_Widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("FirstShot")
        self.pushButton.clicked.connect(self.gen_results)
        self.pushButton_2.clicked.connect(self.view_results)

        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidget.itemClicked.connect(self.select_files)

        self.thread = QThread()
        self.ctrl = {'break': False}
        self.worker = ScreenshotThread(self.ctrl)
        self.start()

        self.checkBox.stateChanged.connect(self.toggle_ss)

    def gen_results(self):
        self.checkBox.setChecked(0)

    def view_results(self):
        x, y = server.getcoords()

        chart = MplCanvas(self, x, y)
        self.verticalLayout.addWidget(chart)

    def select_files(self):
        items = self.listWidget.selectedItems()
        global selected_names
        selected_names = []
        for i in range(len(items)):
            selected_names.append(str(self.listWidget.selectedItems()[i].text()))

    def toggle_ss(self):
        if self.checkBox.isChecked():
            self.ctrl['break'] = False
            print("checkBox is checked")
        else:
            self.ctrl['break'] = True
            print("checkBox is not checked")

    def start(self):
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.start()