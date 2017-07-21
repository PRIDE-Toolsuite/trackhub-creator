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
import toolbox.general as general_toolbox


class TestToolboxes(unittest.TestCase):
    def test_gunzip_files(self):
        file_url = 'ftp://ftp.ensembl.org/pub/release-89/gtf/homo_sapiens/Homo_sapiens.GRCh38.89.abinitio.gtf.gz';
