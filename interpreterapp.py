import sys
import pickle
from settings import Settings
from chip8.chip8 import Chip8
from gridframe import GridFrame
from guiwindow import GUIWindow
from PyQt5 import QtGui, QtCore, QtWidgets, QtMultimedia


class InterpreterApp(QtWidgets.QApplication):
    '''InterpreterApp extends the QtWidgets.QApplication class. This class
    creates the GUI for the CHIP-8 interpreter system and provides functions
    for all of the application's events. It uses GridFrame and GUIWindow to
    create the window, menu and status bars and the drawing grid frame
    required.'''

    def __init__(self, args):
        '''Create a new InterpreterApp with arguments specified by args.'''
        super(InterpreterApp, self).__init__(args)
        # Application constants and variables
        self.__FPS = 60
        self.__WIDTH = 640
        self.__HEIGHT = 360
        self.__WHITE = (255, 255, 255)
        self.__BLACK = (0, 0, 0)
        self.__WINTITLE = 'Python CHIP-8 Interpreter'
        self.__ICON = 'assets/icon.svg'
        self.__defaultStatus = 'Please load a ROM file...'
        self.__pausedStatus = 'PAUSED'
        self.__runStatus = 'Running...'
        self.__pauseLock = False
        self.__isPaused = False
        self.__isRunning = False
        self.__chip8 = Chip8()
        self.__keyBindings = {}
        self.__timer = QtCore.QBasicTimer()
        # Configure Settings
        self.__settings = Settings('settings.ini')
        # Configure the GUIWindow
        self.__window = GUIWindow(self.__WINTITLE,
                                  self.__WIDTH,
                                  self.__HEIGHT,
                                  self.__ICON)
        # Configure the GridFrame
        self.__gridFrame = GridFrame(self.__window,
                                     64,
                                     32,
                                     10,
                                     self.__BLACK,
                                     self.__WHITE)
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
        '''Load settings for the GridFrame's pixel colour and background
        colour.'''
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
        '''Add all the menus used in the application to GUIWindow.'''
        self.__window.addMenu('File')
        self.__window.addMenu('Options')
        self.__window.addMenu('Settings')
        self.__window.addMenu('Help')

    def __setupMenuItems(self):
        '''Add all the menu items, along with their event functions, used in
        the application to GUIWindow.'''
        # Setup File menu items
        self.__window.addMenuItem('File', 'Load ROM', self.__eventLoadROM)
        self.__window.addMenuSeperator('File')
        self.__window.addMenuItem('File', 'Quit', self.__window.close)
        # Setup Option menu items
        self.__window.addMenuItem('Options', 'Reset', self.__eventReset)
        self.__window.addCheckableMenuItem('Options',
                                           'Pause',
                                           False,
                                           self.__eventPauseResume)
        self.__window.addMenuSeperator('Options')
        self.__window.addMenuItem('Options',
                                  'Save State',
                                  self.__eventSaveState)
        self.__window.addMenuItem('Options',
                                  'Load State',
                                  self.__eventLoadState)
        # Setup Settings menu items
        self.__window.addMenuItem('Settings',
                                  'Pixel Colour',
                                  self.__eventChangePxColour)
        self.__window.addMenuItem('Settings',
                                  'Background Colour',
                                  self.__eventChangeBgColour)
        # Setup Help menu items
        self.__window.addMenuItem('Help', 'About', self.__eventAbout)

    def __setupKeyBindings(self):
        '''Configure the key bindings for the CHIP-8 controller using specific
        keys in order corresponding to the rows of the original CHIP-8 input
        controller.'''
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

    def __showException(self, exception):
        '''Show a popup message box with the exception that occured.'''
        message = "An unexpected error occured:\n\n {}".format(str(exception))
        QtWidgets.QMessageBox.critical(self.__window,
                                       'Error',
                                       message,
                                       buttons=QtWidgets.QMessageBox.Ok)

    def __emulate(self):
        '''Emulate the CHIP-8 system using a timer that executes some number
        of times per second specified by the framerate. Process CHIP-8
        instructions and pixel rendering. Halt the system if an exception is
        caught and log the exception to a file.'''
        try:
            if self.__isRunning and not self.__isPaused:
                self.__chip8.emulateCycle()
                self.__handleSound(self.__chip8.getSoundTimer())
                self.__gridFrame.updatePixels(self.__chip8.getGFX())
        except (Exception) as error:
            # Exception caught, display message and terminate
            self.__isRunning = False
            self.__showException(error)
            self.__window.close()
        finally:
            QtCore.QTimer.singleShot(1, self.__emulate)

    def __handleSound(self, soundTimer):
        '''Play a beep sound if the value of the soundTimer is non-zero.'''
        if soundTimer:
            QtMultimedia.QSound.play('assets/beep.wav')

    def __selectColour(self, defColour):
        '''Open a colour selection dialog and return a new QColor if a new
        colour was selected.'''
        # Pause interpreter while dialog is shown
        self.__pauseEmulator()
        color = QtWidgets.QColorDialog.getColor(QtGui.QColor(defColour[0],
                                                             defColour[1],
                                                             defColour[2]),
                                                self.__window)
        # Resume interpreter when dialog is closed
        if not self.__pauseLock:
            self.__pauseEmulator(False)
        return color

    def __pauseEmulator(self, action=True):
        '''Pause the emulator and modify the StatusBar text to reflect the
        state of the application.'''
        if self.__isRunning:
            self.__isPaused = action
            # Set the status text (paused or running)
            if self.__isPaused:
                self.__window.setStatusBar(self.__pausedStatus)
            else:
                self.__window.setStatusBar(self.__runStatus)
        else:
            # Uncheck pause menu option item
            self.__window.setCheckedMenuItem('Pause', False)

    def __eventSaveState(self):
        '''Display a save file dialog and save the current state of the CHIP-8
        system to the specified file. Display an error message otherwise if not
        ROM is loaded.'''
        # Check if ROM is loaded
        if self.__isRunning:
            # Pause interpreter while dialog is shown
            self.__pauseEmulator()
            fname, _ = QtWidgets.QFileDialog.getSaveFileName(
                self.__window,
                'Save State', '',
                'Saved Data (*.sav)',
                options=QtWidgets.QFileDialog.DontUseNativeDialog)
            # Add the .sav extension to the fname if it doesn't exist
            if not fname.endswith('.sav'):
                fname += '.sav'
            # Resume interpreter when dialog is closed
            if not self.__pauseLock:
                self.__pauseEmulator(False)
            # Save the state of the CHIP-8 CPU to a file
            if fname:
                pickle.dump(self.__chip8.getState(), open(fname, 'wb'))
        else:
            # Display error message
            QtWidgets.QMessageBox.information(self.__window,
                                              'Information',
                                              'Please load a ROM first ' +
                                              'before saving its state.',
                                              buttons=QtWidgets.QMessageBox.Ok)

    def __eventLoadState(self):
        '''Display an open file dialog and load the state of a previously saved
        state of the CHIP-8 system from the specified file.'''
        # Pause interpreter while dialog is shown
        self.__pauseEmulator()
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self.__window,
                                                         'Load State', '',
                                                         'Saved Data (*.sav)',
                                                         options=QtWidgets.
                                                         QFileDialog.
                                                         DontUseNativeDialog)
        # Resume interpreter when dialog is closed
        if not self.__pauseLock:
            self.__pauseEmulator(False)
        # Load the state of the CHIP-8 CPU from a file
        if fname:
            self.__chip8.setState(pickle.load(open(fname, 'rb')))
            self.__window.setStatusBar(self.__runStatus)
            self.__isRunning = True

    def __eventChangeBgColour(self):
        '''Change the current value of the GridFrame's pixel colour and save
        the updated setting.'''
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
        '''Change the current value of the GridFrame's background colour and
        save the updated setting.'''
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
        '''Pause the CHIP-8 system if it is current running, otherwise resume
        the state of the CHIP-8 system if it is paused.'''
        if self.__isRunning:
            self.__pauseLock = not self.__pauseLock
        self.__pauseEmulator(not self.__isPaused)

    def __eventReset(self):
        '''Reset the current state of the emulator by clearing all the pixels
        in GridFrame and restoring the CHIP-8 system to it's initial state.'''
        if self.__isRunning:
            self.__gridFrame.clearPixels()
            self.__chip8.reset()
            self.__window.setStatusBar(self.__defaultStatus)
            self.__isPaused = self.__isRunning = self.__pauseLock = False
            # Uncheck Pause menu option item
            self.__window.setCheckedMenuItem('Pause', False)

    def __eventAbout(self):
        '''Display an information dialog about the program languages and tools
        used to create this application and the name of the developer.'''
        # Pause interpreter while dialog is shown
        self.__pauseEmulator()
        message = 'Python CHIP-8 CPU Interpreter\n\nPython 3, PyQt 5\n' + \
            '\nCreated by Salinder Sidhu'
        # Render the message box
        QtWidgets.QMessageBox.information(self.__window,
                                          'About',
                                          message,
                                          buttons=QtWidgets.QMessageBox.Ok)
        # Resume interpreter when dialog is closed
        if not self.__pauseLock:
            self.__pauseEmulator(False)

    def __eventLoadROM(self):
        '''Display a open file dialog and load a ROM from the file specified
        into the CHIP-8 system.'''
        # Pause interpreter while dialog is shown
        self.__pauseEmulator()
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self.__window,
                                                         'Open File', '',
                                                         'All Files (*)',
                                                         options=QtWidgets.
                                                         QFileDialog.
                                                         DontUseNativeDialog)
        # Resume interpreter when dialog is closed
        if not self.__pauseLock:
            self.__pauseEmulator(False)
        # Load the CHIP-8 ROM if the fname exists
        try:
            if fname:
                self.__chip8.loadROM(fname)
                self.__window.setStatusBar(self.__runStatus)
                self.__isRunning = True
        except (Exception) as error:
            # Exception caught, display message and terminate
            self.__isRunning = False
            self.__showException(error)
            self.__window.close()


if __name__ == '__main__':
    # Pass command line arguments into application and launch it
    myApp = InterpreterApp(sys.argv)
    sys.exit(myApp.exec_())
