# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 28-09-2017 14:20
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This module offers converters between different formats
"""

from parallel.models import ParallelRunner


# Factories
class DataFormatConverterFactory:
    pass


# Possible base class for data format converters
class DataFormatConverter(ParallelRunner):
    def __init__(self):
        super().__init__()
        # TODO


class FileDataFormatConverter(DataFormatConverter):
    def __init__(self):
        super().__init__()


class BedToBigBedMultithreadedConverter(FileDataFormatConverter):
    def __init__(self):
        super().__init__()
