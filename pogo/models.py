# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 02-08-2017 16:40
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This module contains models for dealing with PoGo stuff
"""

import os
import abc
import threading
# Application imports
import config_manager as main_app_config_manager
from parallel.models import ParallelRunner
from . import config_manager as module_config_manager
from .exceptions import PogoRunnerFactoryException, PogoRunnerException


class PogoRunResult:
    def __init__(self,
                 ncbi_taxonomy_id=None,
                 pogo_source_file_path=None,
                 protein_sequence_file_path=None,
                 gtf_file_path=None):
        """
        Just the constructor, I had this implemented as syntactic sugar, but I was wrong
        :param ncbi_taxonomy_id: ncbi taxonomy id for this PoGo run results
        :param pogo_source_file_path: path of the source file used to run PoGo
        """
        # Logging
        self.__logger = main_app_config_manager.get_app_config_manager().get_logger_for(
            "{}.{}".format(__name__, type(self).__name__))
        # Map<pogo_result_file_extension, pogo_result_file_path>
        self.__pogo_result_file_paths = {}
        self.__pogo_source_file_path = None
        # I knew this was going to give me trouble
        self.set_ncbi_taxonomy_id(ncbi_taxonomy_id)
        self.set_protein_sequence_file_path(protein_sequence_file_path)
        self.set_gtf_file_path(gtf_file_path)
        self.set_pogo_source_file_path(pogo_source_file_path)

    def __generate_pogo_result_file_paths(self, pogo_source_file_path):
        self.__pogo_result_file_paths = {}
        pogo_results_folder_path = os.path.dirname(pogo_source_file_path)
        pogo_source_file_name = os.path.basename(pogo_source_file_path)
        for root, dirs, files in os.walk(pogo_results_folder_path):
            for pogo_result_file_path in files:
                pogo_result_file_name = os.path.basename(pogo_result_file_path)
                if pogo_result_file_name.startswith(pogo_source_file_name) and (
                            pogo_result_file_name != pogo_source_file_name):
                    # It is file generated by PoGo
                    pogo_result_file_extension = pogo_result_file_name.split(pogo_source_file_name)[1]
                    # self.__pogo_result_file_paths[pogo_result_file_extension] = pogo_result_file_path
                    # I need the full path for the pogo result file path
                    self.__pogo_result_file_paths[pogo_result_file_extension] = os.path.join(pogo_results_folder_path,
                                                                                             pogo_result_file_path)
                    self._get_logger().info(
                        "PoGo run result '{}' ---> '{}', at full path '{}'".format(pogo_result_file_extension,
                                                                                   pogo_result_file_path,
                                                                                   self.__pogo_result_file_paths[
                                                                                       pogo_result_file_extension]))

    def __get_pogo_result_file_path(self, file_extension):
        if file_extension in self.__pogo_result_file_paths:
            return self.__pogo_result_file_paths[file_extension]
        return None

    def _get_logger(self):
        return self.__logger

    def set_ncbi_taxonomy_id(self, taxonomy_id):
        self.__ncbi_taxonomy_id = taxonomy_id

    def set_pogo_source_file_path(self, pogo_source_file_path):
        if not self.__pogo_source_file_path or (self.__pogo_source_file_path != pogo_source_file_path):
            self.__pogo_source_file_path = pogo_source_file_path
            # Regenerate pogo result file paths
            self.__generate_pogo_result_file_paths(pogo_source_file_path)

    def set_protein_sequence_file_path(self, protein_sequence_file_path):
        self.__protein_sequence_file_path = protein_sequence_file_path

    def set_gtf_file_path(self, gtf_file_path):
        self.__gtf_file_path = gtf_file_path

    def get_ncbi_taxonomy_id(self):
        return self.__ncbi_taxonomy_id

    def get_pogo_result_main_bed_file_path(self):
        return self.__get_pogo_result_file_path(
            module_config_manager.get_configuration_service().get_pogo_result_file_extension_for_main_bed_file())

    def get_pogo_result_main_ptm_bed_file_path(self):
        return self.__get_pogo_result_file_path(
            module_config_manager.get_configuration_service().get_pogo_result_file_extension_for_main_ptm_bed_file()
        )


# PoGo Runners
class PogoRunnerFactory:
    @staticmethod
    def get_pogo_runner(ncbi_taxonomy_id, pogo_input_file, protein_sequence_file_path, gtf_file_path):
        # TODO - In the future, more PoGo runners will be implemented
        return PogoRunnerLocalThread(ncbi_taxonomy_id, pogo_input_file, protein_sequence_file_path, gtf_file_path)


class PogoRunner(ParallelRunner):
    def __init__(self,
                 ncbi_taxonomy_id=None,
                 pogo_input_file=None,
                 protein_sequence_file_path=None,
                 gtf_file_path=None):
        super().__init__()
        self.ncbi_taxonomy_id = ncbi_taxonomy_id
        self.pogo_input_file = pogo_input_file
        self.protein_sequence_file_path = protein_sequence_file_path
        self.gtf_file_path = gtf_file_path

    def _validate_environment_for_running_pogo(self):
        return os.path.isfile(self.pogo_input_file) \
               and os.path.isfile(self.protein_sequence_file_path) \
               and os.path.isfile(self.gtf_file_path) \
               and os.path.isfile(module_config_manager.get_configuration_service().get_pogo_binary_file_path())

    def _get_pogo_run_command(self):
        pogo_parameter_species = ''
        if self.ncbi_taxonomy_id:
            pogo_parameter_species = " -species {} ".format(self.ncbi_taxonomy_id)
        pogo_command = "time {}{} -fasta {} -gtf {} -in {}" \
            .format(module_config_manager.get_configuration_service().get_pogo_binary_file_path(),
                    pogo_parameter_species,
                    self.protein_sequence_file_path,
                    self.gtf_file_path,
                    self.pogo_input_file)
        self._logger.debug("Command for running PoGo - '{}'".format(pogo_command))
        return pogo_command

    @abc.abstractmethod
    def _get_command_line_runner(self):
        """
        Although a factory is used to get a command line runner, its initialization differs depending on the final
        PogoRunner, i.e. we delegate to subclasses the provisioning of an initialized CommandLineRunner, how we use
        it, is the same for all subclasses
        :return: a CommandLineRunner for running PoGo
        """
        ...

    def _run(self):
        pass


class PogoRunnerLocalThread(PogoRunner):
    def __init__(self,
                 ncbi_taxonomy_id=None,
                 pogo_input_file=None,
                 protein_sequence_file_path=None,
                 gtf_file_path=None):
        super().__init__(ncbi_taxonomy_id, pogo_input_file, protein_sequence_file_path, gtf_file_path)
        self._logger = main_app_config_manager \
            .get_app_config_manager() \
            .get_logger_for("{}.{}-{}".format(__name__, type(self).__name__, threading.current_thread().getName()))

    def _get_command_line_runner(self):
        pass


class PogoRunnerHpc(PogoRunner):
    pass


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
