# Filename: BotSettings.py
# Author: mfwass
# Date: January 8th, 2017
#
# The Legend of Pirates Online Software
# Copyright (c) The Legend of Pirates Online. All rights reserved.
#
# All use of this software is subject to the terms of the revised BSD
# license.  You should have received a copy of this license along
# with this source code in a file named "LICENSE."

from bot.core.BotGlobals import *

import json
import os

class BotSettings:
    """
    The BotSettings class will serve as a central location
    of all settings specified in an outside file.

    This class must be called each time a setting is checked.
    """

    def __init__(self):
        # Dict containing all settings.
        # This will be filled by settings.json.
        self.settings = {}

    def loadSettings(self, settingsFilename, override=False):
        """
        Loads settings from a settings file.
        """

        print(":BotSettings: Loading settings (%s)..." % settingsFilename)

        # Sanity check that the settings file exists.
        if not os.path.exists(settingsFilename):
            # This file does not exist.
            raise Exception("Settings file '%s' not found." % settingsFilename)

        # Open the settings for reading.
        s = open(settingsFilename, 'r')
        s = json.load(s)

        # Loop through each setting and set that
        # setting.
        for key, value in s.items():
            self.addSetting(key, value, override=override)

        # Print a debug print only if they are enabled.
        if self.getSetting('debug'):
            print(':BotSettings(debug): Loaded settings: %s' % self.getAllSettings())

    def getSetting(self, settingName):
        """
        Returns the setting for a specific key.
        """

        return self.settings.get(settingName)

    def hasSetting(self, settingName):
        """
        Checks if specific setting exists.
        """

        return settingName in self.getAllSettings().keys()

    def getAllSettings(self):
        """
        Returns a list of all settings.
        """

        return self.settings

    def addSetting(self, setting, newValue, override=False):
        """
        Adds a setting to our settings.
        """

        # Check whether or not we already have this setting.
        if self.hasSetting(setting):
            # This check already exists.  We can still replace
            # the prior check, but only if we're told we can.
            if not override:
                # User attempted to add a setting which already exists.
                # If they wish to do this, they must manually override
                # this check.  This may have been caused by a setting
                # being added twice to their settings.json file.
                raise Exception("Setting '%s' already exists."
                                "Did you add this setting twice?" % setting)
            else:
                # We are overriding a previous setting.  This could potentially
                # cause unwanted side effects, therefore we should warn the user
                # that they have overidden a prior setting.
                if not self.getSetting('suppessWarnings'):
                    print(":BotSettings(warning): Setting '%s' was overridden." % setting)

        # Add the setting.
        self.settings[setting] = newValue
