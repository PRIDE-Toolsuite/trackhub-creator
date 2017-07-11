# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 11-07-2017 10:40
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Unit Tests for the download manager module
"""

import unittest
# App imports
import config_manager
from download_manager.manager import Manager as DownloadManager


class TestDownloadManager(unittest.TestCase):
    __logger = config_manager.get_app_config_manager().get_logger_for(__name__)

    def test_success_on_sample_files_download(self):
        urls = ['ftp://ftp.ensembl.org/pub/release-89/fasta/homo_sapiens/pep/Homo_sapiens.GRCh38.pep.all.fa.gz',
                'ftp://ftp.ensembl.org/pub/release-89/fasta/homo_sapiens/pep/Homo_sapiens.GRCh38.pep.abinitio.fa.gz',
                'ftp://ftp.ensembl.org/pub/release-89/gtf/homo_sapiens/Homo_sapiens.GRCh38.89.abinitio.gtf.gz',
                'ftp://ftp.ensembl.org/pub/release-89/gtf/homo_sapiens/Homo_sapiens.GRCh38.89.chr.gtf.gz']
        destination_folder = config_manager.get_app_config_manager().get_folder_run()
        # Log the test environment
        self.__logger.info("Sample file URLs to download: {}".format(",".join(urls)))
        self.__logger.info("Destination folder for the downloads, '{}'".format(destination_folder))
        # Get the download manager and start the downloads
        download_manager = DownloadManager(urls, destination_folder, self.__logger)
        download_manager.start_downloads()
        download_manager.wait_all()
        self.assertTrue(download_manager.is_success(), "Files downloaded successfully")


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
