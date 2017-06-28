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
from exceptions import ConfigException


# Application defaults - NORMAL OPERATION MODE
_folder_bin = os.path.abspath('bin')
_folder_config = os.path.abspath('config')
_folder_docs = os.path.abspath('docs')
_folder_logs = os.path.abspath('logs')
_folder_resources = os.path.abspath('resources')
__configuration_file_name = None


# Logging defaults
_logger_formatters = {
	"DEBUG": "%(asctime)s [%(levelname)7s][%(name)48s][%(module)18s, %(lineno)4s] %(message)s",
	"INFO": "%(asctime)s [%(levelname)7s][%(name)48s] %(message)s"
}
_log_level = 'DEBUG'


def set_application_config_file(configuration_file):
	"""
	This method sets the application wide configuration file that will be used
	:param configuration_file: config file name if the file is in the default configuration path or path to the configuration file if it is not
	:return: no return value
	:exception: ConfigException is raised if there already is a configuration file set
	"""
	global __configuration_file_name
	if __configuration_file_name is not None:
		raise ConfigException("Configuration file can't be changed once an initial configuartion file has been provided")
	__configuration_file_name = configuration_file


# Configuration Singleton
__config_manager = None


def __read_configuration(configuration_file):
	# TODO
	pass


def get_manager():
	# TODO
	pass
