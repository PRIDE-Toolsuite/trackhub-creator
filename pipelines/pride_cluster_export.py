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
import subprocess
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
    _CONFIG_CLUSTER_FILE_EXPORTER_WORKING_SUBDIR = "cluster-file-exporter"
    _CONFIG_CLUSTER_FILE_EXPORTER_BIN_SUBFOLDER = "cluster-file-exporter"
    _CONFIG_CLUSTER_FILE_EXPORTER_JAR_FILE_NAME = "cluster-file-exporter.jar"

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
        """
        Get the destination folder for the cluster file exporter result files, it will typically be a subfolder of the
        current running session working directory.

        This is computed here just in case I want to make it either a configuration parameter or a command line argument
        in the near future
        :return: destination folder for pride cluster-file-exporter result files
        """
        return os.path.join(config_manager.get_app_config_manager().get_session_working_dir(),
                            self._CONFIG_CLUSTER_FILE_EXPORTER_WORKING_SUBDIR)

    def get_cluster_file_exporter_quality_parameter(self):
        """
        Get the value for the 'quality' parameter of 'cluster-file-exporter'

        This is computed here just in case I want to make it either a configuration parameter or a command line argument
        in the near future
        :return: 'quality' parameter value for running pride cluster-file-exporter
        """
        return '2'

    def get_cluster_file_exporter_java_max_memory(self):
        """
        Get the maximum amount of memory we want Java to use for running pride cluster-file-exporter

        This is computed here just in case I want to make it either a configuration parameter or a command line argument
        in the near future
        :return: maximum amount of memory to append to -Xmx java parameter
        """
        return '12G'

    def get_cluster_file_exporter_jar_path(self):
        """
        Get the path to cluster-file-exporter jar file for running the software

        This is computed here just in case I want to make it either a configuration parameter or a command line argument
        in the near future
        :return: cluster-file-exporter jar file path
        """
        return os.path.join(config_manager.get_app_config_manager().get_folder_bin(),
                            os.path.join(self._CONFIG_CLUSTER_FILE_EXPORTER_BIN_SUBFOLDER,
                                         self._CONFIG_CLUSTER_FILE_EXPORTER_JAR_FILE_NAME))

    def get_cluster_file_exporter_output_log_file_path(self):
        """
        Get the path to the file where all output from running cluster-file-exporter will be dumped to.

        This is computed here just in case I want to make it either a configuration parameter or a command line argument
        in the near future
        :return: cluster-file-exporter output log file path
        """
        return os.path.join(self.get_cluster_file_exporter_destination_folder(),
                            "output.log")

    def get_cluster_file_exporter_run_timeout(self):
        """
        Get how much time, in seconds, to wait before considering the run of cluster-file-exporter overtimed.

        This is computed here just in case I want to make it either a configuration parameter or a command line argument
        in the near future
        :return: timeout for cluster-file-exporter command
        """
        return 7200


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
        # Build cluster-file-exporter command
        cluster_file_exporter_command = \
            "time java -Xmx{} -jar {} -out {} -version {} -quality {} " \
            "-filter_out_multitaxonomies -include_pogo_export > {} 2>&1".format(
                self._get_configuration_manager().get_cluster_file_exporter_java_max_memory(),
                self._get_configuration_manager().get_cluster_file_exporter_jar_path(),
                self._get_configuration_manager().get_cluster_file_exporter_destination_folder(),
                self._get_configuration_manager().get_cluster_file_exporter_version_parameter(),
                self._get_configuration_manager().get_cluster_file_exporter_quality_parameter(),
                self._get_configuration_manager().get_cluster_file_exporter_output_log_file_path()
            )
        # Run cluster file exporter
        cluster_file_exporter_subprocess = subprocess.Popen(cluster_file_exporter_command,
                                                            shell=True)
        

if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
