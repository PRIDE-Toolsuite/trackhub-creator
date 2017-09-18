# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 18-09-2017 09:48
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This toolbox models assembly mapping services between Ensembl and UCSC
"""

import abc
# Application imports
import config_manager
from exceptions import AppException


# Exceptions
class AssemblyMappingServiceException(AppException):
    def __init__(self, value):
        super().__init__(value)


# Abstract Factory
class AssemblyMappingServiceFactory:
    pass


# Assembly Mapping Services
class AssemblyMappingService(metaclass=abc.ABCMeta):
    def __init__(self):
        self._logger = config_manager \
            .get_app_config_manager() \
            .get_logger_for("{}.{}".format(__name__, type(self).__name__))

    @abc.abstractmethod
    def map_ensembl_to_ucsc(self, ensembl_assembly_accession):
        """
        Given an Ensembl Assembly Accession, get its corresponding UCSC Assembly name
        :param ensembl_assembly_accession: Ensembl assembly accession
        :return: its corresponding UCSC assembly name
        """
        ...


class AssemblyMappingServiceFromStaticFile(AssemblyMappingService):
    pass


class AssemblyMappingServiceFromEnsembl(AssemblyMappingService):
    pass


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
