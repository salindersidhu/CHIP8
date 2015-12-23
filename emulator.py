import sys
import chip8cpu
from PyQt4 import QtGui, QtCore

class Window(QtGui.QMainWindow):
    
    def __init__(self):
        ''''''
        super(Window, self).__init__()
        # Configure the window's properties
        self.setGeometry(0, 0, 650, 400)
        self.setFixedSize(650, 400)
        self.setWindowTitle("Python CHIP-8 Emulator")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        # Set the window to appear in the center of the screen
        self._centerOnScreen()
        # Configure the remaining parts of the GUI
        self._setStatusBar()
        self._setMainMenu()
        # Render the window
        self.show()

    def _setMainMenu(self):
        ''''''
        # Define events and statusbar text for all menu bar items
        exitAction = QtGui.QAction('&Quit', self)
        exitAction.setStatusTip('Exit the application')
        exitAction.triggered.connect(self.close)
        aboutAction = QtGui.QAction('&About', self)
        aboutAction.setStatusTip('About the application')
        aboutAction.triggered.connect(lambda: self._evtAboutDialog())
        # Define the menu bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        prefMenu = menubar.addMenu('&Preferences')
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(aboutAction)

    def _evtAboutDialog(self):
        ''''''
        msgBox = QtGui.QMessageBox()
        msgBoxTitle = 'About'
        msgBoxText = 'CHIP-8 Emulator created using:\nPython 3 and PyQt 4' + \
            '\n\nCopyright (C) 2015 Salinder Sidhu'
        # Render the message box
        QtGui.QMessageBox.information(self, msgBoxTitle, msgBoxText,
                                      buttons = QtGui.QMessageBox.Ok)
        
    def _setStatusBar(self):
        ''''''
        self.statusBar().showMessage('Ready...')

    def _centerOnScreen(self):
        ''''''
        res = QtGui.QDesktopWidget().screenGeometry()
        move_width = (res.width() / 2) - (self.frameSize().width() / 2)
        move_height = (res.height() / 2) - (self.frameSize().height() / 2)
        self.move(move_width, move_height)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
