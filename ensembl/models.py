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
        # TODO
        pass

    def get_common_name(self):
        # TODO
        pass

    def get_strain(self):
        # TODO
        pass

    def get_aliases(self):
        # TODO
        pass

    def get_groups(self):
        # TODO
        pass

    def get_assembly(self):
        # TODO
        pass


class SpeciesService:
    # TODO
    pass
