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
from ensembl.models import SpeciesService
from exceptions import ConfigManagerException
from toolbox import rest

# Ensembl Service is going to be a Singleton, unique for the running session
__configuration_file = None
__service_instance = None


def set_configuration_file(config_file):
    global __configuration_file
    if __configuration_file is None:
        __configuration_file = config_file
    return __configuration_file


def get_service():
    global __service_instance
    if __service_instance is None:
        __service_instance = Service(config_manager.read_config_from_file(__configuration_file), __configuration_file)
    return __service_instance


# Ensembl Service configuration manager
class ConfigurationManager(config_manager.ConfigurationManager):
    # Configuration Keys
    _CONFIG_KEY_SERVICE = 'service'
    _CONFIG_KEY_ENSEMBL_API = 'ensembl_api'
    _CONFIG_KEY_SERVER = 'server'

    def __init__(self, configuration_object, configuration_file):
        super(ConfigurationManager, self).__init__(configuration_object, configuration_file)
        self._logger = config_manager.get_app_config_manager()\
            .get_logger_for("{}.{}".format(__name__, type(self).__name__))

    def get_api_server(self):
        self._logger.debug(
            "get_api_server, from configuration object '{}'".format(self._get_configuration_object()))
        try:
            return self._get_configuration_object()[self._CONFIG_KEY_SERVICE][self._CONFIG_KEY_ENSEMBL_API][
                self._CONFIG_KEY_SERVER]
        except Exception as e:
            raise ConfigManagerException(
                "MISSING information about Ensembl '{}.{}.{}' API server in configuration file '{}'".format(
                    self._CONFIG_KEY_SERVICE,
                    self._CONFIG_KEY_ENSEMBL_API,
                    self._CONFIG_KEY_SERVER,
                    self._get_configuration_file()))


# Ensembl Service model
class Service:
    def __init__(self, configuration_object, configuration_file):
        self._logger = config_manager.get_app_config_manager()\
            .get_logger_for("{}.{}".format(__name__, type(self).__name__))
        self._logger.debug("Using configuration file '{}'".format(configuration_file))
        self.__config_manager = ConfigurationManager(configuration_object, configuration_file)
        # Ensembl Release Number
        self.__release_number = None
        # Ensembl Species Data
        self.__species_data_service = None

    def __request_release_number(self):
        request_url = self._get_config_manager().get_api_server() + "/info/data/?"
        current_release_data = rest.make_rest_request(request_url)
        self._logger.debug("Request Release Number response from Ensembl - '{}'".format(current_release_data))
        self._logger.info(
            "This session is working with Ensembl Release {}".format(current_release_data['releases'][0]))
        return current_release_data['releases'][0]

    def __request_species_data(self):
        request_url = self._get_config_manager().get_api_server() + "/info/species?"
        self._logger.debug("Requesting Species Data to Ensembl, url '{}'".format(request_url))
        return rest.make_rest_request(request_url)

    def _get_config_manager(self):
        return self.__config_manager

    def get_release_number(self):
        """
        Get current Ensembl Release Number
        :return: current Ensembl Release Number
        """
        if self.__release_number is None:
            self.__release_number = self.__request_release_number()
        return self.__release_number

    def get_species_data_service(self):
        if self.__species_data_service is None:
            self.__species_data_service = SpeciesService(self.__request_species_data())
        return self.__species_data_service


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
