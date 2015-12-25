import sys
import pickle
import configparser
from PyQt4 import QtGui, QtCore
from chip8 import Chip8
from guiwindow import GUIWindow

class EmulatorApplication:
    ''''''

    def __init__(self):
        ''''''
        # Application variables
        self.isPaused = False
        self.isRunning = False
        self.CPU = Chip8()
        self.FPS = 60
        self.timer = QtCore.QBasicTimer()
        # GUI Window variables
        self.winTitle = 'Python CHIP-8 Emulator'
        self.winWidth = 640
        self.winHeight = 360
        self.canvasPxWidth = 64
        self.canvasPxHeight = 32
        self.canvasPxSize = 10
        self.winIcon = 'Resources/icon.png'
        self.defaultStatusText = 'Please load a ROM file...'
        self.pausedStatusText = 'PAUSED'
        self.runningStatusText = 'Running...'
        # Configure the application
        self.app = QtGui.QApplication(sys.argv)
        # Configure the GUI window
        self.window = GUIWindow(self.winTitle, self.winWidth, self.winHeight,
                                self.winIcon)
        self.setup_menu()
        self.setup_menu_items()
        self.window.setStatusBar(self.defaultStatusText)
        self.window.setupDrawingGrid(self.canvasPxWidth, self.canvasPxHeight,
                                     self.canvasPxSize)
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
        self.window.addMenuItem('File', 'Load ROM', self.event_load_ROM)
        self.window.addMenuSeperator('File')
        self.window.addMenuItem('File', 'Quit', self.window.close)
        # Setup Option menu items
        self.window.addMenuItem('Options', 'Reset', self.event_reset)
        self.window.addMenuItem('Options', 'Pause / Resume',
                                self.event_pause_resume)
        self.window.addMenuSeperator('Options')
        self.window.addMenuItem('Options', 'Save State')
        self.window.addMenuItem('Options', 'Load State')
        # Setup Settings menu items
        self.window.addMenuItem('Settings', 'Pixel Colour')        
        self.window.addMenuItem('Settings', 'Background Colour')
        self.window.addMenuItem('Settings', 'Control Key Mapping')
        # Setup Help menu items
        self.window.addMenuItem('Help', 'About', self.event_about)

    def emulate(self):
        ''''''
        try:
            if self.isRunning:
                if  not self.isPaused:
                    self.CPU.emulate_cycle()
                    self.window.updateDrawingGrid(self.CPU.get_GFX())
        finally:
            QtCore.QTimer.singleShot(1 / self.FPS, self.emulate)

    def event_pause_resume(self):
        ''''''
        if self.isRunning:
            self.isPaused = not self.isPaused
            # Set the status bar text depending on the state of the emulator
            if self.isPaused:
                self.window.setStatusBar(self.pausedStatusText)
            else:
                self.window.setStatusBar(self.runningStatusText)

    def event_reset(self):
        ''''''
        if self.isRunning:
            self.window.clearDrawingGrid()
            self.CPU.reset()
            self.window.setStatusBar(self.defaultStatusText)
            self.isPaused = self.isRunning = False

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
            self.window.setStatusBar(self.runningStatusText)
            self.isRunning = True

if __name__ == '__main__':
    EmulatorApplication()
