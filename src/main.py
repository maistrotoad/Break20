"""
 * Copyright (C) 2020 Michiel Gielen - All Rights Reserved
 *
 * Authors:
 * Michiel Gielen, https://github.com/maistrotoad
"""

import sys

from PyQt5.QtGui import QSurfaceFormat
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QEvent, QRect, Qt

from mainText import MainText
from matrix import Matrix


class Break20(QWidget):
    def __init__(self, screenGeometry: QRect):
        super().__init__()

        surfaceFormat = QSurfaceFormat()
        surfaceFormat.setSamples(4)

        mainText = MainText()
        mainText.setParent(self)
        mainText.setGeometry(screenGeometry)
        mainText.anim()

        matrices = [Matrix(screenGeometry=screenGeometry) for _ in range(50)]

        for matrix in matrices:
            matrix.setParent(self)
            matrix.anim()

        self.setStyleSheet("background:transparent")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showFullScreen()

    def keyPressEvent(self, event: QEvent):
        if event.key() == Qt.Key_Escape:
            sys.exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    screen = app.primaryScreen()

    window = Break20(screenGeometry=screen.geometry())
    sys.exit(app.exec_())
