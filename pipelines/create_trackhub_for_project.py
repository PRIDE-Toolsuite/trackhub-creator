# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 07-09-2017 11:24
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This pipeline creates a trackhub for a PRIDE project, based on the information provided via a JSON formatted file, as it
can be seen on this sample:
{
  "trackHubName" : "PXD000625",
  "trackHubShortLabel" : "<a href=\"http://www.ebi.ac.uk/pride/archive/projects/PXD000625\">PXD000625</a> - Hepatoc...",
  "trackHubLongLabel" : "Experimental design For the label-free ...",
  "trackHubType" : "PROTEOMICS",
  "trackHubEmail" : "pride-support@ebi.ac.uk",
  "trackHubInternalAbsolutePath" : "...",
  "trackMaps" : [ {
    "trackName" : "PXD000625_10090_Original",
    "trackShortLabel" : "<a href=\"http://www.ebi.ac.uk/pride/archive/projects/PXD000625\">PXD000625</a> - Mus musc...",
    "trackLongLabel" : "Experimental design For the label-free proteome analysis 17 mice were used composed of 5 ...",
    "trackSpecie" : "10090",
    "pogoFile" : "..."
  } ]
}
"""

import os
import time
# App imports
import config_manager
import ensembl.service
import toolbox.general as general_toolbox
from pipelines.template_pipeline import PogoBasedPipelineDirector, DirectorConfigurationManager

# Globals
__configuration_file = None
__pipeline_arguments = None
__pipeline_director = None


# Pipeline properties access
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
        __pipeline_director = TrackhubCreatorForProject(config_manager.read_config_from_file(__configuration_file),
                                                        __configuration_file,
                                                        __pipeline_arguments)
    return __pipeline_director


class ConfigManager(DirectorConfigurationManager):
    # Command Line Arguments for this pipeline look like
    #   # This is a JSON formatted file that contains all the relevant information needed for processing the project
    #   # data and create its trackhub
    #   project_data_file=project_data.json

    # Command Line Argument keys
    _CONFIG_COMMAND_LINE_ARGUMENT_KEY_PROJECT_DATA_FILE = 'project_data_file'

    def __init__(self, configuration_object, configuration_file, pipeline_arguments):
        super(ConfigManager, self).__init__(configuration_object, configuration_file, pipeline_arguments)
        # Lazy Process command line arguments
        self.__pipeline_arguments_object = None
        self.__running_mode = None

    def get_project_data_file_path(self):
        return self._get_value_for_pipeline_argument_key(self._CONFIG_COMMAND_LINE_ARGUMENT_KEY_PROJECT_DATA_FILE)


# Models for dealing with the data file that describes the project
class ProjectTrackDescriptor:
    # Project Data File keys relative to every TrackMap object
    _PROJECT_DATA_FILE_KEY_TRACK_NAME = 'trackName'
    _PROJECT_DATA_FILE_KEY_TRACK_SHORT_LABEL = 'trackShortLabel'
    _PROJECT_DATA_FILE_KEY_TRACK_LONG_LABEL = 'trackLongLabel'
    _PROJECT_DATA_FILE_KEY_TRACK_SPECIES = 'trackSpecie'
    _PROJECT_DATA_FILE_KEY_TRACK_POGO_FILE_PATH = 'pogoFile'

    def __init__(self, project_track_descriptor_object):
        self.__project_track_descriptor_object = project_track_descriptor_object

    def _get_value_for_key(self, key, default=""):
        if self.__project_track_descriptor_object and (key in self.__project_track_descriptor_object):
            return self.__project_track_descriptor_object[key]
        return default

    def get_track_name(self):
        return self._get_value_for_key(self._PROJECT_DATA_FILE_KEY_TRACK_NAME)

    def get_track_short_label(self):
        return self._get_value_for_key(self._PROJECT_DATA_FILE_KEY_TRACK_SHORT_LABEL)

    def get_track_long_label(self):
        return self._get_value_for_key(self._PROJECT_DATA_FILE_KEY_TRACK_LONG_LABEL)

    def get_track_species(self):
        return self._get_value_for_key(self._PROJECT_DATA_FILE_KEY_TRACK_SPECIES)

    def get_track_file_path_pogo(self):
        return self._get_value_for_key(self._PROJECT_DATA_FILE_KEY_TRACK_POGO_FILE_PATH)


class ProjectTrackhubDescriptor:
    # Project Data File keys
    _PROJECT_DATA_FILE_KEY_TRACKHUB_NAME = 'trackHubName'
    _PROJECT_DATA_FILE_KEY_TRACKHUB_SHORT_LABEL = 'trackHubShortLabel'
    _PROJECT_DATA_FILE_KEY_TRACKHUB_LONG_LABEL = 'trackHubLongLabel'
    _PROJECT_DATA_FILE_KEY_TRACKHUB_HUB_TYPE = 'trackHubType'
    _PROJECT_DATA_FILE_KEY_TRACKHUB_EMAIL = 'trackHubEmail'
    _PROJECT_DATA_FILE_KEY_TRACKHUB_INTERNAL_ABSOLUTE_PATH = 'trackHubInternalAbsolutePath'
    _PROJECT_DATA_FILE_KEY_TRACKHUB_SECTION_TRACKMAPS = 'trackMaps'

    def __init__(self, project_data_file_path):
        self.__project_data_file_path = project_data_file_path
        self.__project_data_object = None
        self.__project_tracks_descriptors = None

    def _get_project_data_object(self):
        if not self.__project_data_object:
            self.__project_data_object = general_toolbox.read_json(self.__project_data_file_path)
        return self.__project_data_object

    def _get_value_for_key(self, key, default=""):
        # TODO - I should start thinking about refactoring this out
        if key in self._get_project_data_object():
            return self._get_project_data_object()[key]
        return default

    def get_trackhub_name(self):
        return self._get_value_for_key(self._PROJECT_DATA_FILE_KEY_TRACKHUB_NAME,
                                       os.path.basename(self.__project_data_file_path))

    def get_trackhub_short_label(self):
        return self._get_value_for_key(self._PROJECT_DATA_FILE_KEY_TRACKHUB_SHORT_LABEL,
                                       "--- NO SHORT LABEL HAS BEEN DEFINED FOR THIS TRACKHUB ---")

    def get_trackhub_long_label(self):
        return self._get_value_for_key(self._PROJECT_DATA_FILE_KEY_TRACKHUB_LONG_LABEL,
                                       "--- NO LONG LABEL HAS BEEN DEFINED FOR THIS TRACKHUB ---")

    def get_trackhub_hub_type(self):
        return self._get_value_for_key(self._PROJECT_DATA_FILE_KEY_TRACKHUB_HUB_TYPE,
                                       "PROTEOMICS")

    def get_trackhub_email(self):
        return self._get_value_for_key(self._PROJECT_DATA_FILE_KEY_TRACKHUB_EMAIL,
                                       "pride-support@ebi.ac.uk")

    def get_trackhub_destination_path(self):
        return self._get_value_for_key(self._PROJECT_DATA_FILE_KEY_TRACKHUB_INTERNAL_ABSOLUTE_PATH)

    def get_trackhub_project_defined_tracks(self):
        if not self.__project_tracks_descriptors:
            # Default value is an empty list of tracks
            self.__project_tracks_descriptors = []
            data_file_project_track_description_objects = \
                self._get_value_for_key(self._PROJECT_DATA_FILE_KEY_TRACKHUB_SECTION_TRACKMAPS)
            if data_file_project_track_description_objects:
                self.__project_tracks_descriptors = \
                    [ProjectTrackDescriptor(data_file_project_track_description_object)
                     for data_file_project_track_description_object
                     in data_file_project_track_description_objects]
        return self.__project_tracks_descriptors


class TrackhubCreatorForProject(PogoBasedPipelineDirector):
    # TODO
    def __init__(self, configuration_object, configuration_file, pipeline_arguments):
        runner_id = "{}-{}".format(__name__, time.time())
        super(TrackhubCreatorForProject, self).__init__(runner_id)
        self.__config_manager = ConfigManager(configuration_object, configuration_file, pipeline_arguments)
        self.__project_trackhub_descriptor = None
        # Only the valid project tracks will be processed for being included in the trackhub
        self.__valid_project_tracks = None

    @property
    def __valid_project_tracks(self):
        """
        This helper creates a list of valid trackhub tracks from the given project, i.e. tracks that meet this cirteria:
            - Its taxonomy ID is available on Ensembl
        :return: a list of valid trackhub tracks for the given project
        """
        if not self.__valid_project_tracks:
            self.__valid_project_tracks = []
            ensembl_service = ensembl.service.get_service()
            for project_track_descriptor in self.__project_trackhub_descriptor.get_trackhub_project_defined_tracks():
                if ensembl_service.get_species_data_service().get_species_entry_for_taxonomy_id(project_track_descriptor.get_track_species()):
                    self.__valid_project_tracks.append(project_track_descriptor)
        return self.__valid_project_tracks

    def _before(self):
        if self.__config_manager.get_project_data_file_path():
            self._get_logger().info("Reading Project Trackhub Descriptor from file at '{}'"
                                    .format(self.__config_manager.get_project_data_file_path()))
            self.__project_trackhub_descriptor = \
                ProjectTrackhubDescriptor(self.__config_manager.get_project_data_file_path())
            # Check that the destination folder exists
            if not os.path.isdir(self.__project_trackhub_descriptor.get_trackhub_destination_path()):
                self._get_logger().error("Trackhub destination path NOT VALID, '{}'"
                                         .format(self.__project_trackhub_descriptor.get_trackhub_destination_path()))
                return False
            # TODO - Check valid project tracks
            return True
        self._get_logger().error("INVALID / MISSING Project Trackhub Descriptor file, '{}'"
                                 .format(self.__config_manager.get_project_data_file_path()))
        return False


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
