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
        pass
