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


# Logging defaults
_logger_formatters = {
	"DEBUG": "%(asctime)s [%(levelname)7s][%(name)48s][%(module)18s, %(lineno)4s] %(message)s",
	"INFO": "%(asctime)s [%(levelname)7s][%(name)48s] %(message)s"
}
_log_level = 'DEBUG'

