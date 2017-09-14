# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 29-06-2017 15:05
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This is a template pipeline for refactoring out things from final pipelines as I identify how they're gonna look like
"""

import abc
# App imports
import config_manager
import trackhub.models as trackhubs
import ensembl.service
import ensembl.data_downloader
from toolbox import general

# The config manager singleton is just an example that only makes sense for specialized pipeline modules, not really for
# this template
__configuration_file = None
__configuration_manager = None


def __get_configuration_manager():
    global __configuration_manager
    if __configuration_manager is None:
        __configuration_manager = DirectorConfigurationManager(general.read_json(__configuration_file),
                                                               __configuration_file)
    return __configuration_manager


class DirectorConfigurationManager(config_manager.ConfigurationManager):
    # Command line arguments special characters
    _CONFIG_COMMAND_LINE_ARGUMENT_PARAMETER_SEPARATOR = ','
    _CONFIG_COMMAND_LINE_ARGUMENT_PARAMETER_ASSIGNMENT_CHAR = '='

    def __init__(self, configuration_object, configuration_file, pipeline_arguments):
        super(DirectorConfigurationManager, self).__init__(configuration_object, configuration_file)
        self.__pipeline_arguments = pipeline_arguments
        self.__pipeline_arguments_object = None
        # Logger the pythonist way
        self._logger = config_manager.get_app_config_manager().get_logger_for(
            "{}.{}".format(__name__, type(self).__name__))

    def _get_pipeline_arguments(self):
        return self.__pipeline_arguments

    def _get_allowed_configuration_keys(self):
        # Allowed configuration keys set is empty by default
        return {}

    def _get_pipeline_arguments_object(self):
        if self.__pipeline_arguments_object is None:
            self.__pipeline_arguments_object = self._process_pipeline_arguments()
        return self.__pipeline_arguments_object

    def _process_pipeline_arguments(self):
        if self._get_pipeline_arguments():
            if self.__pipeline_arguments_object:
                self._logger.error("DUPLICATED CALL for processing command line arguments for this pipeline, IGNORED")
            else:
                self.__pipeline_arguments_object = {}
                self._logger.debug("Processing pipeline command line arguments")
                allowed_keys = self._get_allowed_configuration_keys()
                for command_line_parameter in self._get_pipeline_arguments().split(
                        self._CONFIG_COMMAND_LINE_ARGUMENT_PARAMETER_SEPARATOR):
                    key, value = command_line_parameter.split(
                        self._CONFIG_COMMAND_LINE_ARGUMENT_PARAMETER_ASSIGNMENT_CHAR)
                    if key not in allowed_keys:
                        self._logger.error(
                            "INVALID KEY '{}' while parsing pipeline arguments, parameter '{}' SKIPPED"
                                .format(key, command_line_parameter))
                        continue
                    if key in self.__pipeline_arguments_object:
                        self._logger.error(
                            "DUPLICATED KEY '{}' while parsing pipeline arguments, parameter '{}' SKIPPED"
                                .format(key, command_line_parameter))
                        continue
                    self.__pipeline_arguments_object[key] = value
                    self._logger.debug("Pipeline argument '{}' parsed and set with value '{}'".format(key, value))
        else:
            self._logger.warning("This pipeline was provided with NO COMMAND LINE ARGUMENTS")
        return self.__pipeline_arguments_object

    def _get_value_for_pipeline_argument_key(self, key, default=None):
        if key in self._get_pipeline_arguments_object():
            return self._get_pipeline_arguments_object()[key]
        else:
            return default


class Director(metaclass=abc.ABCMeta):
    """
    This is the director of the pipeline
    """
    _PIPELINE_STATUS_OK = "ok"
    _PIPELINE_STATUS_FAIL = "fail"

    def __init__(self, runner_id=None):
        logger_name = __name__
        if runner_id:
            logger_name = runner_id
        self.__logger = config_manager.get_app_config_manager().get_logger_for(logger_name)
        self.pipeline_status = self._PIPELINE_STATUS_OK

    def is_pipeline_status_ok(self):
        return self.pipeline_status == self._PIPELINE_STATUS_OK

    def set_pipeline_status_fail(self):
        self.pipeline_status = self._PIPELINE_STATUS_FAIL

    def _before(self):
        """
        This method implements some logic that is run before running the main pipeline director.
        Subclasses implementing the pipeline logic, can override this method for establishing pre-pipeline logic.
        :return: it returns True if there was no problem, False otherwise
        """
        self._get_logger().debug("No behaviour has been defined for 'before' running the pipeline")
        return True

    def run(self):
        """
        Pipeline template director algorithm, it executes 'before' logic, then the 'pipeline' logic, and 'after' logic
        once the pipeline is finished
        It delegates to specific pipeline implementations the decision of flagging the pipeline as FAIL or not, but the
        pipeline will only be reported as 'successful' after the successful execution of all its stages. This gives the
        developer enough flexibility to have failing stages but still be able to keep going with the pipeline, alghough
        not being considered a complete success. Also, it delegates to subclasses the responsibility of deciding when
        it is not acceptable to keep running the pipeline, which makes sense, as it is their responsibility.
        :return: True if the pipeline has been successful, False otherwise
        """
        result = True
        if not self._before():
            self._get_logger().error("The logic executed BEFORE running the pipeline has FAILED")
            result = result and False
        if not self._run_pipeline():
            self._get_logger().error("The PIPELINE execution has FAILED")
            result = result and False
        if not self._after():
            self._get_logger().error("The logic executed AFTER running the pipeline has FAILED")
            result = result and False
        if result:
            self._get_logger().info("SUCCESSFUL Pipeline execution")
        return result

    def _run_pipeline(self):
        """
        This abstract method must be implemented by the subclasses with the strategy / director logic that drives the
        pipeline they are performing
        :return: True if the pipeline is successful, False otherwise
        """
        raise NotImplementedError("Implement your main pipeline logic here")

    def _after(self):
        """
        This method implements the logic that must be executed after the pipeline workflow has run.
        Subclasses implementing the pipeline logic, can override this method for establishing post-pipeline logic.
        :return: True if success, False otherwise
        """
        self._get_logger().debug("No behaviour has been defined for 'after' running the pipeline")
        return True

    def _get_logger(self):
        """
        Get the logger to be used for logging messages
        :return: it returns the logger set for the current instance of the class
        """
        return self.__logger

    def _set_logger(self, new_logger):
        """
        This method allows subclasses to change the default logger created when instantiating an implementation of this
        abstract class.
        :param new_logger: new logger to set up as the default logger for a particular implementation subclass instance
        :return: the newly set logger
        """
        self.__logger = new_logger
        return self._get_logger()


class PogoBasedPipelineDirector(Director):
    """
    Abstract class pipeline director class for those pipelines running PoGo in PRIDE
    """

    def __init__(self, runner_id=None):
        super().__init__(runner_id)

    def _get_pogo_protein_sequence_file_path_for_taxonomy(self, taxonomy_id):
        """
        This is a helper method that, given a taxonomy, it finds the protein sequence file to use as a PoGo parameter
        :param taxonomy_id: ncbi taxonomy ID
        :return: the protein sequence file path if found, None otherwise
        """
        # Get an instance of the Ensembl data downloader
        ensembl_downloader_service = ensembl.data_downloader.get_data_download_service()
        # Get Protein Sequence file from Ensembl for this taxonomy, only the "*all*" kind
        protein_sequence_files = ensembl_downloader_service.get_protein_sequences_for_species(taxonomy_id)
        # Checking on whether we can find a protein sequence or not for the given taxonomy will tell us if the
        # taxonomy is on Ensembl or not
        if not protein_sequence_files:
            return None
        pogo_parameter_protein_sequence_file_path = None
        for file_name, file_path in protein_sequence_files:
            self._get_logger().debug("Scanning protein sequence file name '{}'".format(file_name))
            if "all" in file_name:
                pogo_parameter_protein_sequence_file_path = file_path
                break
        if not pogo_parameter_protein_sequence_file_path:
            self._get_logger().error("File 'pep all' containing all sequences NOT FOUND!")
            return None
        return pogo_parameter_protein_sequence_file_path

    def _get_pogo_gtf_file_path_for_taxonomy(self, taxonomy_id):
        """
        This is a helper method that, given a taxonomy ID, it finds out which GTF file should be used for running PoGo
        :param taxonomy_id: ncbi taxonomy ID
        :return: the GTF file path if found, None otherwise
        """
        # Get an instance of the Ensembl data downloader
        ensembl_downloader_service = ensembl.data_downloader.get_data_download_service()
        gtf_files = ensembl_downloader_service.get_genome_reference_for_species(taxonomy_id)
        # For PoGo, we will use the GTF file that has no suffixes, thus, it will be the shortest file name
        pogo_parameter_gtf_file_name = None
        pogo_parameter_gtf_file_path = None
        for file_name, file_path in gtf_files:
            if (not pogo_parameter_gtf_file_name) \
                    or (len(pogo_parameter_gtf_file_name) > len(file_name)):
                pogo_parameter_gtf_file_name = file_name
                pogo_parameter_gtf_file_path = file_path
        return pogo_parameter_gtf_file_path


class TrackhubCreationDirector:
    """
    This is the abstract base class for those pipelines devoted to the creation of a trackhub
    """

    def __init__(self):
        self._logger = config_manager \
            .get_app_config_manager() \
            .get_logger_for("{}.{}".format(__name__, type(self).__name__))

    def _get_track_hub_builder(self, trackhub_descriptor):
        # TODO - Implement more complex logic for instantiating a trackhub builder, e.g. setting up the trackhub
        return trackhubs.SimpleTrackHubBuilder(trackhub_descriptor)

    @abc.abstractmethod
    def _get_trackhub_descriptor(self):
        ...

    @abc.abstractmethod
    def _get_trackhub_exporter(self):
        ...

    @abc.abstractmethod
    def _get_assemblies(self):
        ...

    def _create_trackhub(self):
        # TODO
        pass

class TrackhubCreationPogoBasedDirector(PogoBasedPipelineDirector, TrackhubCreationDirector):
    def __init__(self, runner_id=None):
        PogoBasedPipelineDirector.__init__(runner_id)
        TrackhubCreationDirector.__init__()
        # Override superclass logger to use this one
        logger_name = "{}.{}".format(__name__, type(self).__name__)
        if runner_id:
            logger_name = runner_id
        self._logger = config_manager \
            .get_app_config_manager() \
            .get_logger_for(logger_name)

    @abc.abstractmethod
    def _get_pogo_results_for_input_data(self):
        ...

    def _get_assemblies_from_pogo_results(self):
        pogo_results = self._get_pogo_results_for_input_data()
        self._get_logger().info("Processing #{} Taxonomies from PoGo results".format(len(pogo_results)))
        for taxonomy in pogo_results:
            ensembl_species_entry = ensembl.service\
                .get_service()\
                .get_species_data_service()\
                .get_species_entry_for_taxonomy_id(taxonomy)

    def _get_assemblies(self):
        self._get_assemblies_from_pogo_results()


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
