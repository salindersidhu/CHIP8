import sys
import pickle
import traceback
from PyQt4 import QtGui, QtCore
from chip8 import Chip8
from settings import Settings
from gridframe import GridFrame
from guiwindow import GUIWindow


class InterpreterApp(QtGui.QApplication):
    ''''''

    def __init__(self, args):
        ''''''
        super(InterpreterApp, self).__init__(args)
        # Application variables
        self.__FPS = 60
        self.__defaultStatus = 'Please load a ROM file...'
        self.__pausedStatus = 'PAUSED'
        self.__runStatus = 'Running...'
        self.__debugLog = 'debugLog.txt'
        self.__isPaused = False
        self.__isRunning = False
        self.__chip8 = Chip8()
        self.__keyBindings = {}
        self.__timer = QtCore.QBasicTimer()
        # Configure Settings
        self.__settings = Settings('settings.ini')
        # Configure the GUIWindow
        self.__window = GUIWindow('Python CHIP-8 Interpreter', 640, 360,
                                  'Resources/icon.png')
        # Configure the GridFrame
        self.__gridFrame = GridFrame(self.__window, 64, 32, 10, (0, 0, 0),
                                     (255, 255, 255))
        self.__window.setCentralWidget(self.__gridFrame)
        # Setup remaining GUI elements
        self.__loadSettings()
        self.__setupMenu()
        self.__setupMenuItems()
        self.__setupKeyBindings()
        self.__window.setStatusBar(self.__defaultStatus)
        self.__window.show()
        # Start the CHIP-8 emulation
        self.__emulate()

    def __loadSettings(self):
        ''''''
        # Save default settings to file if they no settings data exists
        if self.__settings.isEmpty():
            defaults = {}
            # Get the default value for the pixel colour
            pixelColour = self.__gridFrame.getPixelColour()
            defaults['pxcolr'] = pixelColour[0]
            defaults['pxcolg'] = pixelColour[1]
            defaults['pxcolb'] = pixelColour[2]
            # Get the  default value for the background color
            backgroundColour = self.__gridFrame.getBackgroundColour()
            defaults['bgcolr'] = backgroundColour[0]
            defaults['bgcolg'] = backgroundColour[1]
            defaults['bgcolb'] = backgroundColour[2]
            # Add and save default settings
            self.__settings.addNewSetting('DEFAULT', defaults)
        else:
            # Load settings for pixel colour
            pxRed = int(self.__settings.getSetting('DEFAULT', 'pxcolr'))
            pxGreen = int(self.__settings.getSetting('DEFAULT', 'pxcolg'))
            pxBlue = int(self.__settings.getSetting('DEFAULT', 'pxcolb'))
            self.__gridFrame.changePixelColour((pxRed, pxGreen, pxBlue))
            # Load settings for background colour
            bgRed = int(self.__settings.getSetting('DEFAULT', 'bgcolr'))
            bgGreen = int(self.__settings.getSetting('DEFAULT', 'bgcolg'))
            bgBlue = int(self.__settings.getSetting('DEFAULT', 'bgcolb'))
            self.__gridFrame.changeBackgroundColour((bgRed, bgGreen, bgBlue))

    def __setupMenu(self):
        ''''''
        self.__window.addMenu('File')
        self.__window.addMenu('Options')
        self.__window.addMenu('Settings')
        self.__window.addMenu('Help')

    def __setupMenuItems(self):
        ''''''
        # Setup File menu items
        self.__window.addMenuItem('File', 'Load ROM', self.__eventLoadROM)
        self.__window.addMenuSeperator('File')
        self.__window.addMenuItem('File', 'Quit', self.__window.close)
        # Setup Option menu items
        self.__window.addMenuItem('Options', 'Reset', self.__eventReset)
        self.__window.addMenuItem('Options', 'Pause / Resume',
                                  self.__eventPauseResume)
        self.__window.addMenuSeperator('Options')
        self.__window.addMenuItem('Options', 'Save State',
                                  self.__eventSaveState)
        self.__window.addMenuItem('Options', 'Load State',
                                  self.__eventLoadState)
        # Setup Settings menu items
        self.__window.addMenuItem('Settings', 'Pixel Colour',
                                  self.__eventChangePxColour)
        self.__window.addMenuItem('Settings', 'Background Colour',
                                  self.__eventChangeBgColour)
        # Setup Help menu items
        self.__window.addMenuItem('Help', 'About', self.__eventAbout)

    def __setupKeyBindings(self):
        ''''''
        self.__keyBindings[QtCore.Qt.Key_1] = [
            lambda: self.__chip8.setKeyState(1, 1),
            lambda: self.__chip8.setKeyState(1, 0)]
        self.__keyBindings[QtCore.Qt.Key_2] = [
            lambda: self.__chip8.setKeyState(2, 1),
            lambda: self.__chip8.setKeyState(2, 0)]
        self.__keyBindings[QtCore.Qt.Key_3] = [
            lambda: self.__chip8.setKeyState(3, 1),
            lambda: self.__chip8.setKeyState(3, 0)]
        self.__keyBindings[QtCore.Qt.Key_4] = [
            lambda: self.__chip8.setKeyState(12, 1),
            lambda: self.__chip8.setKeyState(12, 0)]
        self.__keyBindings[QtCore.Qt.Key_Q] = [
            lambda: self.__chip8.setKeyState(4, 1),
            lambda: self.__chip8.setKeyState(4, 0)]
        self.__keyBindings[QtCore.Qt.Key_W] = [
            lambda: self.__chip8.setKeyState(5, 1),
            lambda: self.__chip8.setKeyState(5, 0)]
        self.__keyBindings[QtCore.Qt.Key_E] = [
            lambda: self.__chip8.setKeyState(6, 1),
            lambda: self.__chip8.setKeyState(6, 0)]
        self.__keyBindings[QtCore.Qt.Key_R] = [
            lambda: self.__chip8.setKeyState(13, 1),
            lambda: self.__chip8.setKeyState(13, 0)]
        self.__keyBindings[QtCore.Qt.Key_A] = [
            lambda: self.__chip8.setKeyState(7, 1),
            lambda: self.__chip8.setKeyState(7, 0)]
        self.__keyBindings[QtCore.Qt.Key_S] = [
            lambda: self.__chip8.setKeyState(8, 1),
            lambda: self.__chip8.setKeyState(8, 0)]
        self.__keyBindings[QtCore.Qt.Key_D] = [
            lambda: self.__chip8.setKeyState(9, 1),
            lambda: self.__chip8.setKeyState(9, 0)]
        self.__keyBindings[QtCore.Qt.Key_F] = [
            lambda: self.__chip8.setKeyState(14, 1),
            lambda: self.__chip8.setKeyState(14, 0)]
        self.__keyBindings[QtCore.Qt.Key_Z] = [
            lambda: self.__chip8.setKeyState(10, 1),
            lambda: self.__chip8.setKeyState(10, 0)]
        self.__keyBindings[QtCore.Qt.Key_X] = [
            lambda: self.__chip8.setKeyState(0, 1),
            lambda: self.__chip8.setKeyState(0, 0)]
        self.__keyBindings[QtCore.Qt.Key_C] = [
            lambda: self.__chip8.setKeyState(11, 1),
            lambda: self.__chip8.setKeyState(11, 0)]
        self.__keyBindings[QtCore.Qt.Key_V] = [
            lambda: self.__chip8.setKeyState(15, 1),
            lambda: self.__chip8.setKeyState(15, 0)]
        self.__window.updateKeyBindings(self.__keyBindings)

    def __logExceptionToFile(self, exceptionMessage):
        ''''''
        message = 'The application has crashed!\n\nPlease refer to ' + \
            self.__debugLog + ' for more information!'
        QtGui.QMessageBox.critical(self.__window, 'Error', message,
                                   buttons=QtGui.QMessageBox.Ok)
        debugFile = open(self.__debugLog, 'w')
        debugFile.write(exceptionMessage)

    def __emulate(self):
        ''''''
        try:
            if self.__isRunning and not self.__isPaused:
                self.__chip8.emulateCycle()
                self.__gridFrame.updatePixels(self.__chip8.getGFX())
        except:
            # Exception was caught, log it and terminate application
            self.__isRunning = False
            self.__logExceptionToFile(traceback.format_exc())
            self.__window.close()
        finally:
            QtCore.QTimer.singleShot(1 / self.__FPS, self.__emulate)

    def __selectColour(self, defColour):
        ''''''
        # Pause interpreter while dialog is shown
        self.__pauseEmulator()
        color = QtGui.QColorDialog.getColor(QtGui.QColor(defColour[0],
                                                         defColour[1],
                                                         defColour[2]),
                                            self.__window)
        # Resume interpreter when dialog is closed
        self.__pauseEmulator(False)
        return color

    def __pauseEmulator(self, action=True):
        ''''''
        if self.__isRunning:
            self.__isPaused = action
            # Set the status text (paused or running)
            if self.__isPaused:
                self.__window.setStatusBar(self.__pausedStatus)
            else:
                self.__window.setStatusBar(self.__runStatus)

    def __eventSaveState(self):
        ''''''
        # Check if ROM is loaded
        if self.__isRunning:
            # Pause interpreter while dialog is shown
            self.__pauseEmulator()
            filename = QtGui.QFileDialog.getSaveFileName(self.__window,
                                                         'Save State', '',
                                                         'State Data (*.dat)')
            # Resume interpreter when dialog is closed
            self.__pauseEmulator(False)
            # Save the state of the CHIP-8 CPU to a file
            if filename:
                pickle.dump(self.__chip8.getState(), open(filename, 'wb'))
        else:
            # Display error message
            QtGui.QMessageBox.critical(self.__window, 'Error', 'Could not ' +
                                       'save state. Please load a ROM first.',
                                       buttons=QtGui.QMessageBox.Ok)

    def __eventLoadState(self):
        ''''''
        # Pause interpreter while dialog is shown
        self.__pauseEmulator()
        filename = QtGui.QFileDialog.getOpenFileName(self.__window,
                                                     'Load State', '',
                                                     'State Data (*.dat)')
        # Resume interpreter when dialog is closed
        self.__pauseEmulator(False)
        # Load the state of the CHIP-8 CPU from a file
        if filename:
            self.__chip8.setState(pickle.load(open(filename, 'rb')))
            self.__window.setStatusBar(self.__runStatus)
            self.__isRunning = True

    def __eventChangeBgColour(self):
        ''''''
        newCol = self.__selectColour(self.__gridFrame.getBackgroundColour())
        # Verify that the new background colour is valid
        if newCol.isValid():
            newBgColour = (newCol.red(), newCol.green(), newCol.blue())
            self.__gridFrame.changeBackgroundColour(newBgColour)
            # Save the new background colour to settings
            self.__settings.editSetting('DEFAULT', 'bgcolr', newCol.red())
            self.__settings.editSetting('DEFAULT', 'bgcolg', newCol.green())
            self.__settings.editSetting('DEFAULT', 'bgcolb', newCol.blue())

    def __eventChangePxColour(self):
        ''''''
        newCol = self.__selectColour(self.__gridFrame.getPixelColour())
        # Verify that the new pixel colour is valid
        if newCol.isValid():
            newPxColour = (newCol.red(), newCol.green(), newCol.blue())
            self.__gridFrame.changePixelColour(newPxColour)
            # Save the new pixel colour to settings
            self.__settings.editSetting('DEFAULT', 'pxcolr', newCol.red())
            self.__settings.editSetting('DEFAULT', 'pxcolg', newCol.green())
            self.__settings.editSetting('DEFAULT', 'pxcolb', newCol.blue())

    def __eventPauseResume(self):
        ''''''
        self.__pauseEmulator(not self.__isPaused)

    def __eventReset(self):
        ''''''
        if self.__isRunning:
            self.__gridFrame.clearPixels()
            self.__chip8.reset()
            self.__window.setStatusBar(self.__defaultStatus)
            self.__isPaused = self.__isRunning = False

    def __eventAbout(self):
        ''''''
        # Pause interpreter while dialog is shown
        self.__pauseEmulator()
        message = 'Python CHIP-8 CPU Interpreter\nPython 3 and PyQt 4\n\n' + \
            'Developed by Salinder Sidhu'
        # Render the message box
        QtGui.QMessageBox.information(self.__window, 'About', message,
                                      buttons=QtGui.QMessageBox.Ok)
        # Resume interpreter when dialog is closed
        self.__pauseEmulator(False)

    def __eventLoadROM(self):
        ''''''
        # Pause interpreter while dialog is shown
        self.__pauseEmulator()
        filename = QtGui.QFileDialog.getOpenFileName(self.__window,
                                                     'Open File', '',
                                                     'CHIP8 ROM (*.c8)')
        # Resume interpreter when dialog is closed
        self.__pauseEmulator(False)
        # Load the CHIP-8 ROM if the filename exists
        if filename:
            self.__chip8.loadROM(filename)
            self.__window.setStatusBar(self.__runStatus)
            self.__isRunning = True

if __name__ == '__main__':
    # Pass command line arguments into application and launch it
    myApp = InterpreterApp(sys.argv)
    sys.exit(myApp.exec_())
