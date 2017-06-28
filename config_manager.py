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
    # TODO
    pass


def __read_config_from_file(configuration_file):
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


def __check_create_folders(configuration_object):
    # TODO
    pass


def get_config_manager_for(configuration_file):
    """
    Factory method for Configuration Managers, used by modules of the running pipeline for their specific configuration
    files.
    :param configuration_file: configuration file name or path
    :return: a ConfigurationManager on top of that configuration information
    """
    return ConfigurationManager(__read_config_from_file(configuration_file), configuration_file)


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


class AppConfigManager:
    """
    Application wide Configuration Manager
    """

    def __init__(self, configuration_object):
        self.__configuration_object = configuration_object
        # TODO check and create folders (if needed)
        self.__session_id = time.strftime('%Y.%m.%d_%H.%M') + "-" + get_pipeline_name()
        # TODO to be completed
        pass

    def get_config_folder(self):
        # TODO
        pass

    def get_logger(self):
        # TODO
        pass
