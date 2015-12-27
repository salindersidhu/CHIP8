from PyQt4 import QtGui, QtCore


class GridFrame(QtGui.QFrame):
    '''GridFrame extends the QtGui.QFrame class. It is used to draw a custom
    grid of pixels to the screen. The pixels are specified in a 2D list where
    the active pixels are denoted by 1 and drawn in a specific colour while
    pixels denoted by 0 are drawn as the background with another colour.'''

    def __init__(self, parentWindow, width, height, pxSize, defaultbgColour,
                 defaultpxColour):
        '''Create a new GridFrame with a specific width, height, pixel size and
        default colours used to draw the pixels and background.'''
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
        '''Set the values of the pixels in the grid to the grid specified and
        update the screen to reflect the change.'''
        self.__grid = [row[:] for row in grid]
        self.update()

    def clearPixels(self):
        '''Set all the values for the pixels in the grid to 0 and update the
        screen to reflect the change.'''
        self.__grid = [[0 for _ in range(self.__gHeight)]
                       for _ in range(self.__gWidth)]
        self.update()

    def changePixelColour(self, pxColour):
        '''Set the new value of the pixel colour to pxColour.'''
        self.__pxColour = pxColour

    def changeBackgroundColour(self, bgColour):
        '''Set the new value of the background colour to bgColour.'''
        self.__bgColour = bgColour

    def getPixelColour(self):
        '''Return the current value of the pixel colour.'''
        return self.__pxColour

    def getBackgroundColour(self):
        '''Return the current value of the background colour.'''
        return self.__bgColour

    def paintEvent(self, event):
        '''Handle and process all of the drawing for the grid. Each pixel is
        drawn using pixel colour and the background is drawn wherever the pixel
        value is 0 using background colour.'''
        painter = QtGui.QPainter(self)  # Used to draw on the frame
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
