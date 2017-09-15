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
from toolbox import general
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
    def __init__(self):
        self.track_hub_root_folder = None
        self.track_hub_descriptor_file_path = None


class TrackHubExporter(metaclass=ABCMeta):
    def __init__(self):
        self.logger = config_manager.get_app_config_manager().get_logger_for(__name__)
        self.export_summary = TrackHubExportSummary()

    @abstractmethod
    def export_simple_trackhub(self, track_hub_builder):
        return self.export_summary


class TrackHubLocalFilesystemExporter(TrackHubExporter):
    def __init__(self):
        super().__init__()
        # The default destination folder for exporting the trackhub is located within the current session working
        # directory
        self.track_hub_destination_folder = os.path.join(
            config_manager.get_app_config_manager().get_session_working_dir(),
            'track_hub')

    def __get_tracks_with_non_empty_bed_files(self, assembly, track_collector):
        non_empty_file_tracks = []
        for track in track_collector.get_tracks():
            if not track.get_big_data_url():
                self.logger.warning("Assembly '{}' contains a track '{}' with NO BIG DATA URL, -- SKIPPED --"
                                    .format(assembly,
                                            track.get_track()))
                continue
            if not os.path.exists(track.get_big_data_url()):
                self.logger.warning("Assembly '{}' contains a track '{}' with AN INVALID BIG DATA URL '{}', "
                                    "-- SKIPPED --"
                                    .format(assembly,
                                            track.get_track(),
                                            track.get_big_data_url()))
                continue
            big_file_stat_info = os.stat(track.get_big_data_url())
            if big_file_stat_info.st_size == 0:
                self.logger.warning("Assembly '{}' contains a track '{}' with AN EMPTY BIG DATA FILE at '{}', "
                                    "-- SKIPPED --"
                                    .format(assembly,
                                            track.get_track(),
                                            track.get_big_data_url()))
                continue
            non_empty_file_tracks.append(track)
        return non_empty_file_tracks

    def export_simple_trackhub(self, trackhub_builder):
        file_trackhub_descriptor = os.path.join(self.track_hub_destination_folder, 'hub.txt')
        # TODO - Tell clients when you're not exporting anything
        if not self.export_summary and not os.path.isfile(file_trackhub_descriptor):
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
            for assembly in trackhub_builder.assemblies:
                tracks_with_non_empty_bed_files = \
                    self.__get_tracks_with_non_empty_bed_files(assembly,
                                                               trackhub_builder.assemblies[assembly].track_collector)
                if not tracks_with_non_empty_bed_files:
                    self.logger.warning("Assembly '{}' contains ALL EMPTY BIG DATA FILE TRACKS -- SKIPPED --"
                                        .format(assembly))
                    continue
                assembly_folder = os.path.join(self.track_hub_destination_folder, assembly)
                # Create the folder for the assembly
                general.check_create_folders([assembly_folder])
                self.logger.info("For Assembly '{}', trackhub folder created at '{}'".format(assembly, assembly_folder))
                # Per track in its track collector, we'll process only those tracks with non-empty big data files
                for track in tracks_with_non_empty_bed_files:
                    # Copy track file to assembly folder
                    # TODO - source of this
                    big_data_file_name = os.path.basename(track.get_big_data_url())
                    destination_file_path = os.path.join(assembly_folder, big_data_file_name)
                    shutil.copy(track.get_big_data_url(), destination_file_path)
                    # Modify the track (irreversible) to point to the big data file relative to the trackDB.txt file
                    # path
                    new_big_data_url = big_data_file_name
                    track.set_big_data_url(new_big_data_url)
                    self.logger.info(
                        "Assembly '{}' ---> Data for track '{}' prepared, track information updated"
                            .format(assembly, track.get_track()))
                # Export trackDB.txt with the current set of 'valid' tracks
                trackdb_file_path = os.path.join(assembly_folder, 'trackDb.txt')
                track_collector_exporter = TrackCollectorFileExporter(trackdb_file_path)
                track_collector_exporter.export_from_track_collection(tracks_with_non_empty_bed_files)
                # Add assembly entry to genomes.txt files within trackhub root folder
                assembly_mapping[assembly] = os.path.join(os.path.basename(os.path.dirname(trackdb_file_path)),
                                                          os.path.basename(trackdb_file_path))
            self.logger.info("Assembly data collected and exported to its corresponding subfolders")
            # Export data to genomes.txt file
            genomes_file_path = os.path.join(self.track_hub_destination_folder, 'genomes.txt')
            with open(genomes_file_path, 'w') as wf:
                for assembly in assembly_mapping:
                    wf.write("genome {}\n"
                             "trackDb {}\n"
                             .format(assembly, assembly_mapping[assembly]))
            self.logger.info("Genomes file with per-assembly data exported to '{}'".format(genomes_file_path))
            # Prepare summary object
            self.export_summary = TrackHubExportSummary()
            self.export_summary.track_hub_root_folder = self.track_hub_destination_folder
            self.export_summary.track_hub_descriptor_file_path = file_trackhub_descriptor
            self.logger.info("Trackhub export summary prepared")
        return self.export_summary


class TrackHubExporterPrideClusterFtp(TrackHubLocalFilesystemExporter):
    def __init__(self):
        super().__init__()
        # Default destination folder for pride cluster trackhubs
        self.track_hub_destination_folder = os.path.join(
            config_manager.get_app_config_manager().get_session_working_dir(),
            os.path.join('pride_cluster', 'track_hubs'))


# TrackHub Builders
class TrackHubBuilder(metaclass=ABCMeta):
    def __init__(self, track_hub_descriptor):
        self.logger = config_manager.get_app_config_manager().get_logger_for(__name__)
        self.track_hub = track_hub_descriptor
        self.assemblies = {}

    @abstractmethod
    def _create_track_collector(self):
        ...

    def add_track_to_assembly(self, assembly, track):
        if assembly not in self.assemblies:
            self.logger.debug("For Trackhub '{}', new assembly '{}'".format(self.track_hub.get_hub(), assembly))
            self.assemblies[assembly] = TrackHubGenomeAssembly(assembly, self._create_track_collector())
        self.assemblies[assembly].track_collector.add_track(track)

    @abstractmethod
    def accept_exporter(self, trackhub_exporter):
        ...


class SimpleTrackHubBuilder(TrackHubBuilder):
    def __init__(self, track_hub_descriptor):
        super().__init__(track_hub_descriptor)

    def _create_track_collector(self):
        return SimpleTrackCollector()

    def accept_exporter(self, trackhub_exporter):
        trackhub_exporter.export_simple_trackhub(self)


# Modeling TrackHubs
class TrackHubGenomeAssembly:
    def __init__(self, assembly, track_collector):
        # Let's try the Pythonist way, attributes are public by default
        self.track_collector = track_collector
        self.assembly = assembly


class TrackCollector:
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
    def __init__(self):
        super().__init__()

    def accept(self, track_collector_visitor):
        return track_collector_visitor.visit_simple_track_collector(self)


# Model for a Track
class BaseTrack:
    _SEPARATOR_CHAR = ' '

    def __init__(self, track, short_label, long_label):
        # Client side of the model
        self.__track = track
        self.__short_label = short_label
        self.__long_label = long_label
        # Builder side of the model
        self.__type = None
        self.__big_data_url = None

    def __str__(self):
        return "{}{}{}{}{}" \
            .format(key_value_to_str_if_not_none('track', self.get_track(), self._SEPARATOR_CHAR, '\n'),
                    key_value_to_str_if_not_none('type', self.get_type(), self._SEPARATOR_CHAR, '\n'),
                    key_value_to_str_if_not_none('bigDataUrl', self.get_big_data_url(), self._SEPARATOR_CHAR, '\n'),
                    key_value_to_str_if_not_none('shortLabel', self.get_short_label(), self._SEPARATOR_CHAR, '\n'),
                    key_value_to_str_if_not_none('longLabel', self.get_long_label(), self._SEPARATOR_CHAR, ''))

    def __identify_track_type_from_file(self, file_path):
        # TODO - We return the default type right now, but this will change in the future
        return 'bed'

    def set_type(self, file_path):
        self.__type = self.__identify_track_type_from_file(file_path)

    def set_big_data_url(self, big_data_url):
        self.__big_data_url = big_data_url

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

    def get_big_data_url(self):
        return self.__big_data_url

    def dump_to_track_db_file(self, file_path):
        with open(file_path, 'w') as f:
            f.write(str(self))


# Model for a trackhub
class TrackHub:
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
