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

import abc
# App imports
import config_manager
from parallel.models import ParallelRunner


# Factories
class DataFormatConverterFactory:
    pass


# Possible base class for data format converters
class DataFormatConverter(ParallelRunner):
    def __init__(self):
        super().__init__()


class FileDataFormatConverter(DataFormatConverter):
    def __init__(self):
        super().__init__()
        self.file_path_source = ''

    @abc.abstractmethod
    def _get_command_line_runner(self):
        ...


class BedToBigBedMultithreadedConverter(FileDataFormatConverter):
    def __init__(self):
        super().__init__()
        self._logger = config_manager.get_app_config_manager()\
            .get_logger_for("{}.{}".format(__name__, type(self).__name__))

    def _run(self):
        pass
        # TODO
