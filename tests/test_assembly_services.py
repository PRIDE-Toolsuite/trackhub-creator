# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 18-09-2017 12:19
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Unit tests for assembly services
"""

import unittest
# Application imports
import ensembl.service
from toolbox.assembly import AssemblyMappingServiceFactory


class TestAssemblyMappingServices(unittest.TestCase):
    def test_ensembl_species_has_mapping(self):
        ensembl_service = ensembl.service.get_service()
        sample_ncbi_taxonomies = ['9606', '10090']
        species_data_service = ensembl_service.get_species_data_service()
        assembly_mapping_service = AssemblyMappingServiceFactory.get_assembly_mapping_service()
        for taxonomy_id in sample_ncbi_taxonomies:
            ensembl_species_data_entry = species_data_service.get_species_entry_for_taxonomy_id(taxonomy_id)
            self.assertIsNotNone("NCBI Taxonomy ID #{} with accession '{}' Maps to UCSC Assembly name '{}'"
                                 .format(taxonomy_id,
                                         ensembl_species_data_entry.get_assembly_accession(),
                                         assembly_mapping_service
                                         .get_ucsc_assembly_for_ensembl_assembly_accession(
                                             ensembl_species_data_entry.get_assembly_accession())))


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
