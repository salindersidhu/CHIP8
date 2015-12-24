import sys
import pickle
from PyQt4 import QtGui
from chip8 import Chip8
from guiwindow import GUIWindow

class EmulatorApplication:
    ''''''
    
    def __init__(self):
        ''''''
        # GUI Window variables
        self.winTitle = 'Python CHIP-8 Emulator'
        self.winWidth = 630
        self.winHeight = 400
        self.winIcon = 'icon.png'
        self.defaultStatus = 'Ready...'
        # Configure the application
        self.app = QtGui.QApplication(sys.argv)
        # Configure the GUI window
        self.window = GUIWindow(self.winTitle, self.winWidth, self.winHeight,
                                self.winIcon)
        self.window.setStatusBar(self.defaultStatus)
        self.setup_menu()
        self.setup_menu_items()
        # Finish GUI window setup
        self.window.done()
        sys.exit(self.app.exec_())
        
    def setup_menu(self):
        ''''''
        self.window.addMenu('File')
        self.window.addMenu('Options')
        self.window.addMenu('Settings')
        self.window.addMenu('Help')
        
    def setup_menu_items(self):
        ''''''
        # Setup File menu items
        self.window.addMenuItem('File', 'Reset', 'Reset the emulator')
        self.window.addMenuItem('File', 'Load ROM', 'Load ROM file into RAM')
        self.window.addMenuSeperator('File')
        self.window.addMenuItem('File', 'Quit', 'Exit the application',
                                self.window.close)
        # Setup Option menu items
        self.window.addMenuItem('Options', 'Pause', 'Pause the emulator')
        self.window.addMenuItem('Options', 'Resume', 'Resume the emulator')
        self.window.addMenuSeperator('Options')
        self.window.addMenuItem('Options', 'Save State',
                                'Save emulator state to a file')
        self.window.addMenuItem('Options', 'Load State',
                                'Load emulator state from a file')
        # Setup Settings menu items
        self.window.addMenuItem('Settings', 'Background Colour',
                                'Change the background colour')
        self.window.addMenuItem('Settings', 'Pixel Colour',
                                'Change the pixel colour')
        # Setup Help menu items
        self.window.addMenuItem('Help', 'About', 'About the application',
                                self.event_about)
        
    def event_about(self):
        ''''''
        msgBox = QtGui.QMessageBox()
        msgBoxTitle = 'About'
        msgBoxText = 'Python CHIP-8 CPU Emulator.\nPython 3 and PyQt 4' + \
            '\n\nCopyright (C) 2015 Salinder Sidhu'
        # Render the message box
        QtGui.QMessageBox.information(self.window, msgBoxTitle, msgBoxText,
                                      buttons = QtGui.QMessageBox.Ok)        

if __name__ == '__main__':
    EmulatorApplication()
