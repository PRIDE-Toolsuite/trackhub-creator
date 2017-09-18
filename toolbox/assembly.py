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
import json
import requests
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
    # TODO - Due to the nature of the mapping data provided in this first iteration, I won't use this model
    _ASSEMBLY_DATABASE_ENSEMBL = 'Ensembl'
    _ASSEMBLY_DATABASE_UCSC = 'UCSC'

    def __init__(self, database=_ASSEMBLY_DATABASE_ENSEMBL,
                 name='---NOT_SET---',
                 accession='---NOT_SET---',
                 level='---NOT_SET---',
                 id='---NOT_SET---',
                 base_count='---NOT_SET---'):
        self.database = database
        self.name = name
        self.accession = accession
        self.level = level
        self.id = id
        self.base_count = base_count

class MappingEntry:
    """
    As mapping entry, as received from the mapping file, looks like this:
    {
        "assembly_name": "KH",
        "assembly_level": "chromosome",
        "assembly_accession": "GCA_000224145.1",
        "assembly_id": 2,
        "base_count": 115227500,
        "assembly_ucsc": "ci2"
    }
    """
    # Mapping keys
    _MAPPING_ENTRY_KEY_ENSEMBL_ASSEMBLY_NAME = 'assembly_name'
    _MAPPING_ENTRY_KEY_ENSEMBL_ASSEMBLY_LEVEL = 'assembly_level'
    _MAPPING_ENTRY_KEY_ENSEMBL_ASSEMBLY_ACCESSION = 'assembly_accession'
    _MAPPING_ENTRY_KEY_ENSEMBL_ASSEMBLY_ID = 'assembly_id'
    _MAPPING_ENTRY_KEY_ENSEMBL_ASSEMBLY_BASE_COUNT = 'base_count'
    _MAPPING_ENTRY_KEY_UCSC_ASSEMBLY_NAME = 'assembly_ucsc'

    def __init__(self, mapping_entry_object):
        self.mapping_entry_object = mapping_entry_object

    def __get_value_for_key_or_default(self, key, default='---NOT_SET---'):
        # I could have used 'getattr' but I wrote this method to avoid myself repeating '---NOT_SET---' at the callers
        if key in self.mapping_entry_object:
            value = self.mapping_entry_object[key]
        return default

    def get_ensembl_assembly_name(self):
        return self.__get_value_for_key_or_default(self._MAPPING_ENTRY_KEY_ENSEMBL_ASSEMBLY_NAME)

    def get_ensembl_assembly_level(self):
        return self.__get_value_for_key_or_default(self._MAPPING_ENTRY_KEY_ENSEMBL_ASSEMBLY_LEVEL)

    def get_ensembl_assembly_accession(self):
        return self.__get_value_for_key_or_default(self._MAPPING_ENTRY_KEY_ENSEMBL_ASSEMBLY_ACCESSION)

    def get_ensembl_assembly_id(self):
        return self.__get_value_for_key_or_default(self._MAPPING_ENTRY_KEY_ENSEMBL_ASSEMBLY_ID)

    def get_ensembl_assembly_base_count(self):
        return self.__get_value_for_key_or_default(self._MAPPING_ENTRY_KEY_ENSEMBL_ASSEMBLY_BASE_COUNT)

    def get_ucsc_assembly_name(self):
        return self.__get_value_for_key_or_default(self._MAPPING_ENTRY_KEY_UCSC_ASSEMBLY_NAME)


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
        # URL for the json formatted mapping file
        self.url_assembly_mapping_data = None

    def __get_url_assembly_mapping_data(self):
        if self.url_assembly_mapping_data:
            return self.url_assembly_mapping_data
        return self._CONFIG_URL_ASSEMBLY_MAPPING_DATA

    def _get_raw_assembly_data_object(self):
        if not self.__raw_assembly_data_object
            self._logger.info("Loading Assembly Mapping data between Ensembl and UCSC from '{}'"
                              .format(self.__get_url_assembly_mapping_data()))
            self.__raw_assembly_data_object = json.loads(requests.get(self.__get_url_assembly_mapping_data()).content)
            self._logger.info("#{} assembly mapping entries between Ensembl and UCSC loaded from '{}"
                              .format(len(self.__raw_assembly_data_object),
                                      self.__get_url_assembly_mapping_data()))
            # I will cache the content of the file, as it's too small to cause problems
        return self.__raw_assembly_data_object

    def _get_index_by_accession_ensembl_assembly(self):
        # WARNING - This index can be based on the assumption that the raw mapping data is Ensembl centric, which means
        # every Ensembl assembly accession appears only once, and it has a unique mapping to UCSC, that's not
        # necessarily the case the other way around
        if not self.__index_by_accession_ensembl_assembly:
            self.__index_by_accession_ensembl_assembly = {}
            for raw_mapping_entry in self._get_raw_assembly_data_object():
                mapping_entry = MappingEntry(raw_mapping_entry)
                if mapping_entry.get_ensembl_assembly_accession() in self.__index_by_accession_ensembl_assembly:
                    self._logger.error("DUPLICATED ENSEMBL ASSEMBLY ACCESSION ENTRY!!! '{}',"
                                       " the one already in the index is '{}' - MAPPING ENTRY SKIPPED"
                                       .format(json.dumps(raw_mapping_entry),
                                               json.dumps(self.__index_by_accession_ensembl_assembly
                                                          .mapping_entry_object)))
                self.__index_by_accession_ensembl_assembly[mapping_entry.get_ensembl_assembly_accession()] = \
                    mapping_entry
        return self.__index_by_accession_ensembl_assembly

    def _get_index_by_ensembl_accession_ucsc_assembly(self):
        pass

    def get_ucsc_assembly_for_ensembl_assembly_accession(self):
        pass


class AssemblyMappingServiceFromEnsembl(AssemblyMappingService):
    pass


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
