# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 01-07-2017 23:20
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This module runs PoGo for a file, using the given GTF and FA reference files, it will produce the results in the same
folder where the input file is located
"""

import config_manager
import toolbox

__configuration_file = None
__configuration_manager = None


def __get_configuration_manager():
    global __configuration_manager
    if __configuration_manager is None:
        __configuration_manager = DirectorConfigurationManager(toolbox.read_json(__configuration_file),
                                                               __configuration_file)
    return __configuration_manager


class DirectorConfigurationManager(config_manager.ConfigurationManager):
    def __init__(self, configuration_object, configuration_file):
        super(DirectorConfigurationManager, self).__init__(configuration_object, configuration_file)


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not met to be run in stand alone mode")
