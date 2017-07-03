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
    def __init__(self, configuration_object, configuration_file):
        super(ConfigurationManager, self).__init__(configuration_object, configuration_file)


# Ensembl Service model
class EnsemblService():
    def __init__(self, configuration_object, configuration_file):
        self.__config_manager = ConfigurationManager(configuration_object, configuration_file)

    def _get_config_manager(self):
        return self.__config_manager


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not met to be run in stand alone mode")
