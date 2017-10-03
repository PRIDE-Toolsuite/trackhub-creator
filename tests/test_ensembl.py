# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 03-07-2017 11:51
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Unit tests for Ensembl module
"""

import unittest
# App modules
import config_manager
import ensembl.service


class TestEnsemblService(unittest.TestCase):
    def setUp(self):
        self.logger = config_manager.get_app_config_manager() \
            .get_logger_for("{}.{}".format(__name__, type(self).__name__))

    def test_test(self):
        """
        This test has been used just for setting up the unit testing subsystem.
        It always passes.
        :return: no return value
        """
        pass

    def test_get_ensembl_current_release(self):
        service = ensembl.service.get_service()
        current_release_number = service.get_release_number()
        print("Current release number ---> {}".format(current_release_number))

    def test_chromosome_sizes(self):
        taxonomy_ids = ['9606', '10090']
        for taxonomy in taxonomy_ids:
            chromosome_sizes = ensembl.service.get_service().get_chromosome_sizes_for_taxonomy(taxonomy)
            self.assertIsNotNone(chromosome_sizes, "We got chromosome sizes")
            self.logger.debug("Chromosome sizes for taxonomy '{}' ---> '{}'".format(taxonomy, str(chromosome_sizes)))

    def test_ucsc_chromosome_sizes(self):
        taxonomy_ids = ['9606', '10090']
        for taxonomy in taxonomy_ids:
            chromosome_sizes = ensembl.service.get_service().get_ucsc_chromosome_sizes_for_taxonomy(taxonomy)
            self.assertIsNotNone(chromosome_sizes, "We got chromosome sizes")
            self.logger.debug("UCSC Chromosome sizes for taxonomy '{}' ---> '{}'".format(taxonomy, str(chromosome_sizes)))


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
