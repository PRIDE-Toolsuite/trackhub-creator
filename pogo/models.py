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
from parallel.models import ParallelRunner, CommandLineRunnerFactory
from parallel.exceptions import CommandLineRunnerException
from . import config_manager as module_config_manager
from .exceptions import PogoRunnerException


class PogoRunResult:
    # TODO - Needs to be extended for abstracting from results files from '-mm' parameter use
    # TODO - This needs refactoring to make it pythonist compliant
    def __init__(self,
                 ncbi_taxonomy_id=None,
                 pogo_source_file_path=None,
                 protein_sequence_file_path=None,
                 gtf_file_path=None,
                 pogo_runner=None):
        """
        Just the constructor, I had this implemented as syntactic sugar, but I was wrong
        :param ncbi_taxonomy_id: ncbi taxonomy id for this PoGo run results
        :param pogo_source_file_path: path of the source file used to run PoGo
        :param protein_sequence_file_path: FASTA file
        :param gtf_file_path: GTF file
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
        self.__pogo_runner = None

    @property
    def pogo_runner(self):
        return self.__pogo_runner

    @pogo_runner.setter
    def pogo_runner(self, pogo_runner):
        if not self.__pogo_runner or (self.__pogo_runner != pogo_runner):
            self.__pogo_runner = pogo_runner
            # Regenerate pogo result file paths
            self.__generate_pogo_result_file_paths(pogo_runner.pogo_input_file)

    @property
    def ncbi_taxonomy_id(self):
        return self.pogo_runner.ncbi_taxonomy_id

    @property
    def protein_sequence_file_path(self):
        return self.pogo_runner.protein_sequence_file_path

    @property
    def gtf_file_path(self):
        return self.pogo_runner.gtf_file_path

    def __generate_pogo_result_file_paths(self, pogo_source_file_path):
        """
        Given a full path to a source file, e.g. /nfs/fullpath/PXD001110-9606.pogo, and the fact that PoGo generates
        result files by appending to the source file name different extensions, e.g.
            PXD001110-9606.pogo.bed
            PXD001110-9606.pogo.gct
            PXD001110-9606.pogo_no-ptm.bed
            PXD001110-9606.pogo_out.gtf
            PXD001110-9606.pogo_patch_hapl_scaff.bed
            PXD001110-9606.pogo_patch_hapl_scaff.gct
            PXD001110-9606.pogo_patch_hapl_scaff_no-ptm.bed
            PXD001110-9606.pogo_patch_hapl_scaff_out.gtf
            PXD001110-9606.pogo_patch_hapl_scaff_ptm.bed
            PXD001110-9606.pogo_ptm.bed
            PXD001110-9606.pogo_ptm_sorted.bed
            PXD001110-9606.pogo_sorted.bed
            PXD001110-9606.pogo_unmapped.txt
        being the extensions: .bed, .gct, _no-ptm.bed, _out.gtf, _patch_hapl_scaff.bed ... etc.
        This method collects all the result files based on being them files that start with the source file name
        'PXD001110-9606.pogo', and it will create a map (file_suffix, file_full_path), e.g.
            {
                ...
                '_patch_hapl_scaff.bed': '/nfs/fullpath/PXD001110-9606.pogo_patch_hapl_scaff.bed'
                ...
            }
        This means, for the current use case where we could be running PoGo specifying parameters like '-mm' that will
        produce files with different (extended) suffixes, e.g. _1MM_patch_hapl_scaff.bed, in the same folder as other
        PoGo runners with different parameters, this method will also map the other runners result files available at
        the time of performing the file system scan. THIS IS PERFECTLY OK, DON'T PANIC, because whe you use the getters
        for full paths to the result files for a particular runner, only the ones belonging to that runner will be
        picked up from the map, e.g. if this is a runner with '-mm' parameter active, only those '_1MM_*" files will be
        returned as result.
        :param pogo_source_file_path:
        :return:
        """
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
    def get_pogo_runner(ncbi_taxonomy_id, pogo_input_file, protein_sequence_file_path, gtf_file_path, mm_gap=None):
        # TODO - In the future, more PoGo runners will be implemented
        return PogoRunnerLocalThread(ncbi_taxonomy_id,
                                     pogo_input_file,
                                     protein_sequence_file_path,
                                     gtf_file_path,
                                     mm_gap)


class PogoRunner(ParallelRunner):
    def __init__(self,
                 ncbi_taxonomy_id=None,
                 pogo_input_file=None,
                 protein_sequence_file_path=None,
                 gtf_file_path=None,
                 mm_gap=None):
        super().__init__()
        self.ncbi_taxonomy_id = ncbi_taxonomy_id
        self.pogo_input_file = pogo_input_file
        self.protein_sequence_file_path = protein_sequence_file_path
        self.gtf_file_path = gtf_file_path
        self.mm_gap = mm_gap
        self._stdout = b' '
        self._stderr = b' '
        self.__success = True
        self.__pogo_run_result = None

    def _set_failed_to_run_pogo(self):
        self.__success = False

    def _set_success_to_run_pogo(self):
        self.__success = self.__success and True

    def _validate_environment_for_running_pogo(self):
        validation_ok = True
        if not self.ncbi_taxonomy_id:
            self._logger.warning("NO NCBI TAXONOMY ID has been specified for running PoGo with input file '{}'"
                                 .format(self.pogo_input_file))
        if not os.path.isfile(self.pogo_input_file):
            self._logger.error("PoGo input file '{}' IS NOT VALID".format(self.pogo_input_file))
            validation_ok = False
        if not os.path.isfile(self.protein_sequence_file_path):
            self._logger.error("Protein sequence file '{}' IS NOT VALID".format(self.protein_sequence_file_path))
            validation_ok = False
        if not os.path.isfile(self.gtf_file_path):
            self._logger.error("GTF file '{}' IS NOT VALID".format(self.gtf_file_path))
            validation_ok = False
        if not os.path.isfile(module_config_manager.get_configuration_service().get_pogo_binary_file_path()):
            self._logger.error("PoGo binary file '{}' IS NOT VALID"
                               .format(module_config_manager.get_configuration_service().get_pogo_binary_file_path()))
            validation_ok = False
        return validation_ok

    def get_stdout(self):
        # Never give it back until the runner is done with whatever it is doing
        if not self._done:
            raise PogoRunnerException("PoGo Runner is NOT DONE doing its job, thus 'stdout' is NOT AVAILABLE")
        return self._stdout

    def get_stderr(self):
        # Never give it back until the runner is done with whatever it is doing
        if not self._done:
            raise PogoRunnerException("PoGo Runner is NOT DONE doing its job, thus 'stderr' is NOT AVAILABLE")
        return self._stderr

    def get_pogo_run_command(self):
        pogo_parameter_species = ''
        if self.ncbi_taxonomy_id:
            pogo_parameter_species = " -species {} ".format(self.ncbi_taxonomy_id)
        pogo_parameter_mm_gap = ''
        if self.mm_gap:
            pogo_parameter_mm_gap = " -mm {}".format(self.mm_gap)
        pogo_command = "time {}{}{} -fasta {} -gtf {} -in {}" \
            .format(module_config_manager.get_configuration_service().get_pogo_binary_file_path(),
                    pogo_parameter_species,
                    pogo_parameter_mm_gap,
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
        it, is the same for all subclasses.
        It will prepare the command line runner completely, including the command it has to run.
        :return: a CommandLineRunner for running PoGo
        """
        ...

    def _run(self):
        if not self._validate_environment_for_running_pogo():
            self._logger.error("Can't run PoGo for file '{}'".format(self.pogo_input_file))
            self._set_failed_to_run_pogo()
        else:
            command_line_runner = self._get_command_line_runner()
            try:
                command_line_runner.start()
                self._logger.debug("PoGo --- STARTED --- command '{}'".format(command_line_runner.command))
                command_line_runner.wait()
            except CommandLineRunnerException as e:
                self._logger.error("ERROR RUNNING PoGo - {}, STDOUT ---> '{}', STDERR ---> '{}'"
                                   .format(e.value,
                                           command_line_runner.get_stdout().decode('utf8'),
                                           command_line_runner.get_stderr().decode('utf8')))
                self._set_failed_to_run_pogo()
            finally:
                self._stdout = command_line_runner.get_stdout()
                self._stderr = command_line_runner.get_stderr()
            if not command_line_runner.command_success:
                self._set_failed_to_run_pogo()
                self._logger.error("PoGo FAILED on input file '{}', command '{}'"
                                   .format(self.pogo_input_file, command_line_runner.command))
            else:
                # Successful run of PoGo
                self._set_success_to_run_pogo()
                self._logger.info("PoGo SUCCESS on input file '{}', command '{}'"
                                  .format(self.pogo_input_file, command_line_runner.command))

    def get_pogo_run_result(self):
        if not self.is_done():
            raise PogoRunnerException("PoGo runner IS NOT FINISHED YET, thus, results can't be retrieved")
        if not self.__pogo_run_result:
            self.__pogo_run_result = PogoRunResult(self.ncbi_taxonomy_id,
                                                   self.pogo_input_file,
                                                   self.protein_sequence_file_path,
                                                   self.gtf_file_path,
                                                   self)
        return self.__pogo_run_result

    def is_success(self):
        return self.__success


class PogoRunnerLocalThread(PogoRunner):
    def __init__(self,
                 ncbi_taxonomy_id=None,
                 pogo_input_file=None,
                 protein_sequence_file_path=None,
                 gtf_file_path=None,
                 mm_gap=None):
        super().__init__(ncbi_taxonomy_id, pogo_input_file, protein_sequence_file_path, gtf_file_path, mm_gap)
        self._logger = main_app_config_manager \
            .get_app_config_manager() \
            .get_logger_for("{}.{}-{}".format(__name__, type(self).__name__, threading.current_thread().getName()))

    def _get_command_line_runner(self):
        command_line_runner = CommandLineRunnerFactory.get_multithread_command_line_runner()
        command_line_runner.command = self.get_pogo_run_command()
        command_line_runner.timeout = module_config_manager.get_configuration_service().get_pogo_run_timeout()
        return command_line_runner


class PogoRunnerHpc(PogoRunner):
    pass


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
