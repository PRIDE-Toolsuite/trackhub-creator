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
import main_app
import ensembl.service
from ensembl.models import Species, SpeciesService


class TestEnsemblSpeciesService(unittest.TestCase):
    def setUp(self):
        self.ensembl_service = ensembl.service.get_service()

    def test_get_species_data(self):
        species_data_service = self.ensembl_service.get_species_data_service()
        self.assertIsNotNone(species_data_service.get_species_data())

    def test_count_of_species(self):
        self.assertNotEqual(self.ensembl_service.get_species_data_service().count_ensembl_species(),
                            0,
                            "Ensembl has a non-zero number of species")
