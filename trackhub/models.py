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


# Trackhub builder
class TrackHubBuilder:
    # TODO
    pass


# Model for a TrackDb
class TrackDb:
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
