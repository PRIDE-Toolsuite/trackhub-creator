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
from parallel.models import ParallelRunner, CommandLineRunnerFactory


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


class BedToBigBedConverter(FileDataFormatConverter):
    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def _get_command_line_runner(self):
        ...

    def _run(self):
        pass
        # TODO - Conversion algorithm goes here


class BedToBigBedMultithreadedConverter(BedToBigBedConverter):
    def __init__(self):
        self._logger = config_manager.get_app_config_manager() \
            .get_logger_for("{}.{}".format(__name__, type(self).__name__))

    def _get_command_line_runner(self):
        return CommandLineRunnerFactory.get_multithread_command_line_runner()


class BedToBigBedHpcConverter(BedToBigBedConverter):
    pass


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
