# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 03-08-2017 12:13
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Configuration manager for this module
"""

# Application imports
import config_manager

# TODO - Every module should have a configuration manager like this, refactor in the future, whenever you have time
# WARNING - Yes, I know, I've always called this 'Configuration Manager' and now I'm calling it 'Configuration Service',
# well, welcome to the wonderful world of 'I've changed my mind' in the land of 'refactoring' ^_^


# Configuration file and singleton instance
__configuration_file = None
__configuration_service = None


def set_configuration_file(config_file):
    global __configuration_file
    if __configuration_file is None:
        __configuration_file = config_file
    return __configuration_file


class ConfigurationService(config_manager.ConfigurationManager):
    def __init__(self, configuration_object, configuration_file):
        super(ConfigurationService, self).__init__(configuration_object, configuration_file)
        self.__logger = config_manager.get_app_config_manager().get_logger_for(__name__)

    def _get_logger(self):
        return self.__logger


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
