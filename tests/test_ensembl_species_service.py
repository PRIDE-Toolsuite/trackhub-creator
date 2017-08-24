# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 04-07-2017 09:14
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Unit Tests for Ensembl Species Service
"""

import unittest
# App modules
import ensembl.service


class TestEnsemblSpeciesService(unittest.TestCase):
    __NCB_TAXONOMY_HUMAN = '9606'

    def setUp(self):
        self.ensembl_service = ensembl.service.get_service()

    def test_get_species_data(self):
        species_data_service = self.ensembl_service.get_species_data_service()
        self.assertIsNotNone(species_data_service.get_species_data(),
                             "Requested RAW species data from Ensembl IS NOT None")

    def test_count_of_species(self):
        self.assertNotEqual(self.ensembl_service.get_species_data_service().count_ensembl_species(),
                            0,
                            "Ensembl has a non-zero number of species")

    def test_human_species_is_present(self):
        """
        Test that Human taxonomy is present, this unit test is also testing the indexing mechanism
        :return: no returned value
        """
        self.assertIsNotNone(
            self.ensembl_service.get_species_data_service().get_species_entry_for_taxonomy_id(
                self.__NCB_TAXONOMY_HUMAN), "Human NCBI taxonomy is in species data from Ensembl")

    def test_assembly_to_taxonomy_translation(self):
        pass


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
