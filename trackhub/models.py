# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 03-08-2017 15:44
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
These are the models for representing and dealing with trackhubs
DISCLAIMER - This is the first iteration of the software to create the trackhubs. In this iteration we are going for the
simple version of the hubs, "trackhub quickstart guide" at https://genome.ucsc.edu/goldenpath/help/hubQuickStart.html
"""

import os
import shutil
from abc import ABCMeta, abstractmethod
# Application imports
import config_manager
import ensembl.service
from toolbox import general
from data_formats.converters import DataFormatConverterFactory
from toolbox.assembly import AssemblyMappingServiceFactory, AssemblyMappingServiceException
from .exceptions import UnknownBigDataFileType, BaseTrackException, TrackHubLocalFilesystemExporterException
from . import config_manager as module_config_manager


# Now, different trackhub builders for the different types of trackhubs (quickstart, custom, etc.)
# DISCLAIMER - I'm aware this first iteration may look a little bit patchy, but it needs to be acknowledged that the
# documentation for modeling this is not very developer friendly, this module it is not meant to be a general module for
# building all sorts of trackhubs and this is the first iteration, so we're not very sure what we want
# TODO - How and where to define the building directors?


def key_value_to_str_if_not_none(key, value, separator=' ', suffix='\n'):
    """
    Helper method that, given a key, value, separator and suffix, it will return the string
    '<key><separator><value><suffix>' if value is not None, otherwise it will return the empty string ''
    :param key: key
    :param value: value
    :param separator: character to use as separator, default ' '
    :param suffix: character to use as suffix, default '\n'
    :return: '<key><separator><value><suffix>' if value not None, '' otherwise
    """
    if value:
        return "{}{}{}{}".format(key, separator, value, suffix)
    return ""


# Track Collector Serializers
class TrackCollectorExporter(metaclass=ABCMeta):
    def __init__(self):
        self.logger = config_manager.get_app_config_manager().get_logger_for(__name__)

    @abstractmethod
    def visit_simple_track_collector(self, track_collector):
        ...


class TrackCollectorFileExporter(TrackCollectorExporter):
    """
    This track collector exporter is specialised on simple track collectors and it will export their information to a
    file (usually this is the 'trackDb.txt' file that is present within every assembly in a trackhub)
    """
    def __init__(self, destination_file_path):
        super(TrackCollectorFileExporter, self).__init__()
        self.destination_file_path = destination_file_path

    def visit_simple_track_collector(self, track_collector):
        self.logger.debug("Exporting #{} track(s) from Simple Track Collector to file '{}'"
                          .format(len(track_collector.get_tracks()), self.destination_file_path))
        with open(self.destination_file_path, 'w') as wf:
            for track in track_collector.get_tracks():
                wf.write(str(track) + "\n\n")

    def export_from_track_collection(self, tracks):
        self.logger.debug("Exporting #{} track(s) from a given collection to file '{}'"
                          .format(len(tracks), self.destination_file_path))
        with open(self.destination_file_path, 'w') as wf:
            for track in tracks:
                wf.write(str(track) + "\n\n")


# TrackHub Exporters
class TrackHubExportSummary:
    """
    Summary report about the process of exporting a trackhub
    """
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.infos = []
        self.export_performed = False
        self.track_hub_root_folder = None
        self.track_hub_descriptor_file_path = None


class TrackHubExporter(metaclass=ABCMeta):
    """
    A trackhub exporter materializes all the parts held together by a trackhub builder into a trackhub structure
    """
    def __init__(self):
        self.logger = config_manager.get_app_config_manager().get_logger_for(__name__)
        self.export_summary = None

    @abstractmethod
    def export_simple_trackhub(self, track_hub_builder):
        # I know, I should avoid returning 'None'
        return self.export_summary


class TrackHubLocalFilesystemExporter(TrackHubExporter):
    """
    This trackhub exporter will recreate a trackhub in a given location of the filesystem, by exporting all the parts
    held together by a trackhub builder, in this case ONLY a simple trackhub builder is supported at this iteration of
    the software development lifecycle
    """
    def __init__(self):
        super().__init__()
        # The default destination folder for exporting the trackhub is located within the current session working
        # directory
        self.track_hub_destination_folder = os.path.join(
            config_manager.get_app_config_manager().get_session_working_dir(),
            'track_hub')
        # By default we're working with an empty export summary
        self.export_summary = TrackHubExportSummary()

    def __get_tracks_with_non_empty_bed_files(self, assembly, track_collector):
        non_empty_file_tracks = []
        for track in track_collector.get_tracks():
            if not track.get_big_data_url():
                message = "Assembly '{}' contains a track '{}' with NO BIG DATA URL, -- SKIPPED --"\
                    .format(assembly,
                            track.get_track())
                self.export_summary.warnings.append(message)
                self.logger.warning(message)
                continue
            if not os.path.exists(track.get_big_data_url()):
                message = "Assembly '{}' contains a track '{}' with AN INVALID BIG DATA URL '{}', -- SKIPPED --"\
                    .format(assembly,
                            track.get_track(),
                            track.get_big_data_url())
                self.export_summary.warnings.append(message)
                self.logger.warning(message)
                continue
            big_file_stat_info = os.stat(track.get_big_data_url())
            if big_file_stat_info.st_size == 0:
                message = "Assembly '{}' contains a track '{}' with AN EMPTY BIG DATA FILE at '{}', -- SKIPPED --"\
                    .format(assembly,
                            track.get_track(),
                            track.get_big_data_url())
                self.export_summary.warnings.append(message)
                self.logger.warning(message)
                continue
            non_empty_file_tracks.append(track)
        if not non_empty_file_tracks:
            message = "All tracks in Assembly '{}' contain INVALID BIG DATA FILES!!!".format(assembly)
            self.export_summary.warnings.append(message)
            self.logger.error(message)
        return non_empty_file_tracks

    def export_simple_trackhub(self, trackhub_builder):
        """
        When exporting a simple trackhub from a (simple) trackhub builder, those tracks with empty .bed files will be
        skipped
        :param trackhub_builder: a TrackhubBuilder that holds all the trackhub parts together
        :return: a report of the export process as a TrackHubExportSummary
        """
        file_trackhub_descriptor = os.path.join(self.track_hub_destination_folder, 'hub.txt')
        self.export_summary.track_hub_root_folder = self.track_hub_destination_folder
        self.export_summary.track_hub_descriptor_file_path = file_trackhub_descriptor
        # TODO - Tell clients when you're not exporting anything
        if os.path.isfile(file_trackhub_descriptor):
            error_message = "Trackhub Export to '{}' ABORTED, there already is a trackhub there" \
                .format(self.track_hub_destination_folder)
            self.logger.warning(error_message)
            self.export_summary.errors.append(error_message)
        else:
            self.logger.info("Export Simple TrackHub to '{}'".format(self.track_hub_destination_folder))
            # Check / Create destination folder
            general.check_create_folders([self.track_hub_destination_folder])
            # Create hub.txt file
            with open(file_trackhub_descriptor, 'w') as wf:
                wf.write("{}\n".format(str(trackhub_builder.track_hub)))
            self.logger.info("TrackHub descriptor file at '{}'".format(file_trackhub_descriptor))
            # Per assembly
            # TODO - I should also have an assembly collector and refactor TrackHubGenomeAssembly accordingly, but I'm
            # TODO - cutting some corners here to get the first iteration up and running as soon as possible. Supporting
            # TODO - more complex genomes.txt files is not as critical as getting the 'tracks' the right way
            assembly_mapping = {}
            assembly_mapping_service = AssemblyMappingServiceFactory.get_assembly_mapping_service()
            ensembl_species_service = ensembl.service.get_service().get_species_data_service()
            for assembly in dict(trackhub_builder.assemblies):
                try:
                    ucsc_assembly = assembly_mapping_service \
                        .get_ucsc_assembly_for_ensembl_assembly_accession(ensembl_species_service
                                                                          .get_species_entry_for_assembly(assembly)
                                                                          .get_assembly_accession())
                except AssemblyMappingServiceException as e:
                    message = "ERROR while mapping Ensembl Assembly '{}' - SKIPPING THIS ASSEMBLY - xxx> '{}'"\
                        .format(assembly, e.value)
                    self.export_summary.warnings.append(message)
                    self.logger.error(message)
                    trackhub_builder.invalidate_assembly(assembly)
                    continue
                self.logger.info("Ensembl Assembly '{}' --- mapped_to ---> UCSC Assembly '{}'"
                                    .format(assembly, ucsc_assembly))
                tracks_with_non_empty_bed_files = \
                    self.__get_tracks_with_non_empty_bed_files(assembly,
                                                               trackhub_builder.assemblies[assembly].track_collector)
                if not tracks_with_non_empty_bed_files:
                    message = "Assembly '{} ({})' contains ALL EMPTY BIG DATA FILE TRACKS -- SKIPPED --"\
                        .format(assembly,ucsc_assembly)
                    self.export_summary.warnings.append(message)
                    self.logger.warning(message)
                    trackhub_builder.invalidate_assembly(assembly)
                    continue
                assembly_folder = os.path.join(self.track_hub_destination_folder, ucsc_assembly)
                # Create the folder for the assembly
                general.check_create_folders([assembly_folder])
                self.logger.info("For Assembly '{} ({})', trackhub folder created at '{}'"
                                 .format(assembly,
                                         ucsc_assembly,
                                         assembly_folder))
                # Per track in its track collector, we'll process only those tracks with non-empty big data files
                # The following map will contain the tracks that are ready for being added to the collector. If a track
                # has no converter associated, then it can be added with no problem, but if it has a converter, we need
                # to wait for it to finish the conversion process before we can add the track to the collector
                # TODO - Apparently, there's usually just a couple of tracks per assembly (without PTMs and with PTMs),
                # TODO - this part can be parallelized even further by making a map <assembly, <track, converter>> that
                # TODO - will contain all the processed tracks for all the assemblies, so all the conversions happen in
                # TODO - parallel. Then, iterating over this would produce the final genomes.txt file
                track_converter_map = {}
                for track in tracks_with_non_empty_bed_files:
                    # Copy track file to assembly folder
                    # TODO - source of this
                    # Instead of copying the file, if it is a BED file, perform conversion -
                    # Get the original big data url
                    big_data_file_name = os.path.basename(track.get_big_data_url())
                    # Default destination for the big data file is just copying it
                    destination_file_path = os.path.join(assembly_folder, big_data_file_name)
                    # if track type is BED, workout the destination file as bigbed and do not copy the data, convert it
                    converter = None
                    if (track.get_type() == BaseTrack.TRACK_TYPE_BED) \
                            and track.taxonomy_id:
                        destination_file_path = \
                            os.path.join(assembly_folder,
                                         "{}.bb".format(big_data_file_name[:big_data_file_name.rfind(".")]))
                        # The new name for the big data file
                        big_data_file_name = os.path.basename(destination_file_path)
                        # Convert the file
                        converter = DataFormatConverterFactory.get_bed_to_bigbed_converter(track.taxonomy_id,
                                                                                           track.get_big_data_url(),
                                                                                           destination_file_path)
                        # We start the converter
                        converter.start()
                    else:
                        shutil.copy(track.get_big_data_url(), destination_file_path)
                    # Update the big data url with either the copied file or the newly built .bb (bigBed) file
                    # Modify the track (irreversible) to point to the big data file relative to the trackDB.txt file
                    # path
                    new_big_data_url = big_data_file_name
                    track.set_big_data_url(new_big_data_url)
                    self.logger.info(
                        "Assembly '{} ({})' ---> Data for track '{}' prepared, track information updated"
                            .format(assembly,
                                    ucsc_assembly,
                                    track.get_track()))
                    # Apparently, 'blank spaces' are not allowed in the track names (UCSC)
                    track.set_track(track.get_track().replace(' ', '_'))
                    # Add the track to the map
                    track_converter_map[track] = converter
                # Export trackDB.txt with the current set of 'valid' tracks
                trackdb_file_path = os.path.join(assembly_folder, 'trackDb.txt')
                track_collector_exporter = TrackCollectorFileExporter(trackdb_file_path)
                # Add successful tracks
                successful_tracks = []
                for track, converter in track_converter_map.items():
                    if converter:
                        converter.wait()
                        if not converter.is_conversion_ok():
                            message = "SKIP TRACK for Assembly '{} ({})' " \
                                      "---> Track '{}' Big Data File FAILED conversion process " \
                                      "- STDOUT '{}', STDERR '{}'".format(assembly,
                                                                          ucsc_assembly,
                                                                          track.get_track(),
                                                                          converter.get_conversion_output(),
                                                                          converter.get_conversion_output_error())
                            self.export_summary.warnings.append(message)
                            self.logger.error(message)
                            # Skip this track
                            continue
                    # Add the track to the successful tracks list
                    successful_tracks.append(track)
                track_collector_exporter.export_from_track_collection(successful_tracks)
                # Add assembly entry to genomes.txt files within trackhub root folder
                assembly_mapping[ucsc_assembly] = os.path.join(os.path.basename(os.path.dirname(trackdb_file_path)),
                                                               os.path.basename(trackdb_file_path))
            if not assembly_mapping:
                message = "ALL Assemblies in this project are INVALID"
                self.export_summary.errors.append(message)
                self.logger.error(message)
            self.logger.info("Assembly data collected and exported to its corresponding subfolders")
            # Export data to genomes.txt file
            genomes_file_path = os.path.join(self.track_hub_destination_folder, 'genomes.txt')
            with open(genomes_file_path, 'w') as wf:
                for assembly in assembly_mapping:
                    wf.write("genome {}\n"
                             "trackDb {}\n\n"
                             .format(assembly, assembly_mapping[assembly]))
            self.logger.info("Genomes file with per-assembly data exported to '{}'".format(genomes_file_path))
            # Prepare summary object
            self.export_summary.export_performed = True
            self.logger.info("Trackhub export summary prepared")
        return self.export_summary


class TrackHubExporterPrideClusterFtp(TrackHubLocalFilesystemExporter):
    """
    This is a file system based trackhub exporter specialised on PRIDE Cluster trackhubs, so it will set up the
    particular location where the new trackhub has to be exported to.
    """
    def __init__(self):
        super().__init__()
        # Default destination folder for pride cluster trackhubs
        self.track_hub_destination_folder = os.path.join(
            config_manager.get_app_config_manager().get_session_working_dir(),
            os.path.join('pride_cluster', 'track_hubs'))


# TrackHub Builders
class TrackHubBuilder(metaclass=ABCMeta):
    """
    A trackhub builder puts together all the parts that make a trackhub: the descriptor (hub.txt) and the assemblies
    with their corresponding track collectors
    """
    def __init__(self, track_hub_descriptor):
        self.logger = config_manager.get_app_config_manager().get_logger_for(__name__)
        self.track_hub = track_hub_descriptor
        self.assemblies = {}
        self.invalid_assemblies = {}

    @abstractmethod
    def _create_track_collector(self):
        ...

    def add_track_to_assembly(self, assembly, track):
        if assembly not in self.assemblies:
            self.logger.debug("For Trackhub '{}', new assembly '{}'".format(self.track_hub.get_hub(), assembly))
            self.assemblies[assembly] = TrackHubGenomeAssembly(assembly, self._create_track_collector())
        self.assemblies[assembly].track_collector.add_track(track)

    def invalidate_assembly(self, assembly):
        if assembly not in self.assemblies:
            self.logger.error("CANNOT Invalidate assembly '{}', because it is not present in this builder"
                              .format(assembly))
        elif assembly in self.invalid_assemblies:
            self.logger.error("ALREADY INVALID assembly '{}'".format(assembly))
        else:
            self.logger.warning("INVALIDATING Assembly '{}'"
                              .format(assembly))
            self.invalid_assemblies[assembly] = self.assemblies[assembly]
            self.assemblies.pop(assembly)

    @abstractmethod
    def accept_exporter(self, trackhub_exporter):
        ...


class SimpleTrackHubBuilder(TrackHubBuilder):
    """
    This trackhub builder implements the factory methods for putting together a simple trackhub, i.e. using a simple
    track collector, and a particular method of the trackhub visitor for exporting
    """
    def __init__(self, track_hub_descriptor):
        super().__init__(track_hub_descriptor)

    def _create_track_collector(self):
        return SimpleTrackCollector()

    def accept_exporter(self, trackhub_exporter):
        trackhub_exporter.export_simple_trackhub(self)


# Modeling TrackHubs
class TrackHubGenomeAssembly:
    """
    This class models an entry in the 'genomes.txt' file present in a trackhub, it consists of the assembly name and a
    track collector for that assembly
    """
    def __init__(self, assembly, track_collector):
        # Let's try the Pythonist way, attributes are public by default
        self.track_collector = track_collector
        self.assembly = assembly


class TrackCollector:
    """
    A track collector is an entity that holds related tracks together, and it also provides a context for those tracks,
    which will determine how they are exported into a trackhub later on, by the visitor passed to this track collector
    and its implementation of the visit method.
    """
    def __init__(self):
        # List of tracks in this track collector
        self.__tracks = []

    def add_track(self, track):
        self.__tracks.append(track)

    def get_tracks(self):
        return self.__tracks

    @abstractmethod
    def accept(self, track_collector_visitor):
        return track_collector_visitor.visit_track_collector(self)


class SimpleTrackCollector(TrackCollector):
    """
    This track collector models the simplest track collection scheme defined in the UCSC documentation
    at https://genome.ucsc.edu/goldenpath/help/trackDb/trackDbHub.html
    """
    def __init__(self):
        super().__init__()

    def accept(self, track_collector_visitor):
        return track_collector_visitor.visit_simple_track_collector(self)


# Model for a Track
class BaseTrack:
    """
    Base class for modeling a trackhub track.
    On this iteration of the software, we are dealing with simple tracks, in the future it may need refactoring, but
    this class is modeling the core information common to all possible tracks, from the simplest ones to the more
    complex, at least according to the documentation available up to the date when this module was developed.
    """
    _SEPARATOR_CHAR = ' '
    # Big Data file extensions
    _BIG_DATA_FILE_EXTENSION_BED = '.bed'
    _BIG_DATA_FILE_EXTENSION_BIGBED = '.bb'
    # Big Data file format information
    _BIG_DATA_BED_MAX_NUMBER_OF_COLUMNS = 12
    _BIG_DATA_BED_MIN_NUMBER_OF_COLUMNS = 3
    # Track Types
    TRACK_TYPE_BED = 'bed'
    TRACK_TYPE_BIGBED = 'bigBed'

    def __init__(self, track, short_label, long_label):
        # Client side of the model
        self.__track = track
        self.__short_label = short_label
        self.__long_label = long_label
        # Builder side of the model
        self.__type = None
        self.__big_data_url = None
        # TODO - warning - shitty modeling here...
        # This field reflects the <3, 12> [+/.]
        self.__bigbed_addon = None
        # NCBI Taxonomy for this track, this will be useful later
        self.taxonomy_id = None

    def __str__(self):
        return "{}{}{}{}{}" \
            .format(key_value_to_str_if_not_none('track', self.get_track(), self._SEPARATOR_CHAR, '\n'),
                    key_value_to_str_if_not_none('type', self.get_type_string(), self._SEPARATOR_CHAR, '\n'),
                    key_value_to_str_if_not_none('bigDataUrl', self.get_big_data_url(), self._SEPARATOR_CHAR, '\n'),
                    key_value_to_str_if_not_none('shortLabel', self.get_short_label(), self._SEPARATOR_CHAR, '\n'),
                    key_value_to_str_if_not_none('longLabel', self.get_long_label(), self._SEPARATOR_CHAR, ''))

    def __identify_track_type_from_file(self, file_path):
        # TODO - I should not identify the file type by looking at the extension, but by looking at the content via a
        # TODO - specialised handler. It will be done like this at this iteration of the software
        if file_path.endswith(self._BIG_DATA_FILE_EXTENSION_BED):
            with open(file_path) as f:
                for line in f:
                    number_of_columns = len(line.strip().split('\t'))
                    if number_of_columns < self._BIG_DATA_BED_MIN_NUMBER_OF_COLUMNS:
                        raise BaseTrackException("BED format requires, at least, 3 columns, "
                                                 "only #{} identified in file '{}', sampled line '{}'"
                                                 .format(str(number_of_columns),
                                                         file_path,
                                                         line.strip()))
                    elif number_of_columns > self._BIG_DATA_BED_MAX_NUMBER_OF_COLUMNS:
                        self.__bigbed_addon = "{} +".format(str(self._BIG_DATA_BED_MAX_NUMBER_OF_COLUMNS))
                    else:
                        self.__bigbed_addon = str(number_of_columns)
            return self.TRACK_TYPE_BED
        if file_path.endswith(self._BIG_DATA_FILE_EXTENSION_BIGBED):
            return self.TRACK_TYPE_BIGBED
        raise UnknownBigDataFileType("Unknown big data file type for '{}'".format(file_path))

    def set_type(self, file_path):
        self.__type = self.__identify_track_type_from_file(file_path)

    def set_big_data_url(self, big_data_url):
        self.__big_data_url = big_data_url
        self.set_type(big_data_url)

    def get_track(self):
        return self.__track

    def set_track(self, track_name):
        self.__track = track_name

    def get_short_label(self):
        return self.__short_label

    def get_long_label(self):
        return self.__long_label

    def get_type(self):
        return self.__type

    def get_type_string(self):
        if self.get_type() == self.TRACK_TYPE_BIGBED:
            return "{} {}".format(self.get_type(), self.__bigbed_addon)
        return self.get_type()

    def get_big_data_url(self):
        return self.__big_data_url

    def dump_to_track_db_file(self, file_path):
        with open(file_path, 'w') as f:
            f.write(str(self))


# Model for a trackhub
class TrackHub:
    """
    This class models the kind of data that can be found in the 'hub.txt' within a trackhub
    """
    _SEPARATOR_CHAR = ' '

    def __init__(self, hub, short_label, long_label, email, description_url):
        self.__hub = hub
        self.__short_label = short_label
        self.__long_label = long_label
        self.__email = email
        self.__description_url = description_url
        # Default genomes file
        self.__genomes_file = 'genomes.txt'

    def __str__(self):
        return "hub{}{}\n" \
               "shortLabel{}{}\n" \
               "longLabel{}{}\n" \
               "genomesFile{}{}\n" \
               "email{}{}\n" \
               "descriptionUrl{}{}" \
            .format(self._SEPARATOR_CHAR, self.get_hub(),
                    self._SEPARATOR_CHAR, self.get_short_label(),
                    self._SEPARATOR_CHAR, self.get_long_label(),
                    self._SEPARATOR_CHAR, self.get_genomes_file(),
                    self._SEPARATOR_CHAR, self.get_email(),
                    self._SEPARATOR_CHAR, self.get_description_url())

    def get_hub(self):
        return self.__hub

    def get_short_label(self):
        return self.__short_label

    def get_long_label(self):
        return self.__long_label

    def get_email(self):
        return self.__email

    def get_description_url(self):
        return self.__description_url

    def get_genomes_file(self):
        return self.__genomes_file

    def dump_to_file(self, file_path):
        with open(file_path, 'w') as f:
            f.write(str(self))


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
