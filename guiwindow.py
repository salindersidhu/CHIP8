from PyQt4 import QtGui, QtCore
from guicanvas import GUICanvas

class GUIWindow(QtGui.QMainWindow):
    ''''''

    def __init__(self, winTitle, winWidth, winHeight, winIcon):
        ''''''
        super(GUIWindow, self).__init__()
        # Window GUI variables
        self.__menubar = self.menuBar()     # Define a Menu Bar
        self.__menuDict = {}                # Define a map of Menus
        self.__canvas = GUICanvas(self)     # Define a drawing canvas
        self.__statusLabel = QtGui.QLabel() # Define a new status label
        self.__keyInputDict = {}            # Define a map of key events
        # Configure the window's properties
        self.setGeometry(0, 0, winWidth, winHeight)
        self.setFixedSize(winWidth, winHeight)
        self.setWindowTitle(winTitle)
        self.setWindowIcon(QtGui.QIcon(winIcon))
        # Bind the QLabel to the Status Bar
        self.statusBar().addWidget(self.__statusLabel, 1)
        # Bind the GUI drawing canvas to the GUI window
        self.setCentralWidget(self.__canvas)
        # Set the window to appear in the center of the screen
        self.centerOnScreen()
        # Configure the remaining GUI elements for the window

    def centerOnScreen(self):
        ''''''
        res = QtGui.QDesktopWidget().screenGeometry()
        move_width = (res.width() / 2) - (self.frameSize().width() / 2)
        move_height = (res.height() / 2) - (self.frameSize().height() / 2)
        self.move(move_width, move_height)

    def updateKeyBindings(self, keyBindings):
        ''''''
        self.__keyInputDict = keyBindings.copy()

    def keyPressEvent(self, event):
        ''''''
        eventKey = event.key()
        if eventKey in self.__keyInputDict:
            self.__keyInputDict[eventKey][0]()

    def keyReleaseEvent(self, event):
        ''''''
        eventKey = event.key()
        if eventKey in self.__keyInputDict:
            self.__keyInputDict[eventKey][1]()

    def setStatusBar(self, statusText):
        ''''''
        self.__statusLabel.setText(statusText)

    def done(self):
        ''''''
        # Render the window
        self.show()

    def addMenu(self, menuTitle):
        ''''''
        # Check if menuTitle does not exist (prevent duplicates)
        if menuTitle in self.__menuDict:
            raise Exception('Menu ' + menuTitle + ' was already created!')
        else:
            self.__menuDict[menuTitle] = \
            self.__menubar.addMenu('&' + menuTitle);

    def addMenuItem(self, menuTitle, menuItem, evtFunction=None):
        ''''''
        # Check if menuTitle exists
        if menuTitle in self.__menuDict:
            # Create the menu item
            menuItem = QtGui.QAction('&' + menuItem, self)
            if evtFunction:
                menuItem.triggered.connect(lambda: evtFunction())
            # Add the menu items to the menu item dictionary
            self.__menuDict[menuTitle].addAction(menuItem)
        else:
            raise Exception('Menu ' + menuTitle + ' was not found!')

    def defaultEvent(self):
        ''''''
        msgBoxTitle = 'Error'
        msgBoxText = 'The specific action is not implemented!'
        # Render the error message box
        QtGui.QMessageBox.critical(self, msgBoxTitle, msgBoxText,
                                   buttons = QtGui.QMessageBox.Ok)

    def setupDrawingGrid(self, canvasWidth, canvasHeight, pxSize):
        ''''''
        self.__canvas.setGrid(canvasWidth, canvasHeight, pxSize)

    def clearDrawingGrid(self):
        ''''''
        self.__canvas.clearGrid()

    def updateDrawingGrid(self, grid):
        ''''''
        self.__canvas.updateGrid(grid)

    def setDrawingGridBgColour(self, bgColour):
        ''''''
        self.__canvas.updateBgColour(bgColour)

    def setDrawingGridPxColour(self, pxColour):
        ''''''
        self.__canvas.updatePxColour(pxColour)

    def getDrawingGridBgColour(self):
        ''''''
        return self.__canvas.getBgColour()

    def getDrawingGridPxColour(self):
        ''''''
        return self.__canvas.getPxColour()

    def addMenuSeperator(self, menuTitle):
        ''''''
        # Check if menuTitle exists
        if menuTitle in self.__menuDict:
            self.__menuDict[menuTitle].addSeparator()
        else:
            raise Exception('Menu ' + menuTitle + ' was not found!')
