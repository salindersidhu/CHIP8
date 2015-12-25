import sys
import pickle
from PyQt4 import QtGui, QtCore
from chip8 import Chip8
from guiwindow import GUIWindow

class EmulatorApplication:
    ''''''

    def __init__(self):
        ''''''
        # Application variables
        self.isPaused = False
        self.isRomLoaded = False
        self.CPU = Chip8()
        self.FPS = 60
        self.timer = QtCore.QBasicTimer()
        # GUI Window variables
        self.winTitle = 'Python CHIP-8 Emulator'
        self.winWidth = 640
        self.winHeight = 360
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
        self.window.setupDrawingGrid(64, 32, 10)
        # Finish GUI window setup
        self.window.done()
        # Start the CHIP-8 timed emulation
        self.emulate()
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
        self.window.addMenuItem('File', 'Load ROM', 'Load ROM file into RAM',
                                self.event_load_ROM)
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
        self.window.addMenuItem('Settings', 'Key Mappings',
                                'Change the controls for the emulator')
        # Setup Help menu items
        self.window.addMenuItem('Help', 'About', 'About the application',
                                self.event_about)

    def emulate(self):
        ''''''
        try:
            if self.isRomLoaded:
                if  not self.isPaused:
                    self.CPU.emulate_cycle()
                    self.window.updateDrawingGrid(self.CPU.get_GFX())
        finally:
            QtCore.QTimer.singleShot(1 / self.FPS, self.emulate)
    
    def event_about(self):
        ''''''
        msgBox = QtGui.QMessageBox()
        msgBoxTitle = 'About'
        msgBoxText = 'Python CHIP-8 CPU Emulator.\nPython 3 and PyQt 4' + \
            '\n\nCopyright (C) 2015 Salinder Sidhu'
        # Render the message box
        QtGui.QMessageBox.information(self.window, msgBoxTitle, msgBoxText,
                                      buttons = QtGui.QMessageBox.Ok)
 
    def event_load_ROM(self):
        ''''''
        filename = QtGui.QFileDialog.getOpenFileName(self.window,
                                                     'Open File',
                                                     '', 'CHIP8 ROM (*.c8)')
        # Load the CHIP-8 ROM if the filename exists
        if filename:
            self.CPU.load_rom(filename)
            self.isRomLoaded = True
            self.window.setStatusBar('ROM Loaded')

if __name__ == '__main__':
    EmulatorApplication()
