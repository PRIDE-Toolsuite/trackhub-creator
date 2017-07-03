#
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 28-06-2017 10:13
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
#

"""
This module models an Ensembl service
"""

# App imports
import config_manager


# Ensembl Service configuration manager
class ConfigurationManager(config_manager.ConfigurationManager):
    # Configuration Keys
    _CONFIG_KEY_SERVICE = 'service'
    _CONFIG_KEY_ENSEMBL_API = 'ensembl_api'
    _CONFIG_KEY_SERVER = 'server'

    def __init__(self, configuration_object, configuration_file):
        super(ConfigurationManager, self).__init__(configuration_object, configuration_file)

    def get_api_server(self):
        try:
            self._get_configuration_object()[self._CONFIG_KEY_SERVICE]


# Ensembl Service model
class Service():
    def __init__(self, configuration_object, configuration_file):
        self.__config_manager = ConfigurationManager(configuration_object, configuration_file)
        # Ensembl Release Number
        self.__release_number = None

    def _get_config_manager(self):
        return self.__config_manager

    def __request_release_number(self):
        # TODO
        pass

    def get_release_number(self):
        """
        Get current Ensembl Release Number
        :return: current Ensembl Release Number
        """
        if self.__release_number is None:
            self.__request_release_number()
        return self.__release_number


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not met to be run in stand alone mode")
