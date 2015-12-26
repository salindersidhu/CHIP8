import configparser

class Settings:
    ''''''

    def __init__(self, filename):
        ''''''
        # Settings variables
        self.__filename = filename
        self.__config = configparser.ConfigParser()
        # Load settings from existing file (if one exists)
        self.__isEmpty = len(self.__config.read(self.__filename)) == 0

    def isEmpty(self):
        ''''''
        return self.__isEmpty

    def addNewSetting(self, category, settingDict):
        ''''''
        self.__config[category] = settingDict.copy()
        self.__saveAllSettings()
        self.__isEmpty = False

    def getSetting(self, category, key):
        ''''''
        try:
            return self.__config[category][key]
        except KeyError:
            Exception('Cannot find setting data for category: ' + category + \
                      'and setting key: ' + key + '!')

    def editSetting(self, category, key, value):
        ''''''
        try:
            self.__config[category][key] = str(value) # Convert value to str
            self.__saveAllSettings()
        except KeyError:
            Exception('Cannot find setting data for category: ' + category + \
                      'and setting key: ' + key + '!')

    def __saveAllSettings(self):
        ''''''
        with open(self.__filename, 'w') as configFile:
            self.__config.write(configFile)
