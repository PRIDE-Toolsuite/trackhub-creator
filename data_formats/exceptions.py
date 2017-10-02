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

from exceptions import AppException


class DataFormatConverterFactoryException(AppException):
    def __init__(self, value):
        super().__init__(value)


class DataFormatConverterException(AppException):
    def __init__(self, value):
        super().__init__(value)


class FileDataFormatConverterException(DataFormatConverterException):
    def __init__(self, value):
        super().__init__(value)


class BedToBigBedMultithreadedConverterException(FileDataFormatConverterException):
    def __init__(self, value):
        super().__init__(value)
