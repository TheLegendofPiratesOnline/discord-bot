from bot.base.BotGlobals import *
import json
import os

class BotSettings:
    def __init__(self):
        self.settings = {}

    def loadSettings(self, settingsFilename, override=False):
        print(":BotSettings: Loading settings (%s)..." % settingsFilename)
        if not os.path.exists(settingsFilename):
            raise Exception("Settings file '%s' not found." % settingsFilename)

        s = open(settingsFilename, 'r')
        s = json.load(s)

        for key, value in s.items():
            self.addSetting(key, value, override=override)

        if self.getSetting('debug'):
            print(':BotSettings(debug): Loaded settings: %s' % self.getAllSettings())

    def getSetting(self, settingName):
        return self.settings.get(settingName)

    def hasSetting(self, settingName):
        return settingName in self.getAllSettings().keys()

    def getAllSettings(self):
        return self.settings

    def addSetting(self, setting, newValue, override=False):
        if self.hasSetting(setting):
            if not override:
                raise Exception("Setting '%s' already exists. Did you add this setting twice?" % setting)
            else:
                if not self.getSetting('suppessWarnings'):
                    print(":BotSettings(warning): Setting '%s' was overridden." % setting)

        self.settings[setting] = newValue
