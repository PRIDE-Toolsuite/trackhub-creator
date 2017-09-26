# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 26-07-2017 12:29
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This pipeline collects data from Ensembl to avoid race conditions when running other pipelines that use this data
"""

import os
import time
# Application imports
import config_manager
import ensembl
from pipelines.template_pipeline import DirectorConfigurationManager, Director

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
        __pipeline_director = EnsemblDataCollector(config_manager.read_config_from_file(__configuration_file),
                                                   __configuration_file,
                                                   __pipeline_arguments)
    return __pipeline_director


class ConfigManager(DirectorConfigurationManager):
    _CONFIG_OBJECT_KEY_NCBI_TAXONOMY_IDS = 'ncbi_taxonomy_ids'

    def __init__(self, configuration_object, configuration_file, pipeline_arguments):
        super(ConfigManager, self).__init__(configuration_object, configuration_file, pipeline_arguments)
        self.__pipeline_arguments_object = None

    def _process_pipeline_arguments(self):
        # Pipeline arguments for this pipeline are like: "ncbi_taxonomy_ids=id,id,id"
        id_list = []
        if self._get_pipeline_arguments():
            id_list = self._get_pipeline_arguments().split('=')[1].split(',')
        return {
            self._CONFIG_OBJECT_KEY_NCBI_TAXONOMY_IDS: id_list
        }

    def get_ncbi_taxonomy_ids(self):
        return self._get_pipeline_arguments_object()[self._CONFIG_OBJECT_KEY_NCBI_TAXONOMY_IDS]


class EnsemblDataCollector(Director):
    """
    This pipeline collects data from the latest Ensembl release for the given taxonomies
    """
    def __init__(self, configuration_object, configuration_file, pipeline_arguments):
        runner_id = "{}-{}".format(__name__, time.time())
        super(EnsemblDataCollector, self).__init__(runner_id)
        self.__config_manager = ConfigManager(configuration_object, configuration_file, pipeline_arguments)

    def _get_configuration_manager(self):
        return self.__config_manager

    def __check_downloaded_files(self, files_names_and_paths):
        result = True
        for file_name, file_path in files_names_and_paths:
            if not os.path.exists(file_path):
                result = False
                self._get_logger().error("MISSING ENSEMBL file '{}' at '{}'".format(file_name, file_path))
        return result

    def _run_pipeline(self):
        # TODO - I can easily parallelize this using the parallel module
        # Main pipeline algorithm
        self._get_logger().info("[START]---> Pipeline run")
        self._get_logger().info("Collecting Ensembl data for NCBI Taxonomies: {}"
                                .format(",".join(self._get_configuration_manager().get_ncbi_taxonomy_ids())))
        ensembl_downloader_service = ensembl.data_downloader.get_data_download_service()
        for ncbi_taxonomy_id in self._get_configuration_manager().get_ncbi_taxonomy_ids():
            downloaded_protein_sequences = ensembl_downloader_service \
                .get_protein_sequences_for_species(ncbi_taxonomy_id)
            downloaded_gtf_files = ensembl_downloader_service \
                .get_genome_reference_for_species(ncbi_taxonomy_id)
            if not downloaded_protein_sequences:
                self._get_logger().error("MISSING protein sequence data for taxonomy ID #{}".format(ncbi_taxonomy_id))
            else:
                self.__check_downloaded_files(downloaded_protein_sequences)
            if not downloaded_gtf_files:
                self._get_logger().error("MISSING genome reference data for taxonomy ID #{}".format(ncbi_taxonomy_id))
            else:
                self.__check_downloaded_files(downloaded_gtf_files)
        return True


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
