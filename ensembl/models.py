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

    def get_division(self):
        # TODO
        pass

    def get_ncbi_taxonomy_id(self):
        # TODO
        pass

    def get_name(self):
        # TODO
        pass

    def get_ensembl_release(self):
        # TODO
        pass

    def get_display_name(self):
        # TODO
        pass

    def get_assembly_accession(self):
        # TODO
        pass

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
