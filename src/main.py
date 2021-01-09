"""
 * Copyright (C) 2020 Michiel Gielen - All Rights Reserved
 *
 * Authors:
 * Michiel Gielen, https://github.com/maistrotoad
"""

import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QEvent, QRect, Qt

from mainText import MainText
from matrixGl import MatrixGl


class Break20(QWidget):
    def __init__(self, screenGeometry: QRect):
        super().__init__()

        MatrixGl(self, screenGeometry)
        MainText(self, screenGeometry)

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
