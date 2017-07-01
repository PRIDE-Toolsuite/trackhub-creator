# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 28-06-2017 9:50
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This module manages the configuration for the running pipeline
"""

# System modules
import os
import time
import json
import logging
import importlib
# Package modules
from exceptions import ConfigException, ConfigManagerException
import toolbox

# Application defaults - NORMAL OPERATION MODE
_folder_bin = os.path.abspath('bin')
_folder_config = os.path.abspath('config')
_folder_docs = os.path.abspath('docs')
_folder_logs = os.path.abspath('logs')
_folder_resources = os.path.abspath('resources')
_folder_run = os.path.abspath('run')
__configuration_file_name = None
__pipeline_name = None

# Logging defaults
_logger_formatters = {
    "DEBUG": "%(asctime)s [%(levelname)7s][%(name)48s][%(module)18s, %(lineno)4s] %(message)s",
    "INFO": "%(asctime)s [%(levelname)7s][%(name)48s] %(message)s"
}
_log_level = 'DEBUG'


def set_application_config_file(configuration_file):
    """
    This method sets the application wide configuration file that will be used
    :param configuration_file: config file name if the file is in the default configuration path or path to the
    configuration file if it is not.
    :return: no return value
    :exception: ConfigException is raised if there already is a configuration file set
    """
    global __configuration_file_name
    if __configuration_file_name is not None:
        raise ConfigException(
            "Configuration file can't be changed once an initial configuartion file has been provided")
    __configuration_file_name = configuration_file


def set_pipeline_name(pipeline_name):
    """
    Set the name of the pipeline being run, once it is set, it can't be changed, no matter how many times this method is
    called.
    :param pipeline_name: pipeline name
    :return: the current pipeline name
    """
    global __pipeline_name
    if __pipeline_name is None:
        __pipeline_name = pipeline_name
    return __pipeline_name


def get_pipeline_name():
    return set_pipeline_name("no_pipeline_name_specified")


# Configuration Singleton
__app_config_manager = None


def get_app_config_manager():
    """
    Singleton implementation of the Application Config Manager
    :return: the Application Configuration Manager
    """
    global __app_config_manager
    if __app_config_manager is None:
        __app_config_manager = AppConfigManager(read_config_from_file(__configuration_file_name), __configuration_file_name)
    return __app_config_manager


def read_config_from_file(configuration_file):
    """
    Given a file name or absolute path, read its configuration information in json format and return its object
    representation
    :param configuration_file: file name or absolute path for the file that contains the configuration information
    :return: an object representation of the json formatted configuration information read from the file
    """
    config_file_path = configuration_file
    if not os.path.isabs(config_file_path):
        config_file_path = os.path.join(_folder_config, configuration_file)
    try:
        return toolbox.read_json(config_file_path)
    except Exception as e:
        msg = "Config file " + str(config_file_path) + " could not be read, because " + str(e)
        raise ConfigException(msg)


def get_config_manager_for(configuration_file):
    """
    Factory method for Configuration Managers, used by modules of the running pipeline for their specific configuration
    files.
    :param configuration_file: configuration file name or path
    :return: a ConfigurationManager on top of that configuration information
    """
    return ConfigurationManager(read_config_from_file(configuration_file), configuration_file)


class ConfigurationManager:
    """
    This class is a helper class for those submodules having to manage configuration files themselves, that are specific
    to them
    """

    def __init__(self, configuration_object, configuration_file):
        self.__configuration_object = configuration_object
        self.__configuration_file = configuration_file

    def _get_value_for_key(self, key):
        if key in self.__configuration_object:
            return self.__configuration_object[key]
        else:
            msg = "Could not find '" + str(key) + "' in config file " + self.__configuration_file
            get_app_config_manager().get_logger().error(msg)
            raise ConfigManagerException(msg)

    def _get_value_for_key_with_default(self, key, default):
        if key in self.__configuration_object:
            return self.__configuration_object[key]
        else:
            return default

    def _get_configuration_object(self):
        return self.__configuration_object

    def _get_configuration_file(self):
        return self.__configuration_file


class AppConfigManager(ConfigurationManager):
    """
    Application wide Configuration Manager
    """

    def __init__(self, configuration_object, configuration_file):
        global _log_level
        global _logger_formatters
        super(AppConfigManager, self).__init__(configuration_object, configuration_file)
        # Session ID
        self.__session_id = time.strftime('%Y.%m.%d_%H.%M') + "-" + get_pipeline_name()
        # TODO config, folder_run, etc.
        self.__session_working_dir = os.path.abspath(os.path.join(self.get_folder_run(), self.get_session_id()))
        # TODO check and create folders (if needed)
        folders_to_check = [self.get_folder_bin(),
                            self.get_folder_logs(),
                            self.get_folder_resources(),
                            self.get_folder_run(),
                            self.get_session_working_dir(),
                            ]
        toolbox.check_create_folders(folders_to_check)
        # Prepare Logging subsystem
        if "loglevel" in configuration_object["logger"]:
            _log_level = configuration_object["logger"]["loglevel"]
        if "formatters" in configuration_object["logger"]["formatters"]:
            _logger_formatters = configuration_object["logger"]["formatters"]
        self.__log_handlers = []
        log_handlers_prefix = self.get_session_id() + '-'
        log_handlers_extension = '.log'
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(getattr(logging, _log_level))
        # TODO fix this code
        for llevel, lformat in _logger_formatters.items():
            logfile = os.path.join(self.get_folder_logs(), log_handlers_prefix + llevel.lower() + log_handlers_extension)
            lformatter = logging.Formatter(lformat)
            lhandler = logging.FileHandler(logfile, mode='w')
            lhandler.setLevel(getattr(logging, llevel))
            lhandler.setFormatter(lformatter)
            self.__log_handlers.append(lhandler)
            # Add the handlers to my own logger
            self.__logger.addHandler(lhandler)
        self._get_logger().debug("Logging system initialized")
        # TODO to be completed

    def get_folder_bin(self):
        # 'Bin' folder cannot be changed in this version of the pipeline
        return _folder_bin

    def get_folder_config(self):
        # Configuration folder cannot be changed in this version of the pipeline
        return _folder_config

    def get_folder_logs(self):
        # Configuration for logging folder cannot be changed in this version of the pipeline
        return _folder_logs

    def get_folder_resources(self):
        # Configuration for resources folder cannot be changed in this version of the pipeline
        return _folder_resources

    def get_folder_run(self):
        # Configuration for 'run' folder cannot be changed in this version of the pipeline
        return _folder_run

    def get_session_working_dir(self):
        return self.__session_working_dir

    def _get_log_handlers(self):
        return self.__log_handlers

    def get_logger_for(self, name):
        """
        Create a logger on demand
        :param name: name to be used in the logger
        :return: a new logger on that name
        """
        self._get_logger().debug("Creating logger with name {}".format(name))
        lg = logging.getLogger(name)
        for handler in self._get_log_handlers():
            lg.addHandler(handler)
        lg.setLevel(_log_level)
        return lg

    def _get_logger(self):
        # Get own logger
        return self.__logger

    def get_session_id(self):
        return self.__session_id

if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not met to be run in stand alone mode")