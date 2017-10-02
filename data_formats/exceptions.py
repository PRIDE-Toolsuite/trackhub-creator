# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 02-10-2017 11:36
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Exceptions module
"""

from parallel.exceptions import ParallelRunnerException


class DataFormatConverterFactoryException(ParallelRunnerException):
    def __init__(self, value):
        super().__init__(value)


class DataFormatConverterException(ParallelRunnerException):
    def __init__(self, value):
        super().__init__(value)


class FileDataFormatConverterException(DataFormatConverterException):
    def __init__(self, value):
        super().__init__(value)


class BedToBigBedConverterException(FileDataFormatConverterException):
    def __init__(self, value):
        super().__init__(value)


class BedToBigBedMultithreadedConverterException(BedToBigBedConverterException):
    def __init__(self, value):
        super().__init__(value)


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
