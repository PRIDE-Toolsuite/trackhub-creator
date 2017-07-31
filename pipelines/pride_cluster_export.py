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

import os
import time
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

    def get_cluster_file_exporter_version_parameter(self):
        """
        This method computes the 'version' parameter value for running pride cluster-file-exporter software, it usually
        looks like '2016-05'.

        This value is being computed here in case I want to make it either a configuration parameter or a command line
        argument
        :return: the 'version' parameter value to use for running pride cluster-file-exporter
        """
        return "{}-{:02}".format(time.gmtime().tm_year, time.gmtime().tm_mon)

    def get_cluster_file_exporter_destination_folder(self):
        return os.path.join(config_manager.get_app_config_manager().get_session_working_dir(), "cluster-file-exporter")


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
        # time java -Xmx12G -jar cluster-file-exporter-1.0.0-SNAPSHOT.jar -out ~/tmp/pride-cluster/with_pogo -version 2016-05 -quality 2 -filter_out_multitaxonomies -include_pogo_export > output.log 2>&1 ; cd ..
        # TODO
        # TODO - Run cluster file exporter
        # TODO -


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
