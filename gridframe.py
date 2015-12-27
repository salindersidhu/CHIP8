from PyQt4 import QtGui, QtCore

class GridFrame(QtGui.QFrame):
    ''''''

    def __init__(self, parentWindow, width, height, pxSize, defaultbgColour,
                 defaultpxColour):
        ''''''
        super(GridFrame, self).__init__(parentWindow)
        # Grid frame variables
        self.__grid = [[0 for _ in range(height)] for _ in range(width)]
        self.__pxSize = pxSize
        self.__gWidth = width
        self.__gHeight = height
        # Default pixel and background colours
        self.__pxColour = defaultpxColour
        self.__bgColour = defaultbgColour
        # Set strong policy for focusing keyboard events to GridFrame
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def updatePixels(self, grid):
        ''''''
        self.__grid = [row[:] for row in grid]
        self.update()

    def clearPixels(self):
        ''''''
        self.__grid = [[0 for _ in range(self.__gHeight)] \
                       for _ in range(self.__gWidth)]
        self.update()

    def changePixelColour(self, pxColour):
        ''''''
        self.__pxColour = pxColour

    def changeBackgroundColour(self, bgColour):
        ''''''
        self.__bgColour = bgColour

    def getPixelColour(self):
        ''''''
        return self.__pxColour

    def getBackgroundColour(self):
        ''''''
        return self.__bgColour

    def paintEvent(self, event):
        ''''''
        painter = QtGui.QPainter(self)
        # Clear all drawings on the GridFrame
        painter.eraseRect(0, 0, self.width(), self.height())
        # Draw the pixels on the GridFrame
        for y in range(self.__gHeight):
            for x in range(self.__gWidth):
                if self.__grid[x][y]:
                    color = QtGui.QColor(self.__pxColour[0],
                                         self.__pxColour[1],
                                         self.__pxColour[2])
                else:
                    color = QtGui.QColor(self.__bgColour[0],
                                         self.__bgColour[1],
                                         self.__bgColour[2])
                painter.fillRect(x * self.__pxSize, y * self.__pxSize,
                                 self.__pxSize, self.__pxSize, color)
