# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 17-08-2017 11:40
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
    pass
