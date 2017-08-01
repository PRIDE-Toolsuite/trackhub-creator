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
import ensembl.data_downloader
from toolbox import general as general_toolbox
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


def get_pipeline_director():
    global __pipeline_director
    if __pipeline_director is None:
        __pipeline_director = PrideClusterExporter(config_manager.read_config_from_file(__configuration_file),
                                                   __configuration_file,
                                                   __pipeline_arguments)
    return __pipeline_director


class ConfigManager(DirectorConfigurationManager):
    _CONFIG_CLUSTER_FILE_EXPORTER_WORKING_SUBDIR = "cluster-file-exporter"
    _CONFIG_CLUSTER_FILE_EXPORTER_BIN_SUBFOLDER = "cluster-file-exporter"
    _CONFIG_CLUSTER_FILE_EXPORTER_JAR_FILE_NAME = "cluster-file-exporter.jar"
    _CONFIG_POGO_BIN_SUBFOLDER = "pogo"
    _CONFIG_POGO_BIN_FILE_NAME = "pogo"

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
        destination_folder = os.path.join(config_manager.get_app_config_manager().get_session_working_dir(),
                                          self._CONFIG_CLUSTER_FILE_EXPORTER_WORKING_SUBDIR)
        # Make sure the folder is there
        general_toolbox.check_create_folders([destination_folder])
        return destination_folder

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

    def get_cluster_file_exporter_result_file_name_prefix(self):
        """
        Get the prefix cluster-file-exporter uses for result file names.

        This is computed here just in case I want to make it either a configuration parameter or a command line argument
        in the near future
        :return: file name prefix for cluster-file-exporter result files
        """
        return "pride_cluster_peptides_"

    def get_cluster_file_exporter_result_file_extension(self):
        """
        Get the result file extension used in the files produced by the cluster-file-exporter

        This is computed here just in case I want to make it either a configuration parameter or a command line argument
        in the near future
        :return: cluster-file-exporter result file extension
        """
        return "tsv"

    def get_cluster_file_exporter_pogo_file_extension(self):
        """
        Get the file extension for the pogo files produced by the cluster-file-exporter

        This is computed here just in case I want to make it either a configuration parameter or a command line argument
        in the near future
        :return: cluster-file-exporter 'pogo' file extension
        """
        return "pogo"

    def get_pogo_binary_file_path(self):
        """
        Get the file path to PoGo binary.

        This is computed here just in case I want to make it either a configuration parameter or a command line argument
        in the near future
        :return: PoGo binary file path
        """
        return os.path.join(config_manager.get_app_config_manager().get_folder_bin(),
                            os.path.join(self._CONFIG_POGO_BIN_SUBFOLDER,
                                         self._CONFIG_POGO_BIN_FILE_NAME))


class PrideClusterExporter(Director):
    __CLUSTER_FILE_EXPORTER_RESULT_MAP_KEY_POGO_FILE_PATH = 'pogo_file_path'
    __CLUSTER_FILE_EXPORTER_RESULT_MAP_KEY_PRIDE_CLUSTER_FILE_PATH = 'pride_cluster_file_path'
    __CLUSTER_FILE_EXPORTER_TAXONOMY_KEY_ALL = 'all'

    def __init__(self, configuration_object, configuration_file, pipeline_arguments):
        runner_id = "{}-{}".format(__name__, time.time())
        super(PrideClusterExporter, self).__init__(runner_id)
        self.__config_manager = ConfigManager(configuration_object, configuration_file, pipeline_arguments)

    def _get_configuration_manager(self):
        return self.__config_manager

    def _process_cluster_file_exporter_result_files(self):
        cluster_file_exporter_folder = self._get_configuration_manager().get_cluster_file_exporter_destination_folder()
        # Prepare empty result map
        cluster_file_exporter_result_mapping = {}
        for root, dirs, files in \
                os.walk(cluster_file_exporter_folder):
            for file in files:
                if file.startswith(
                        self._get_configuration_manager().get_cluster_file_exporter_result_file_name_prefix()):
                    self._get_logger().info("Mapping result file '{}'".format(file))
                    result_file_path = os.path.join(cluster_file_exporter_folder, file)
                    # Taxonomy corner case 'pride_cluster_peptides_ALL.tsv'
                    result_file_taxonomy = self.__CLUSTER_FILE_EXPORTER_TAXONOMY_KEY_ALL
                    if 'ALL' not in file:
                        result_file_taxonomy = \
                            file.split(self._get_configuration_manager()
                                       .get_cluster_file_exporter_result_file_name_prefix())[1].split('_')[0]
                    result_file_extension = file[file.rfind('.') + 1:]
                    # Check the taxonomy for the result map
                    if result_file_taxonomy not in cluster_file_exporter_result_mapping:
                        cluster_file_exporter_result_mapping[result_file_taxonomy] = {}
                    # Check the file extension - cluster-file-exporter result file
                    if result_file_extension == self._get_configuration_manager() \
                            .get_cluster_file_exporter_result_file_extension():
                        if self.__CLUSTER_FILE_EXPORTER_RESULT_MAP_KEY_PRIDE_CLUSTER_FILE_PATH in \
                                cluster_file_exporter_result_mapping[result_file_taxonomy]:
                            self._get_logger().error("DUPLICATED entry for file '{}'".format(file))
                            return None
                        cluster_file_exporter_result_mapping[result_file_taxonomy][
                            self.__CLUSTER_FILE_EXPORTER_RESULT_MAP_KEY_PRIDE_CLUSTER_FILE_PATH] = result_file_path
                    # Check the file extension - cluster-file-exporter PoGo file
                    if result_file_extension == self._get_configuration_manager() \
                            .get_cluster_file_exporter_pogo_file_extension():
                        if self.__CLUSTER_FILE_EXPORTER_RESULT_MAP_KEY_POGO_FILE_PATH in \
                                cluster_file_exporter_result_mapping[result_file_taxonomy]:
                            self._get_logger().error("DUPLICATED entry for file '{}'".format(file))
                            return None
                        cluster_file_exporter_result_mapping[result_file_taxonomy][
                            self.__CLUSTER_FILE_EXPORTER_RESULT_MAP_KEY_POGO_FILE_PATH] = result_file_path
                else:
                    self._get_logger().warning("Ignoring cluster-file-exporter non-result file '{}'".format(file))
        return cluster_file_exporter_result_mapping

    def __run_cluster_file_exporter(self):
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
        self._get_logger().info("cluster-file-exporter command: '{}'".format(cluster_file_exporter_command))
        # Run cluster file exporter
        cluster_file_exporter_subprocess = subprocess.Popen(cluster_file_exporter_command,
                                                            shell=True)
        try:
            stdout, stderr = \
                cluster_file_exporter_subprocess.communicate(
                    timeout=self._get_configuration_manager().get_cluster_file_exporter_run_timeout())
        except subprocess.TimeoutExpired as e:
            self._get_logger().error("TIMEOUT ({} seconds) while running cluster-file-exporter, KILLING subprocess")
            cluster_file_exporter_subprocess.kill()
            stdout, stderr = cluster_file_exporter_subprocess.communicate()
            return False
        if cluster_file_exporter_subprocess.poll() and (cluster_file_exporter_subprocess != 0):
            self._get_logger().error("An ERROR occurred while running cluster-file-exporter")
            return False
        return True

    def __run_cluster_file_exporter_simulation(self):
        cluster_file_exporter_destination_folder = self\
            ._get_configuration_manager()\
            .get_cluster_file_exporter_destination_folder()
        

    def _run_pipeline(self):
        # Main pipeline algorithm
        self._get_logger().info("[START]---> Pipeline run")
        # Run cluster-file-exporter
        if not self.__run_cluster_file_exporter():
            return False
        # Process cluster-file-exporter result files
        cluster_file_exporter_result_mapping = self._process_cluster_file_exporter_result_files()
        if not cluster_file_exporter_result_mapping:
            self._get_logger().error("ERROR processing cluster-file-exporter result files")
            return False
        # Get an instance of the Ensembl data downloader
        ensembl_downloader_service = ensembl.data_downloader.get_data_download_service()
        for taxonomy in cluster_file_exporter_result_mapping:
            if taxonomy == self.__CLUSTER_FILE_EXPORTER_TAXONOMY_KEY_ALL:
                self._get_logger().warning("SKIPPING PoGo for taxonomy {}".format(taxonomy))
                continue
            # PoGo input file
            pogo_file = cluster_file_exporter_result_mapping[taxonomy][
                self.__CLUSTER_FILE_EXPORTER_RESULT_MAP_KEY_POGO_FILE_PATH]
            self._get_logger().info(
                "Processing taxonomy '{}' for PoGo file '{}'"
                .format(taxonomy,
                        pogo_file))
            # TODO - Get Protein Sequence file from Ensembl for this taxonomy, only the "*all*" kind
            # TODO - Get the more general GTF file from Ensembl for this taxonomy
            # TODO - Run PoGo
            # TODO - Convert files to BigBed format
        # TODO - Create trackhub structure
        # TODO - Sync Data and get public URL
        # TODO - Publish trackhub
        return True


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
