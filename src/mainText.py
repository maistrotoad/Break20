"""
 * Copyright (C) 2020 Michiel Gielen - All Rights Reserved
 *
 * Authors:
 * Michiel Gielen, https://github.com/maistrotoad
"""


import sys
from PyQt5.QtGui import QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QEvent, QPropertyAnimation, Qt, pyqtProperty


class MainText(QWidget):
    def __init__(self):
        super().__init__()
        self._fontOpacity = 255

        self.mainText = "Stare out of the window for the next 20 seconds..."

    def paintEvent(self, e: QEvent):
        qp = QPainter()

        qp.begin(self)
        self.render(qp)
        qp.end()

    def render(self, qp: QPainter):
        mainFont = QFont()
        mainFont.setPixelSize(32)

        mainPen = QPen(QColor(0, 200, 0, self.fontOpacity), 2, Qt.SolidLine)

        qp.setFont(mainFont)
        qp.setPen(mainPen)

        qp.drawText(
            int(self.width() * 0.3),
            int(self.height() * 0.5),
            self.mainText,
        )

    def anim(self):
        self.a = QPropertyAnimation(self, b"fontOpacity")
        self.a.setDuration(20000)
        self.a.setStartValue(255)
        self.a.setEndValue(0)
        self.a.start()
        self.a.finished.connect(self.exit)

    def exit(self):
        sys.exit(0)

    @pyqtProperty(int)
    def fontOpacity(self):
        return self._fontOpacity

    @fontOpacity.setter
    def fontOpacity(self, value):
        self._fontOpacity = value
