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

# Configuration file and configuration service singleton
__configuration_file = None
__configuration_service = None


def set_configuration_file(config_file):
    global __configuration_file
    if __configuration_file is None:
        __configuration_file = config_file
    return __configuration_file
