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

    def test_success_on_running_simple_command_without_timeout(self):
        command = "echo Successful_run"


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
