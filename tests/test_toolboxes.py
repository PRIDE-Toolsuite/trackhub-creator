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
        # Download the file to the session working directory
        destination_folder = config_manager.get_app_config_manager().get_session_working_dir()
        self.__logger.info("Using test file '{}', from '{}' for testing gunzip functionality at folder '{}'"
                           .format(file_name,
                                   file_url,
                                   destination_folder))
        download_manager = DownloadManager([file_url], destination_folder, self.__logger)
        