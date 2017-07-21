# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 21-07-2017 14:21
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Unit Tests for toolboxes
"""

import os
import unittest
# App modules
import config_manager
from download_manager.manager import Manager as DownloadManager
import toolbox.general as general_toolbox


class TestToolboxes(unittest.TestCase):
    __logger = config_manager.get_app_config_manager().get_logger_for(__name__)

    def test_gunzip_files(self):
        file_url = 'ftp://ftp.ensembl.org/pub/release-89/gtf/homo_sapiens/Homo_sapiens.GRCh38.89.abinitio.gtf.gz'
        file_name = file_url[file_url.rfind('/') + 1:]
        file_name_uncompressed = file_name[:file_name.rfind('.')]
        # Download the file to the session working directory
        destination_folder = config_manager.get_app_config_manager().get_session_working_dir()
        destination_file_path = os.path.join(destination_folder, file_name)
        destination_file_path_uncompressed = os.path.join(destination_folder, file_name_uncompressed)
        self.__logger.info("Using test file '{}', from '{}' for testing gunzip functionality at folder '{}'"
                           .format(file_name,
                                   file_url,
                                   destination_folder))
        download_manager = DownloadManager([file_url], destination_folder, self.__logger)
        download_manager.start_downloads()
        download_manager.wait_all()
        self.assertTrue(download_manager.is_success(), "Test files for gunzip unit test downloaded successfully")
        errors = general_toolbox.gunzip_files([destination_file_path])
        self.assertTrue(not errors, "No errors uncompressing test files for unit testing gunzip feature")
        self.assertTrue(os.path.isfile(destination_file_path_uncompressed), "The test file has been uncompressed, '{}'"
                        .format(destination_file_path_uncompressed))
        
