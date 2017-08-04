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


# Model for a Track
class Track:
    # TODO
    pass


# Model for a trackhub
class TrackHub:
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
    
