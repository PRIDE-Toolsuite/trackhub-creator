# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 01-07-2017 23:11
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This module implements the pipeline for exporting PRIDE Cluster to files using cluster-file-exporter, it will include
PoGo formatted files for its later use
"""

# App imports
import config_manager
import ensembl
from pipelines.template_pipeline import Director, DirectorConfigurationManager

__configuration_file = None
__pipeline_arguments = None
__pipeline_director = None


def set_configuration_file(config_file):
    global __configuration_file
    if __configuration_file is None:
        __configuration_file = config_file
    return __configuration_file


def set_pipeline_arguments(pipeline_arguments):
    global __pipeline_arguments
    if __pipeline_arguments is None:
        __pipeline_arguments = pipeline_arguments
    return __pipeline_arguments


class ConfigManager(DirectorConfigurationManager):
    def __init__(self, configuration_object, configuration_file, pipeline_arguments):
        super(ConfigManager, self).__init__(configuration_object, configuration_file, pipeline_arguments)


class PrideClusterExporter(Director):
    def __init__(self, configuration_object, configuration_file, pipeline_arguments):
        runner_id = "{}-{}".format(__name__, time.time())
        super(PrideClusterExporter, self).__init__(runner_id)
        self.__config_manager = ConfigManager(configuration_object, configuration_file, pipeline_arguments)

    def _get_configuration_manager(self):
        return self.__config_manager

    def _run_pipeline(self):
        # Main pipeline algorithm
        self._get_logger().info("[START]---> Pipeline run")
        # TODO


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
