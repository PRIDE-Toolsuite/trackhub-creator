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

import time
# Application imports
import config_manager
import ensembl
from toolbox import general
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
        self.__pipeline_arguments_object = {
            self._CONFIG_OBJECT_KEY_NCBI_TAXONOMY_IDS: id_list
        }

    def _get_pipeline_arguments_object(self):
        if self.__pipeline_arguments_object is None:
            self._process_pipeline_arguments()
        return self.__pipeline_arguments_object

    def get_ncbi_taxonomy_ids(self):
        return self._get_pipeline_arguments_object()[self._CONFIG_OBJECT_KEY_NCBI_TAXONOMY_IDS]


class EnsemblDataCollector(Director):
    def __init__(self, configuration_object, configuration_file, pipeline_arguments):
        runner_id = "{}-{}".format(__name__, time.time())
        super(EnsemblDataCollector, self).__init__(runner_id)
        self.__config_manager = ConfigManager(configuration_object, configuration_file, pipeline_arguments)

    def _get_configuration_manager(self):
        return self.__config_manager

    def _run_pipeline(self):
        # Main pipeline algorithm
        # TODO
        self._get_logger().info("[START]---> Pipeline run")
        self._get_logger().info("Collecting Ensembl data for NCBI Taxonomies: {}"
                                .format(",".join(self._get_configuration_manager().get_ncbi_taxonomy_ids())))
        ensembl_downloader_service = ensembl.data_downloader.get_data_download_service()
        for ncbi_taxonomy_id in self._get_configuration_manager().get_ncbi_taxonomy_ids():
            downloaded_protein_sequences = ensembl_downloader_service.get_protein_sequences_for_species(ncbi_taxonomy_id)
            downloaded_gtf_files = ensembl_downloader_service.get_genome_reference_for_species(ncbi_taxonomy_id)
        return True
