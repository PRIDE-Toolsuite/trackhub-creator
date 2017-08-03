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

# TODO - Every module should have a configuration manager like this, refactor in the future, whenever you have time


# Configuration file and singleton instance
__configuration_file = None
__configuration_service = None


def set_configuration_file(config_file):
    global __configuration_file
    if __configuration_file is None:
        __configuration_file = config_file
    return __configuration_file
