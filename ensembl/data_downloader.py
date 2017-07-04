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
__configuration_manager = None

def set_configuration_file(config_file):
    global __configuration_file
    if __configuration_file is None:
        __configuration_file = config_file
    return __configuration_file

if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
