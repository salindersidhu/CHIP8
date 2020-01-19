import configparser


class Settings:
    '''The Settings class is a wrapper for configparser and it's functions.
    This class simplifies the tasks of loading, storing and manipulating
    settings data.'''

    def __init__(self, filename):
        '''Create a new Settings object with a specific file name.'''
        # Exceptions
        self.__settingException = Exception(
            'Cannot find specified setting data!')
        # Settings variables
        self.__filename = filename
        self.__config = configparser.ConfigParser()
        # Load settings from existing file (if one exists)
        self.__isEmpty = len(self.__config.read(self.__filename)) == 0

    def isEmpty(self):
        '''Return True if there is not settings data loaded, otherwise return
        False.'''
        return self.__isEmpty

    def addNewSetting(self, category, settingDict):
        '''Add a new setting with the specified category and data. Save the new
        settings data to a file.'''
        self.__config[category] = settingDict.copy()
        self.__saveAllSettings()
        self.__isEmpty = False

    def getSetting(self, category, key):
        '''Return a setting value from the specified category and setting
        key.'''
        try:
            return self.__config.get(category, key)
        except KeyError:
            raise self.__settingException

    def editSetting(self, category, key, value):
        '''Change an existing setting with a specified category and setting key
        to the value specified. Save the new settings data to a file.'''
        try:
            self.__config.set(category, key, str(value))
            self.__saveAllSettings()
        except KeyError:
            raise self.__settingException

    def __saveAllSettings(self):
        '''Write the current settings data to a file.'''
        with open(self.__filename, 'w') as configFile:
            self.__config.write(configFile)
