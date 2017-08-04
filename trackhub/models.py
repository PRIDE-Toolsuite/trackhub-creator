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
"""

# Application imports
import config_manager


# Trackhub builder - base class
class TrackHubBuilder:
    def __init__(self, track_hub):
        self.__logger = config_manager.get_app_config_manager().get_logger_for(__name__)
        self.__track_hub = track_hub

    def _get_logger(self):
        return self.__logger

    def _set_logger(self, logger):
        self.__logger = logger

    def add_track(self, assembly, track_db, big_data_file):
        # TODO
        pass

    def get_product(self):
        # TODO
        pass


# Specialized track hub builders
class PrideFtpTrackHubBuilder(TrackHubBuilder):
    def __init__(self, track_hub):
        super(PrideFtpTrackHubBuilder, self).__init__(track_hub)


# Model for a TrackDb
class TrackDb:
    _SEPARATOR_CHAR = ' '

    def __init__(self, track, short_label, long_label):
        # Client side of the model
        self.__track = track
        self.__short_label = short_label
        self.__long_label = long_label
        # Builder side of the model
        self.__type = None
        self.__big_data_url = None

    def __identify_track_type_from_file(self, file_path):
        # TODO - We return the default type right now, but this will change in the future
        return 'bed'

    def set_type(self, file_path):
        self.__type = self.__identify_track_type_from_file(file_path)

    def set_big_data_url(self, big_data_url):
        self.__big_data_url = big_data_url

    def get_track(self):
        return self.__track

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
            f.write("track{}{}\n"
                    "type{}{}\n"
                    "bigDataUrl{}{}\n"
                    "shortLabel{}{}\n"
                    "longLabel{}{}"
                    .format(self._SEPARATOR_CHAR, self.get_track(),
                            self._SEPARATOR_CHAR, self.get_type(),
                            self._SEPARATOR_CHAR, self.get_big_data_url(),
                            self._SEPARATOR_CHAR, self.get_short_label(),
                            self._SEPARATOR_CHAR, self.get_long_label()))


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
            f.write("hub{}{}\n"
                    "shortLabel{}{}\n"
                    "longLabel{}{}\n"
                    "genomesFile{}{}\n"
                    "email{}{}\n"
                    "descriptionUrl{}{}"
                    .format(self._SEPARATOR_CHAR, self.get_hub(),
                            self._SEPARATOR_CHAR, self.get_short_label(),
                            self._SEPARATOR_CHAR, self.get_long_label(),
                            self._SEPARATOR_CHAR, self.get_genomes_file(),
                            self._SEPARATOR_CHAR, self.get_email(),
                            self._SEPARATOR_CHAR, self.get_description_url()))


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
