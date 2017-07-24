# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 24-07-2017 10:04
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Unit tests for Ensembl Data Downloader
"""

import unittest
# Application imports
import config_manager
import ensembl.data_downloader


class TestEnsemblDataDownloader(unittest.TestCase):
    __logger = config_manager.get_app_config_manager().get_logger_for(__name__)

    def test_get_protein_sequences_for_human(self):
        human_ncbi_tax_id = '9606'
        ensembl_downloader_service = ensembl.data_downloader.get_data_download_service()
        ensembl_downloader_service.get_protein_sequences_for_species(human_ncbi_tax_id)

    def test_get_gtf_for_human(self):
        # TODO
        pass


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
