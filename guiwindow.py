from PyQt4 import QtGui


class GUIWindow(QtGui.QMainWindow):
    ''''''

    def __init__(self, winTitle, winWidth, winHeight, winIcon):
        ''''''
        super(GUIWindow, self).__init__()
        # Exceptions
        self.__menuExistsException = Exception('The specified menu already' +
                                               ' exists!')
        self.__menuNotFoundException = Exception('The specified menu was ' +
                                                 'not found!')
        # GUIWindow variables
        self.__menubar = self.menuBar()         # Define a Menu Bar
        self.__menuDict = {}                    # Define a map of Menus
        self.__statusLabel = QtGui.QLabel()     # Define a new status label
        self.__keyInputDict = {}                # Define a map of key events
        # Configure the window's properties
        self.setGeometry(0, 0, winWidth, winHeight)
        self.setFixedSize(winWidth, winHeight)
        self.setWindowTitle(winTitle)
        self.setWindowIcon(QtGui.QIcon(winIcon))
        # Bind the QLabel to the Status Bar
        self.statusBar().addWidget(self.__statusLabel, 1)
        # Set the window to appear in the center of the screen
        self.__centerOnScreen()
        # Configure the remaining GUI elements for the window

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

    def __centerOnScreen(self):
        ''''''
        res = QtGui.QDesktopWidget().screenGeometry()
        move_width = (res.width() / 2) - (self.frameSize().width() / 2)
        move_height = (res.height() / 2) - (self.frameSize().height() / 2)
        self.move(move_width, move_height)

    def updateKeyBindings(self, keyBindings):
        ''''''
        self.__keyInputDict = keyBindings.copy()

    def setStatusBar(self, statusText):
        ''''''
        self.__statusLabel.setText(statusText)

    def addMenu(self, menuTitle):
        ''''''
        # Check if menuTitle does not exist (prevent duplicates)
        if menuTitle in self.__menuDict:
            raise self.__menuExistsException
        else:
            self.__menuDict[menuTitle] = \
                self.__menubar.addMenu('&' + menuTitle)

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
            raise self.__menuNotFoundExceptionException

    def addMenuSeperator(self, menuTitle):
        ''''''
        # Check if menuTitle exists
        if menuTitle in self.__menuDict:
            self.__menuDict[menuTitle].addSeparator()
        else:
            raise self.__menuNotFoundExceptionException
