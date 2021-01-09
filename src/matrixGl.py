import sys

import numpy as np
import OpenGL.GL as gl
import freetype as ft

from PyQt5 import QtCore, QtWidgets, QtOpenGL
from pathlib import Path
from random import choice, randint, random

chrRanges = (
    (32, 33),
    (36, 38),
    (42, 44),
    (48, 91),
    (161, 172),
    (174, 224),
    (256, 306, 2),
    (412, 414),
    (415, 417),
    (1200, 1208, 2),
    (1217, 1229, 2),
    (1329, 1367),
    (1378, 1416),
)

alphabet = [chr(n) for chrRange in chrRanges for n in range(*chrRange)]

alphabetRange = range(len(alphabet))

topGreens = [((1 - i / 11) * 0.6, 0.8, (1 - i / 11) * 0.6, 1 - i / 11) for i in range(12)]
bottomGreens = [((1 - i / 11) * 0.6, 0.8, (1 - i / 11) * 0.6, (1 - i / 11) * 0.2) for i in range(12)]


def randLetter():
    return choice(alphabetRange)


class MatrixGl(QtWidgets.QOpenGLWidget):
    def __init__(self, parent, geometry):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.setGeometry(geometry)
        self.topFont = {"base": 0, "textureId": 0}
        self.bottomFont = {"base": 0, "textureId": 0}
        self.xPos = 10
        self.yPos = self.height() - 10

        self.topLayers = [self.getTopLayer()]
        self.maxTopLayers = 50
        self.bottomLayers = [self.getTopLayer()]
        self.maxBottomLayers = 10

    def getTopLayer(self):
        chars = [randLetter() for _ in range(randint(5, 13))]

        x = random() * self.width()
        y = self.height() + 13 * 32 + random() * 50

        return {"chars": chars, "x": x, "y": y, "speed": random() * 5 + 8}

    def getBottomLayer(self):
        chars = [randLetter() for _ in range(randint(5, 13))]

        x = random() * self.width()
        y = self.height() + 13 * 32 + random() * 50

        return {"chars": chars, "x": x, "y": y, "speed": random() * 2 + 3}

    def paintGL(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.topFont["textureId"])

        nTopLayers = len(self.topLayers)
        if nTopLayers < self.maxTopLayers:
            addLayer = (self.maxTopLayers - nTopLayers) / self.maxTopLayers
            if random() > 0.6 + addLayer * 0.4:
                self.topLayers.append(self.getTopLayer())

        for n in range(len(self.topLayers)):
            layer = self.topLayers[n]

            self.renderTopLayer(layer)

            if layer["y"] < 0:
                self.topLayers[n] = self.getTopLayer()

        gl.glBindTexture(gl.GL_TEXTURE_2D, self.bottomFont["textureId"])

        nBottomLayers = len(self.bottomLayers)
        if nBottomLayers < self.maxBottomLayers:
            addLayer = (self.maxBottomLayers - nBottomLayers) / self.maxBottomLayers
            if random() > 0.6 + addLayer * 0.4:
                self.bottomLayers.append(self.getBottomLayer())

        for n in range(len(self.bottomLayers)):
            layer = self.bottomLayers[n]

            self.renderBottomLayer(layer)

            if layer["y"] < 0:
                self.bottomLayers[n] = self.getBottomLayer()

        self.update()

    def renderTopLayer(self, layer):
        gl.glPushMatrix()
        gl.glTranslate(layer["x"], layer["y"], 0)
        gl.glListBase(self.topFont["base"])

        firstChars = layer["chars"][1:]
        for i, char in enumerate(firstChars):
            n = len(firstChars) - i - 1
            gl.glColor(*topGreens[n])
            gl.glCallLists(char)

        wobble = random() * 0.5
        brightGreen = (0.4 + wobble, 1, 0.4 + wobble, 1)
        gl.glColor(*brightGreen)
        if layer["chars"][0] == 0 and random() > 0.7:
            layer["chars"][0] = randLetter()
        elif random() > 0.99:
            layer["chars"][0] = 0 if random() > 0.1 else randLetter()

        gl.glCallLists(layer["chars"][0])
        gl.glPopMatrix()
        layer["y"] = layer["y"] - layer["speed"]

    def renderBottomLayer(self, layer):
        if layer["chars"][0] == 0 and random() > 0.75:
            layer["chars"][0] = randLetter()
        elif random() > 0.99:
            layer["chars"][0] = 0 if random() > 0.1 else randLetter()

        for x in range(2):
            for y in range(2):
                gl.glPushMatrix()
                gl.glTranslate(layer["x"] + x * 2, layer["y"] + y * 2, 0)
                gl.glListBase(self.bottomFont["base"])

                firstChars = layer["chars"][1:]
                for i, char in enumerate(firstChars):
                    n = len(firstChars) - i - 1
                    gl.glColor(*bottomGreens[n])
                    gl.glCallLists(char)

                wobble = random() * 0.5
                brightGreen = (0.4 + wobble, 1, 0.4 + wobble, 0.2)
                gl.glColor(*brightGreen)
                gl.glCallLists(layer["chars"][0])
                gl.glPopMatrix()

        layer["y"] = layer["y"] - layer["speed"]

    def initializeGL(self):
        gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_MODULATE)
        gl.glEnable(gl.GL_BLEND)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_TEXTURE_2D)
        self.makefont(fontDict=self.topFont)
        self.makefont(fontDict=self.bottomFont, size=12)

    def resizeGL(self, width, height):
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, width, 0, height, -100, 100)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

    def makefont(self, fontDict, size=32, filename=f"{Path(__file__).parent}/FreeSerif.ttf"):
        # Load font
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
        matrixRows = 14
        matrixColumns = 16
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
        fontDict["textureId"] = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, fontDict["textureId"])
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
        fontDict["base"] = gl.glGenLists(matrixRows * matrixColumns)

        for i in range(matrixRows * matrixColumns):
            letter = alphabet[i]
            x = i % matrixColumns
            y = i // matrixColumns

            gl.glNewList(fontDict["base"] + i, gl.GL_COMPILE)
            gl.glBegin(gl.GL_QUADS)
            gl.glTexCoord2f((x) * dx, (y + 1) * dy), gl.glVertex(0, -height)
            gl.glTexCoord2f((x) * dx, (y) * dy), gl.glVertex(0, 0)
            gl.glTexCoord2f((x + 1) * dx, (y) * dy), gl.glVertex(width, 0)
            gl.glTexCoord2f((x + 1) * dx, (y + 1) * dy), gl.glVertex(width, -height)
            gl.glEnd()
            gl.glTranslatef(0, -0.8 * height, 0)
            gl.glEndList()
