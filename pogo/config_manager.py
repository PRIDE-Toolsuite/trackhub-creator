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


def get_configuration_service():
    global __configuration_service
    if not __configuration_service:
        __configuration_service = ConfigurationService(config_manager.read_config_from_file(__configuration_file),
                                                       __configuration_file)
    return __configuration_service


class ConfigurationService(config_manager.ConfigurationManager):
    # TODO - Externalize to a configuration file these configuration parameters
    _CONFIG_POGO_RESULT_FILE_EXTENSION_MAIN_BED = ".bed"
    _CONFIG_POGO_RESULT_FILE_EXTENSION_PATCH_HAPL_SCAFF_BED = "_patch_hapl_scaff.bed"
    _CONFIG_POGO_RESULT_FILE_EXTENSION_PATCH_HAPL_SCAFF_PTM_BED = "_patch_hapl_scaff_ptm.bed"
    _CONFIG_POGO_RESULT_FILE_EXTENSION_MAIN_PTM_BED = "_ptm.bed"

    def __init__(self, configuration_object, configuration_file):
        super(ConfigurationService, self).__init__(configuration_object, configuration_file)
        self.__logger = config_manager.get_app_config_manager().get_logger_for(__name__)

    def _get_logger(self):
        return self.__logger

    def get_pogo_result_file_extension_for_main_bed_file(self):
        return self._CONFIG_POGO_RESULT_FILE_EXTENSION_MAIN_BED

    def get_pogo_result_file_extension_for_main_ptm_bed_file(self):
        return self._CONFIG_POGO_RESULT_FILE_EXTENSION_MAIN_PTM_BED

    def get_pogo_run_timeout(self):
        """
        This method is duplicating the one at the application wide configuration manager at this stage and iteration
        of this application development with the idea of refactoring it out of the application wide configuration
        manager in the future, as this is a parameter that, even if it's configurable in the future, is within the
        responsiblity boundaries of the 'pogo' module. At this iteration of the software lifecycle, it just returns a
        default value, but later on, it can be made configurable as a parameter to this software.
        :return: configured timeout (seconds) for running PoGo
        """
        return config_manager.get_app_config_manager().get_pogo_run_timeout()

    def get_pogo_binary_file_path(self):
        """
        Again, at this iteration of the software lifecycle, it duplicates the method from the application wide
        configuration manager but, it belongs here, and this extra level of abstraction will help us in the process
        of refactoring the parameter.
        :return: absolute file path to the pogo binary
        """
        pass


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
