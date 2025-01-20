# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import numpy as np
from scipy.stats import gaussian_kde



class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent, x, y):
        fig = plt.figure(figsize=(4,6))
        ax = fig.add_subplot(212)
        super().__init__(fig)
        self.setParent(parent)

        k = gaussian_kde(np.vstack([x, y]))
        xi, yi = np.mgrid[min(x):max(x):len(x) ** 0.5 * 1j, min(y):max(y):len(y) ** 0.5 * 1j]
        zi = k(np.vstack([xi.flatten(), yi.flatten()]))

        ax.contourf(xi, yi, zi.reshape(xi.shape), alpha=0.5)
        ax.set_xlim(-510, 510)
        ax.set_ylim(-960, 960)

        ax.set_xlabel('X Distance From Head (Pixels)')
        ax.set_ylabel('Y Distance From Head (Pixels)')
        ax.set_title("Accuracy")

        ax.plot(extent=[min(x), max(x), min(y), max(y)], aspect='auto')


class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 800)
        self.gridLayout = QGridLayout(Widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.checkBox = QCheckBox(Widget)
        self.checkBox.setObjectName(u"checkBox")
        QFontDatabase.addApplicationFont("Tektur-VariableFont_wdth,wght.ttf")
        font = QFont()
        font.setFamilies([u"Tektur"])
        font.setPointSize(12)
        self.checkBox.setFont(font)

        self.verticalLayout_2.addWidget(self.checkBox, 0, Qt.AlignmentFlag.AlignHCenter)

        self.pushButton = QPushButton(Widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setFont(font)

        self.verticalLayout_2.addWidget(self.pushButton)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.pushButton_2 = QPushButton(Widget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setFont(font)

        self.verticalLayout.addWidget(self.pushButton_2)

        self.listWidget = QListWidget(Widget)
        self.listWidget.setObjectName(u"listWidget")
        font1 = QFont()
        font1.setFamilies([u"Tektur"])
        self.listWidget.setFont(font1)

        self.verticalLayout.addWidget(self.listWidget)


        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")
        font2 = QFont()
        font2.setFamilies([u"Tektur"])
        font2.setPointSize(36)
        font2.setBold(True)
        self.label.setFont(font2)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Form", None))
        self.checkBox.setText(QCoreApplication.translate("Widget", u"Enable/Disable Screenshotting", None))
        self.pushButton.setText(QCoreApplication.translate("Widget", u"Generate Results", None))
        self.pushButton_2.setText(QCoreApplication.translate("Widget", u"View Results", None))
        self.label.setText(QCoreApplication.translate("Widget", u"FirstShot", None))
    # retranslateUi