from PyQt4 import QtGui, QtCore

class MenuException(Exception):
    ''''''
    pass

class GUIWindow(QtGui.QMainWindow):
    ''''''
    
    def __init__(self, winTitle, winWidth, winHeight, winIcon):
        ''''''
        super(GUIWindow, self).__init__()
        # Window GUI variables
        self.__menubar = self.menuBar()     # Define a Menu Bar
        self.__menuDict = {}                # Define a map of Menus
        # Configure the window's properties
        self.setGeometry(0, 0, winWidth, winHeight)
        self.setFixedSize(winWidth, winHeight)
        self.setWindowTitle(winTitle)
        self.setWindowIcon(QtGui.QIcon(winIcon))
        # Set the window to appear in the center of the screen
        self.__centerOnScreen()
        # Configure the remaining GUI elements for the window
        
    def __centerOnScreen(self):
        ''''''
        res = QtGui.QDesktopWidget().screenGeometry()
        move_width = (res.width() / 2) - (self.frameSize().width() / 2)
        move_height = (res.height() / 2) - (self.frameSize().height() / 2)
        self.move(move_width, move_height)
        
    def setStatusBar(self, statusText):
        ''''''
        self.statusBar().showMessage(statusText)
        
    def done(self):
        ''''''
        # Render the window
        self.show()
        
    def addMenu(self, menuTitle):
        ''''''
        # Check if menuTitle does not exist (prevent duplicates)
        if menuTitle in self.__menuDict:
            raise MenuException('Menu ' + menuTitle + ' was already created!')
        else:
            self.__menuDict[menuTitle] = \
            self.__menubar.addMenu('&' + menuTitle);
        
    def addMenuItem(self, menuTitle, menuItem, statusText, evtFunction=None):
        ''''''
        # Check if menuTitle exists
        if menuTitle in self.__menuDict:
            # Create the menu item
            menuItem = QtGui.QAction('&' + menuItem, self)
            menuItem.setStatusTip(statusText)
            if evtFunction:
                menuItem.triggered.connect(lambda: evtFunction())
            # Add the menu items to the menu item dictionary
            self.__menuDict[menuTitle].addAction(menuItem)
        else:
            raise MenuException('Menu ' + menuTitle + ' was not found!')
    
    def addMenuSeperator(self, menuTitle):
        ''''''
        # Check if menuTitle exists
        if menuTitle in self.__menuDict:
            self.__menuDict[menuTitle].addSeparator()
        else:
            raise MenuException('Menu ' + menuTitle + ' was not found!')