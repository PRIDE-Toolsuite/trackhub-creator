# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 13-09-2017 13:10
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Unit tests for the parallelization module
"""

import unittest
# App imports
import config_manager


class TestCommandLineRunner(unittest.TestCase):
    __logger = config_manager.get_app_config_manager().get_logger_for("{}.{}".format(__name__, type(self).__name__))
