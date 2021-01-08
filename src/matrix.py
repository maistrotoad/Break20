"""
 * Copyright (C) 2020 Michiel Gielen - All Rights Reserved
 *
 * Authors:
 * Michiel Gielen, https://github.com/maistrotoad
"""

from random import randint, choice
import sys

from PyQt5.QtGui import QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QEvent, QPoint, QPropertyAnimation, QRect

includeRanges = (
    (0x0021, 0x0021),
    (0x0023, 0x0026),
    (0x0028, 0x007E),
    (0x00A1, 0x00AC),
    (0x00AE, 0x00FF),
    (0x0100, 0x017F),
    (0x0180, 0x024F),
    (0x2C60, 0x2C7F),
    (0x16A0, 0x16F0),
    (0x0370, 0x0377),
    (0x037A, 0x037E),
    (0x0384, 0x038A),
    (0x038C, 0x038C),
)

alphabet = [
    chr(codePoint)
    for currentRange in includeRanges
    for codePoint in range(currentRange[0], currentRange[1] + 1)
]


class Matrix(QWidget):
    def __init__(self, screenGeometry: QRect):
        super().__init__()

        self.setGeometry(screenGeometry)

        self.fontSize = randint(8, 48)

        self.mainFont = QFont()
        self.mainFont.setPixelSize(self.fontSize)

        self.qp = QPainter()

        self.initState()

    def initState(self):
        self.chars = [choice(alphabet) for _ in range(randint(3, 8))]
        self.xPos = randint(0, self.width())

    def paintEvent(self, e: QEvent):
        self.qp.begin(self)

        self.qp.setFont(self.mainFont)

        self.render(self.qp)
        self.qp.end()

    def render(self, qp: QPainter):
        for i, c in enumerate(self.chars):
            matrixColor = QColor()
            matrixColor.setHsl(110, 255, 50 + i * randint(15, 25), 5 * self.fontSize)
            matrixPen = QPen(matrixColor)
            self.qp.setPen(matrixPen)
            qp.drawText(self.xPos, i * self.fontSize, c)

    def anim(self):
        sizeScale = int(20000 / self.fontSize)
        total = 10000 + randint(sizeScale, sizeScale * 3)
        self.a = QPropertyAnimation(self, b"pos")
        self.a.setDuration(total)
        self.a.setStartValue(
            QPoint(0, -self.height() - len(self.chars) * self.fontSize)
        )
        self.a.setEndValue(QPoint(0, self.height()))
        self.a.start()
        self.a.setCurrentTime(randint(0, int(total * 0.5)))
        self.a.finished.connect(self.restart)

    def restart(self):
        self.initState()
        self.anim()