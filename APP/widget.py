from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QThread, QObject
from ui_widget import Ui_Widget
from APP import LeftClickSS


class ScreenshotThread(QObject):
    def __init__(self, ctrl):
        QObject.__init__(self)
        self.ctrl = ctrl

    def run(self):
        self.ctrl['break'] = False
        start = 0

        while True:
            start = LeftClickSS.begin_ss(start)
            if self.ctrl['break']:
                break

class Widget(QWidget, Ui_Widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("FirstShot")
        self.generate_button.clicked.connect(self.gen_results)

        self.thread = QThread()
        self.ctrl = {'break': False}
        self.worker = ScreenshotThread(self.ctrl)
        self.ss_chkbox.stateChanged.connect(self.toggle_ss)

    def gen_results(self):
        self.ss_chkbox.setChecked(0)

    def toggle_ss(self):
        if self.ss_chkbox.checkState().Checked:
            self.start()
        else:
            self.ctrl['break'] = True

    def start(self):
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.start()
