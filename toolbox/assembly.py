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


class AssemblyMappingServiceFromStaticFileException(AssemblyMappingServiceException):
    def __init__(self, value):
        super().__init__(value)


# Assembly model
class Assembly:
    _ASSEMBLY_DATABASE_ENSEMBL = 'Ensembl'
    _ASSEMBLY_DATABASE_UCSC = 'UCSC'

    def __init__(self, database = _ASSEMBLY_DATABASE_ENSEMBL,
                 name = '---NOT_SET---',
                 accession = '---NOT_SET---',
                 level = '---NOT_SET---',
                 id = '---NOT_SET---',
                 base_count = '---NOT_SET---'):
        self.database = database
        self.name = name
        self.accession = accession
        self.level = level
        self.id = id
        self.base_count = base_count


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
    # Default URL to get the assembly mapping data
    _CONFIG_URL_ASSEMBLY_MAPPING_DATA = \
        'https://github.com/Proteogenomics/assembly-mapping-data/raw/master/ensembl_ucsc_assembly_mapping.json'

    def __init__(self):
        self._logger = config_manager \
            .get_app_config_manager() \
            .get_logger_for("{}.{}".format(__name__, type(self).__name__))
        self.__raw_assembly_data_object = None
        self.__index_by_accession_ensembl_assembly = None
        self.__index_by_ensembl_accession_ucsc_assembly = None



class AssemblyMappingServiceFromEnsembl(AssemblyMappingService):
    pass


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
