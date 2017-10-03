# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 03-10-2017 13:47
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Module wide configuration management
"""

# Application imports
import config_manager

# Configuration file and configuration service singleton
__configuration_file = None
__configuration_service = None


def set_configuration_file(config_file):
    global __configuration_file
    if __configuration_file is None:
        __configuration_file = config_file
    return __configuration_file


def get_configuration_service():
    global __configuration_service
    if not __configuration_service:
        __configuration_service = ConfigurationService(config_manager.read_config_from_file(__configuration_file),
                                                       __configuration_file)
    return __configuration_service


class ConfigurationService(config_manager.ConfigurationManager):
    def __init__(self, configuration_object, configuration_file):
        super().__init__(configuration_object, configuration_file)
        self.logger = config_manager.get_app_config_manager() \
            .get_logger_for("{}.{}".format(__name__, type(self).__name__))

    def get_timeout_bed_to_bigbed(self):
        """
        Timeout for the conversion from bed to bigBed file format
        :return: timeout in seconds
        """
        return 3600

    def get_file_path_binary_bed_to_bigbed_conversion_tool(self):
        """
        Get absolute path to the binary tool to convert from 'bed' file to 'bigBed' file format
        :return: absolute path to 'bed to bigBed' conversion tool
        """
        pass


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
