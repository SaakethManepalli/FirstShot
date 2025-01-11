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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(394, 122)
        self.verticalLayout_2 = QVBoxLayout(Widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"Old English Text MT"])
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout.addWidget(self.label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ss_chkbox = QCheckBox(Widget)
        self.ss_chkbox.setObjectName(u"ss_chkbox")
        font1 = QFont()
        font1.setFamilies([u"Perpetua"])
        font1.setBold(True)
        self.ss_chkbox.setFont(font1)

        self.horizontalLayout.addWidget(self.ss_chkbox)

        self.generate_button = QPushButton(Widget)
        self.generate_button.setObjectName(u"generate_button")
        self.generate_button.setFont(font1)

        self.horizontalLayout.addWidget(self.generate_button)

        self.view_button = QPushButton(Widget)
        self.view_button.setObjectName(u"view_button")
        self.view_button.setFont(font1)

        self.horizontalLayout.addWidget(self.view_button)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Form", None))
        self.label.setText(QCoreApplication.translate("Widget", u"FirstShot", None))
        self.ss_chkbox.setText(QCoreApplication.translate("Widget", u"Enable/Disable Screenshotting", None))
        self.generate_button.setText(QCoreApplication.translate("Widget", u"Generate Results", None))
        self.view_button.setText(QCoreApplication.translate("Widget", u"View Results", None))
    # retranslateUi