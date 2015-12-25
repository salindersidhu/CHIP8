from PyQt4 import QtGui

class GUICanvas(QtGui.QFrame):
    ''''''
    
    def __init__(self, parent):
        ''''''
        super(GUICanvas, self).__init__(parent)
        # Canvas GUI variables
        self.__grid = []
        self.__pxSize = 0
        self.__gridWidth = 0
        self.__gridHeight = 0

    def setGrid(self, width, height, pxSize):
        ''''''
        self.__grid = [[0 for _ in range(height)] for _ in range(width)]
        self.__pxSize = pxSize
        self.__gridWidth = width
        self.__gridHeight = height

    def updateGrid(self, grid):
        ''''''
        self.__grid = [row[:] for row in grid]
        self.update()

    def clearGrid(self):
        ''''''
        self.__grid = [[0 for _ in range(self.__gridHeight)] \
                       for _ in range(self.__gridWidth)]
        self.update()

    def paintEvent(self, event):
        ''''''
        painter = QtGui.QPainter(self)
        #
        painter.eraseRect(0, 0, self.width(), self.height())
        #
        for y in range(self.__gridHeight):
            for x in range(self.__gridWidth):
                if self.__grid[x][y]:
                    color = QtGui.QColor(0, 84, 180)
                else:
                    color = QtGui.QColor(0, 0, 0)
                painter.fillRect(x * self.__pxSize, y * self.__pxSize,
                                 self.__pxSize, self.__pxSize, color)
