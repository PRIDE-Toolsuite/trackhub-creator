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
import ensembl.service as ensembl_service
from . import config_manager as module_config_manager
from parallel.models import ParallelRunner, CommandLineRunnerFactory
from .exceptions import DataFormatConversionNotFinished


# Factories
class DataFormatConverterFactory:
    pass


# Possible base class for data format converters
class DataFormatConverter(ParallelRunner):
    def __init__(self):
        super().__init__()
        self.conversion_status_error = False
        self._stdout = []
        self._stderr = []

    def get_conversion_output(self):
        if not self.is_done():
            raise DataFormatConversionNotFinished("{} - NOT FINISHED YET".format(self._get_conversion_details))
        return "\n".join(self._stdout)

    def get_conversion_output_error(self):
        if not self.is_done():
            raise DataFormatConversionNotFinished("{} - NOT FINISHED YET".format(self._get_conversion_details))
        return "\n".join(self._stderr)

    @abc.abstractmethod
    def _get_conversion_details(self):
        ...

    def is_conversion_ok(self):
        if not self.is_done():
            raise DataFormatConversionNotFinished("{} - NOT FINISHED YET".format(self._get_conversion_details))
        return self.conversion_status_error or super().is_error()


class FileDataFormatConverter(DataFormatConverter):
    def __init__(self):
        super().__init__()
        self.file_path_source = ''
        self.file_path_destination = ''


class BedToBigBedConverter(FileDataFormatConverter):
    def __init__(self):
        super().__init__()
        self.taxonomy_id = ''

    @staticmethod
    def get_bed_to_bigbed_conversion_command(input_file_path, chromosome_sizes_file_path, output_file_path):
        return "time {} {} {} {}" \
            .format(
                module_config_manager.get_configuration_service().get_file_path_binary_bed_to_bigbed_conversion_tool(),
                input_file_path,
                chromosome_sizes_file_path,
                output_file_path)

    @abc.abstractmethod
    def _get_command_line_runner(self):
        ...

    def _sort_bed_file(self, bed_file_path, sorted_bed_file_path):
        runner = self._get_command_line_runner()
        runner.command = "time sort -k1,1 -k2,2n {} > {}".format(bed_file_path, sorted_bed_file_path)
        runner.start()
        return runner

    def _fetch_and_dump_chromosome_sizes(self, taxonomy_id, chromosome_sizes_file_path):
        chromosome_sizes = ensembl_service.get_service().get_ucsc_chromosome_sizes_for_taxonomy(taxonomy_id)
        with open(chromosome_sizes_file_path, 'w') as wf:
            for chromosome, size in chromosome_sizes.items():
                wf.write("{}\t{}".format(chromosome, size))
        return chromosome_sizes

    def _run(self):
        file_path_sorted_bed = "{}_sorted.bed".format(self.file_path_source[:self.file_path_source.rfind('.')])
        file_path_chromosome_sizes = "chromosome_sizes_{}.txt".format(self.taxonomy_id)
        # TODO - Conversion algorithm goes here -
        # Sort the .bed file
        runner_sort = self._sort_bed_file(self.file_path_source, file_path_sorted_bed)
        # Fetch chromosome sizes for this .bed file
        chromosome_sizes = self._fetch_and_dump_chromosome_sizes(self.taxonomy_id, file_path_chromosome_sizes)
        runner_sort.wait()
        self._stdout.append(runner_sort.get_stdout())
        self._stderr.append(runner_sort.get_stderr())
        if not runner_sort.command_success:
            self.conversion_status_error = True
            return False
        # Use bedToBigBed utility to create the .bb (bigBed) file
        runner_conversion = self._get_command_line_runner()
        runner_conversion.command = self.get_bed_to_bigbed_conversion_command(self.file_path_source,
                                                                              file_path_chromosome_sizes,
                                                                              self.file_path_destination)
        runner_conversion.start()
        runner_conversion.wait()
        self._stdout.append(runner_conversion.get_stdout())
        self._stderr.append(runner_conversion.get_stderr())
        if not runner_conversion.command_success:
            self.conversion_status_error = True
            return False
        return True


# Leaves - actual implementations
class BedToBigBedMultithreadedConverter(BedToBigBedConverter):
    def __init__(self):
        super().__init__()
        self._logger = config_manager.get_app_config_manager() \
            .get_logger_for("{}.{}".format(__name__, type(self).__name__))

    def _get_conversion_details(self):
        # TODO
        pass

    def _get_command_line_runner(self):
        return CommandLineRunnerFactory.get_multithread_command_line_runner()


class BedToBigBedHpcConverter(BedToBigBedConverter):
    pass


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
