import sys

import numpy as np
import OpenGL.GL as gl
import freetype as ft

from PyQt5 import QtCore, QtWidgets, QtOpenGL
from pathlib import Path
from random import choice, randint, random

transparent = (0, 0, 0, 0)

chrRanges = (
    (32, 33),
    (36, 38),
    (42, 44),
    (48, 91),
    (97, 123),
    (161, 172),
    (174, 452),
    (461, 497),
    (500, 680),
    (931, 1000),
    (1200, 1328),
    (1330, 1367),
    (1378, 1416),
)  # ,(11360,11391),(5792,5872),(880,887),(890,894),(900,906),(908,908))

alphabet = [chr(n) for chrRange in chrRanges for n in range(*chrRange)]

alphabetRange = range(len(alphabet))


def randLetter():
    return choice(alphabetRange)


def getLayer(width, height):
    chars = [randLetter() for _ in range(randint(5, 13))]

    return {"chars": chars, "x": random() * width, "y": height}


class GlWidget(QtWidgets.QOpenGLWidget):
    def __init__(self, parent, geometry):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.setGeometry(geometry)
        self.base = 0
        self.textureId = 0
        self.xPos = 10
        self.yPos = self.height() - 10

        self.topLayers = [getLayer(self.width(), self.height()) for _ in range(20)]

    def paintGL(self):
        gl.glClearColor(*transparent)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textureId)

        for layer in self.topLayers:
            gl.glPushMatrix()
            gl.glTranslate(layer["x"], layer["y"], 0)
            gl.glPushMatrix()
            gl.glListBase(self.base)
            green = (0, 0.5, 0, 0.5)
            gl.glColor(*green)
            gl.glCallLists(layer["chars"][2:])
            wobble = random() * 0.7
            brightGreen = (wobble, 1, wobble, 0.5)
            gl.glColor(*brightGreen)
            if layer["chars"][1] == 0 and random() > 0.7:
                layer["chars"][1] = randLetter()
            elif random() > 0.99:
                layer["chars"][1] = 0 if random() > 0.1 else randLetter()

            gl.glCallLists(layer["chars"][:2])
            gl.glPopMatrix()
            gl.glPopMatrix()
            layer["y"] = layer["y"] - 0.5

            self.update()

    def initializeGL(self):
        gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_MODULATE)
        # gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_BLEND)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_TEXTURE_2D)
        self.makefont()

    def resizeGL(self, width, height):
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, width, 0, height, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

    def makefont(self, filename=f"{Path(__file__).parent}/EversonMono.ttf", size=32):
        # Load font  and check it is monotype
        face = ft.Face(filename)
        face.set_char_size(size * 64)

        # Determine largest glyph size
        width, height, ascender, descender = 0, 0, 0, 0
        for letter in alphabet:
            face.load_char(letter, ft.FT_LOAD_RENDER | ft.FT_LOAD_FORCE_AUTOHINT)
            bitmap = face.glyph.bitmap
            width = max(width, bitmap.width)
            ascender = max(ascender, face.glyph.bitmap_top)
            descender = max(descender, bitmap.rows - face.glyph.bitmap_top)
        height = ascender + descender

        # Generate texture data
        matrixRows = 23
        matrixColumns = 37
        Z = np.zeros((height * matrixRows, width * matrixColumns), dtype=np.ubyte)
        for row in range(matrixRows):
            for i in range(matrixColumns):
                charNo = row * matrixColumns + i
                face.load_char(alphabet[charNo], ft.FT_LOAD_RENDER | ft.FT_LOAD_FORCE_AUTOHINT)
                bitmap = face.glyph.bitmap
                x = i * width + face.glyph.bitmap_left
                y = row * height + ascender - face.glyph.bitmap_top
                Z[y : y + bitmap.rows, x : x + bitmap.width].flat = bitmap.buffer

        # Bound texture
        self.textureId = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textureId)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexImage2D(
            gl.GL_TEXTURE_2D,
            0,
            gl.GL_ALPHA,
            Z.shape[1],
            Z.shape[0],
            0,
            gl.GL_ALPHA,
            gl.GL_UNSIGNED_BYTE,
            Z,
        )

        # Generate display lists
        dx, dy = width / float(Z.shape[1]), height / float(Z.shape[0])
        self.base = gl.glGenLists(matrixRows * matrixColumns)

        for i in range(matrixRows * matrixColumns):
            letter = alphabet[i]
            x = i % matrixColumns
            y = i // matrixColumns

            gl.glNewList(self.base + i, gl.GL_COMPILE)
            gl.glBegin(gl.GL_QUADS)
            gl.glTexCoord2f((x) * dx, (y + 1) * dy), gl.glVertex(0, -height)
            gl.glTexCoord2f((x) * dx, (y) * dy), gl.glVertex(0, 0)
            gl.glTexCoord2f((x + 1) * dx, (y) * dy), gl.glVertex(width, 0)
            gl.glTexCoord2f((x + 1) * dx, (y + 1) * dy), gl.glVertex(width, -height)
            gl.glEnd()
            gl.glTranslatef(0, -height, 0)
            gl.glEndList()


class Break20(QtWidgets.QWidget):
    def __init__(self, screenGeometry: QtCore.QRect):
        super().__init__()

        GlWidget(self, screenGeometry)

        self.setStyleSheet("background:transparent")
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.showFullScreen()

    def keyPressEvent(self, event: QtCore.QEvent):
        if event.key() == QtCore.Qt.Key_Escape:
            sys.exit(0)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    screen = app.primaryScreen()

    window = Break20(screenGeometry=screen.geometry())
    sys.exit(app.exec_())