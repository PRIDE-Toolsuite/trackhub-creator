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

class TestEnsemblDataDownloader(unittest.TestCase):
    __logger = config_manager.get_app_config_manager().get_logger_for(__name__)
    