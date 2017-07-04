# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 03-07-2017 10:38
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This module implements en Ensembl data grabber for a given Ensembl Service instance
"""

# App imports
import config_manager
from exceptions import ConfigManagerException
from ensembl.service import Service as EnsemblService

# Common configuration for all instances of the download manager
__configuration_file = None
__data_download_service = None


def set_configuration_file(config_file):
    global __configuration_file
    if __configuration_file is None:
        __configuration_file = config_file
    return __configuration_file


def get_data_download_service():
    global __data_download_service
    if __data_download_service is None:
        __data_download_service = DataDownloadService(config_manager.read_config_from_file(__configuration_file),
                                                      __configuration_file)
    return __data_download_service


# Ensembl Data Grabbing Service configuration manager
class ConfigurationManager(config_manager.ConfigurationManager):
    def __init__(self, configuration_object, configuration_file):
        super(ConfigurationManager, self).__init__(configuration_object, configuration_file)
        self.__logger = config_manager.get_app_config_manager().get_logger_for(__name__)

    def _get_logger(self):
        return self.__logger


class DataDownloadService:
    """
    This Service is in charge of grabbing data (download) from Ensembl to a local repository
    """

    def __init__(self, configuration_object, configuration_file):
        self.__logger = config_manager.get_app_config_manager().get_logger_for(__name__)
        self._get_logger().debug("Using configuration file '{}'".format(configuration_file))


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
