# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 03-07-2017 16:50
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This module contains Ensembl models used as Entities and DAO/Services
"""

import config_manager


class Species:
    def __init__(self, ensembl_species_entry):
        self.__ensembl_species_entry = ensembl_species_entry
        self.__logger = config_manager.get_app_config_manager().get_logger_for(__name__)

    def _get_logger(self):
        return self.__logger

    def _get_value_for_key_or_default(self, key, default='-not_available-'):
        if key in self.get_ensembl_species_entry():
            return self.get_ensembl_species_entry()[key]
        return default

    def get_ensembl_species_entry(self):
        return self.__ensembl_species_entry

    def get_division(self):
        return self._get_value_for_key_or_default('division')

    def get_ncbi_taxonomy_id(self):
        return self._get_value_for_key_or_default('taxon_id')

    def get_name(self):
        return self._get_value_for_key_or_default('name')

    def get_ensembl_release(self):
        return self._get_value_for_key_or_default('release')

    def get_display_name(self):
        return self._get_value_for_key_or_default('display_name')

    def get_assembly_accession(self):
        return self._get_value_for_key_or_default('accession')

    def get_strain_collection(self):
        if self._get_value_for_key_or_default('strain_collection', 'null') == 'null':
            return None
        return self._get_value_for_key_or_default('strain_collection')

    def get_common_name(self):
        return self._get_value_for_key_or_default('common_name')

    def get_strain(self):
        return self._get_value_for_key_or_default('strain')

    def get_aliases(self):
        return self._get_value_for_key_or_default('aliases', [])

    def get_groups(self):
        return self._get_value_for_key_or_default('groups', [])

    def get_assembly(self):
        return self._get_value_for_key_or_default('assembly')


class SpeciesService:
    def __init__(self, species_data):
        self.__logger = config_manager.get_app_config_manager().get_logger_for(__name__)
        # I've changed this, we store the original species data, and then we offer two different views
        self.__species_data = species_data
        self.__index_by_taxonomy_id = None

    @staticmethod
    def __index_data_for_property(data, property_getter):
        """
        Given an iterable data container, and a property getter to run on every object of that container, it returns a
        dictionary where the key is the property value for a particular data object part of the data collection
        :param data: iterable of data objects to index
        :param property_getter: property on which the index should be created
        :return: a dictionary of the given data objects where the key is the indexed property
        """
        return {property_getter(data_item): data_item for data_item in data}

    def _get_logger(self):
        return self.__logger

    def _get_species_from_species_data(self):
        return self.get_species_data()['species']

    def _get_index_taxonomy_id(self):
        """
        Build the index for species data by taxonomy ID
        :return: ensembl species data indexed by taxonomy ID
        """
        if self.__index_by_taxonomy_id is None:
            self.__index_by_taxonomy_id = \
                self.__index_data_for_property(self._get_species_from_species_data(), Species.get_ncbi_taxonomy_id)
        return self.__index_by_taxonomy_id

    def get_species_data(self):
        return self.__species_data

    def get_species_entry_for_taxonomy_id(self, taxonomy_id):
        """
        Given a taxonomy ID, get its Ensembl species entry
        :param taxonomy_id: taxonomy ID
        :return: the species entry or None if not found
        """
        if taxonomy_id in self._get_index_taxonomy_id():
            return self._get_index_taxonomy_id()[taxonomy_id]
        return None
