import sys
import pickle
from PyQt4 import QtGui, QtCore
from chip8 import Chip8
from guiwindow import GUIWindow
from settings import Settings

class InterpreterApp:
    ''''''

    def __init__(self):
        ''''''
        # Application variables
        self.isPaused = False
        self.isRunning = False
        self.chip8 = Chip8()
        self.FPS = 60
        self.timer = QtCore.QBasicTimer()
        self.keyBindings = {}
        self.settings = Settings('settings.ini')
        # GUI Window variables
        self.winTitle = 'Python CHIP-8 Interpreter'
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
        self.loadSettings()
        self.setupMenu()
        self.setupMenuItems()
        self.setupKeyBindings()
        self.window.setStatusBar(self.defaultStatusText)
        self.window.setupDrawingGrid(self.canvasPxWidth, self.canvasPxHeight,
                                     self.canvasPxSize)
        # Finish GUI window setup
        self.window.done()
        # Start the CHIP-8 timed emulation
        self.emulate()

    def loadSettings(self):
        ''''''
        # Save default settings to file if they no settings data exists
        if self.settings.isEmpty():
            defaults = {}
            # Get the default value for the pixel colour
            defaultPxColours = self.window.getDrawingGridPxColour()
            defaults['pxcolr'] = defaultPxColours[0]
            defaults['pxcolg'] = defaultPxColours[1]
            defaults['pxcolb'] = defaultPxColours[2]
            # Get the  default value for the background color
            defaultBgColours = self.window.getDrawingGridBgColour()
            defaults['bgcolr'] = defaultBgColours[0]
            defaults['bgcolg'] = defaultBgColours[1]
            defaults['bgcolb'] = defaultBgColours[2]
            # Add and save default settings
            self.settings.addNewSetting('DEFAULT', defaults)
        else:
            # Load settings for pixel colour
            pxRed = int(self.settings.getSetting('DEFAULT', 'pxcolr'))
            pxGreen = int(self.settings.getSetting('DEFAULT', 'pxcolg'))
            pxBlue = int(self.settings.getSetting('DEFAULT', 'pxcolb'))
            self.window.setDrawingGridPxColour((pxRed, pxGreen, pxBlue))
            # Load settings for background colour
            bgRed = int(self.settings.getSetting('DEFAULT', 'bgcolr'))
            bgGreen = int(self.settings.getSetting('DEFAULT', 'bgcolg'))
            bgBlue = int(self.settings.getSetting('DEFAULT', 'bgcolb'))
            self.window.setDrawingGridBgColour((bgRed, bgGreen, bgBlue))

    def setupMenu(self):
        ''''''
        self.window.addMenu('File')
        self.window.addMenu('Options')
        self.window.addMenu('Settings')
        self.window.addMenu('Help')

    def setupMenuItems(self):
        ''''''
        # Setup File menu items
        self.window.addMenuItem('File', 'Load ROM', self.eventLoadROM)
        self.window.addMenuSeperator('File')
        self.window.addMenuItem('File', 'Quit', self.window.close)
        # Setup Option menu items
        self.window.addMenuItem('Options', 'Reset', self.eventReset)
        self.window.addMenuItem('Options', 'Pause / Resume',
                                self.eventPauseResume)
        self.window.addMenuSeperator('Options')
        self.window.addMenuItem('Options', 'Save State', self.eventSaveState)
        self.window.addMenuItem('Options', 'Load State', self.eventLoadState)
        # Setup Settings menu items
        self.window.addMenuItem('Settings', 'Pixel Colour',
                                self.eventChangePxColour)        
        self.window.addMenuItem('Settings', 'Background Colour',
                                self.eventChangeBgColour)
        self.window.addMenuItem('Settings', 'Key Bindings')
        # Setup Help menu items
        self.window.addMenuItem('Help', 'About', self.eventAbout)

    def setupKeyBindings(self):
        ''''''
        self.keyBindings[QtCore.Qt.Key_1] = [
            lambda: self.chip8.set_key_state(1, 1),
            lambda: self.chip8.set_key_state(1, 0)]
        self.keyBindings[QtCore.Qt.Key_2] = [
            lambda: self.chip8.set_key_state(2, 1),
            lambda: self.chip8.set_key_state(2, 0)]
        self.keyBindings[QtCore.Qt.Key_3] = [
            lambda: self.chip8.set_key_state(3, 1),
            lambda: self.chip8.set_key_state(3, 0)]
        self.keyBindings[QtCore.Qt.Key_4] = [
            lambda: self.chip8.set_key_state(12, 1),
            lambda: self.chip8.set_key_state(12, 0)]
        self.keyBindings[QtCore.Qt.Key_Q] = [
            lambda: self.chip8.set_key_state(4, 1),
            lambda: self.chip8.set_key_state(4, 0)]
        self.keyBindings[QtCore.Qt.Key_W] = [
            lambda: self.chip8.set_key_state(5, 1),
            lambda: self.chip8.set_key_state(5, 0)]
        self.keyBindings[QtCore.Qt.Key_E] = [
            lambda: self.chip8.set_key_state(6, 1),
            lambda: self.chip8.set_key_state(6, 0)]
        self.keyBindings[QtCore.Qt.Key_R] = [
            lambda: self.chip8.set_key_state(13, 1),
            lambda: self.chip8.set_key_state(13, 0)]
        self.keyBindings[QtCore.Qt.Key_A] = [
            lambda: self.chip8.set_key_state(7, 1),
            lambda: self.chip8.set_key_state(7, 0)]
        self.keyBindings[QtCore.Qt.Key_S] = [
            lambda: self.chip8.set_key_state(8, 1),
            lambda: self.chip8.set_key_state(8, 0)]
        self.keyBindings[QtCore.Qt.Key_D] = [
            lambda: self.chip8.set_key_state(9, 1),
            lambda: self.chip8.set_key_state(9, 0)]
        self.keyBindings[QtCore.Qt.Key_F] = [
            lambda: self.chip8.set_key_state(14, 1),
            lambda: self.chip8.set_key_state(14, 0)]
        self.keyBindings[QtCore.Qt.Key_Z] = [
            lambda: self.chip8.set_key_state(10, 1),
            lambda: self.chip8.set_key_state(10, 0)]
        self.keyBindings[QtCore.Qt.Key_X] = [
            lambda: self.chip8.set_key_state(0, 1),
            lambda: self.chip8.set_key_state(0, 0)]
        self.keyBindings[QtCore.Qt.Key_C] = [
            lambda: self.chip8.set_key_state(11, 1),
            lambda: self.chip8.set_key_state(11, 0)]
        self.keyBindings[QtCore.Qt.Key_V] = [
            lambda: self.chip8.set_key_state(15, 1),
            lambda: self.chip8.set_key_state(15, 0)]
        self.window.updateKeyBindings(self.keyBindings)

    def pauseEmulator(self, action=True):
        ''''''
        if self.isRunning:
            self.isPaused = action
            # Set the status bar text depending on the state of the interpreter
            if self.isPaused:
                self.window.setStatusBar(self.pausedStatusText)
            else:
                self.window.setStatusBar(self.runningStatusText)

    def emulate(self):
        ''''''
        try:
            if self.isRunning and not self.isPaused:
                self.chip8.emulate_cycle()
                self.window.updateDrawingGrid(self.chip8.get_GFX())
        finally:
            QtCore.QTimer.singleShot(1 / self.FPS, self.emulate)

    def eventSaveState(self):
        ''''''
        msgBoxTitle = 'Error'
        msgBoxText = 'Could not save state. Please load a ROM first.'
        # Check if ROM is loaded
        if self.isRunning:
            # Pause interpreter while dialog is shown
            self.pauseEmulator()
            filename = QtGui.QFileDialog.getSaveFileName(self.window, 
                                                         'Save State',
                                                         '',
                                                         'State Data (*.dat)')
            # Resume interpreter when dialog is closed
            self.pauseEmulator(False)
            # Save the state of the CHIP-8 CPU to a file
            if filename:
                pickle.dump(self.chip8.get_state(), open(filename, 'wb'))
        else:
            # Render the error message box
            QtGui.QMessageBox.critical(self.window, msgBoxTitle, msgBoxText,
                                       buttons = QtGui.QMessageBox.Ok)

    def eventLoadState(self):
        ''''''
        # Pause interpreter while dialog is shown
        self.pauseEmulator()
        filename = QtGui.QFileDialog.getOpenFileName(self.window, 'Load State',
                                                     '',
                                                     'State Data (*.dat)')
        # Resume interpreter when dialog is closed
        self.pauseEmulator(False)
        # Load the state of the CHIP-8 CPU from a file
        if filename:
            self.chip8.set_state(pickle.load(open(filename, 'rb')))
            self.window.setStatusBar(self.runningStatusText)
            self.isRunning = True

    def eventChangeBgColour(self):
        ''''''
        newCol = self.selectColour(self.window.getDrawingGridBgColour())
        # Verify that the colour is valid
        if newCol.isValid():
            newBgColour = (newCol.red(), newCol.green(), newCol.blue())
            self.window.setDrawingGridBgColour(newBgColour)
            # Save the background colour to settings
            self.settings.editSetting('DEFAULT', 'bgcolr', newCol.red())
            self.settings.editSetting('DEFAULT', 'bgcolg', newCol.green())
            self.settings.editSetting('DEFAULT', 'bgcolb', newCol.blue())

    def eventChangePxColour(self):
        ''''''
        newCol = self.selectColour(self.window.getDrawingGridPxColour())
        # Verify that the colour is valid
        if newCol.isValid():
            newPxColour = (newCol.red(), newCol.green(), newCol.blue())
            self.window.setDrawingGridPxColour(newPxColour)
            # Save the pixel colour to settings
            self.settings.editSetting('DEFAULT', 'pxcolr', newCol.red())
            self.settings.editSetting('DEFAULT', 'pxcolg', newCol.green())
            self.settings.editSetting('DEFAULT', 'pxcolb', newCol.blue())

    def selectColour(self, defColour):
        ''''''
        # Pause interpreter while dialog is shown
        self.pauseEmulator()
        color = QtGui.QColorDialog.getColor(QtGui.QColor(defColour[0], 
                                                         defColour[1], 
                                                         defColour[2]), 
                                            self.window)
        # Resume interpreter when dialog is closed
        self.pauseEmulator(False)
        return color

    def eventPauseResume(self):
        ''''''
        self.pauseEmulator(not self.isPaused)

    def eventReset(self):
        ''''''
        if self.isRunning:
            self.window.clearDrawingGrid()
            self.chip8.reset()
            self.window.setStatusBar(self.defaultStatusText)
            self.isPaused = self.isRunning = False

    def eventAbout(self):
        ''''''
        # Pause interpreter while dialog is shown
        self.pauseEmulator()
        msgBoxTitle = 'About'
        msgBoxText = 'Python CHIP-8 CPU Interpreter\nPython 3 and PyQt 4' + \
            '\n\nCopyright (C) 2015 Salinder Sidhu'
        # Render the message box
        dialog = QtGui.QMessageBox.information(self.window, msgBoxTitle,
                                               msgBoxText,
                                               buttons = QtGui.QMessageBox.Ok)
        # Resume interpreter when dialog is closed
        self.pauseEmulator(False)
 
    def eventLoadROM(self):
        ''''''
        # Pause interpreter while dialog is shown
        self.pauseEmulator()
        filename = QtGui.QFileDialog.getOpenFileName(self.window,
                                                     'Open File',
                                                     '', 'CHIP8 ROM (*.c8)')
        # Resume interpreter when dialog is closed
        self.pauseEmulator(False)
        # Load the CHIP-8 ROM if the filename exists        
        if filename:
            self.chip8.load_rom(filename)
            self.window.setStatusBar(self.runningStatusText)
            self.isRunning = True

if __name__ == '__main__':
    myApp = InterpreterApp()
    sys.exit(myApp.app.exec_())