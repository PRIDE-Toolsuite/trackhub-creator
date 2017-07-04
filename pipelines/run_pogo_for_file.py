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

# App imports
import config_manager
import toolbox
import pipelines.template_pipeline as template_pipeline

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


# Pipeline Director
class Director(template_pipeline.Director):
    def __init__(self, config_file_name, runner_id=0):
        super(Director, self).__init__(config_file_name, runner_id)
        self._set_logger(config_manager.get_app_config_manager().get_logger_for(__name__))

    def _run_pipeline(self):
        # TODO
        pass


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
