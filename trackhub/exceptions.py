# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 24-08-2017 10:09
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Trackhub module exceptions
"""

# App imports
from exceptions import AppException


class TrackhubRegistryServiceException(AppException):
    def __init__(self, value):
        super().__init__(value)


class TrackHubExporterException(AppException):
    def __init__(self, value):
        super().__init__(value)


class TrackHubLocalFilesystemExporterException(TrackHubExporterException):
    def __init__(self, value):
        super().__init__(value)


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
