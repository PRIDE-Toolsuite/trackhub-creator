# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 03-07-2017 11:51
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Unit tests for Ensembl module
"""

import unittest
# App modules
import ensembl.service


class TestEnsemblService(unittest.TestCase):
    def test_test(self):
        """
        This test has been used just for setting up the unit testing subsystem.
        It always passes.
        :return: no return value
        """
        pass

    def test_get_ensembl_current_release(self):
        service = ensembl.service.get_service()
        current_release_number = service.get_release_number()
        print("Current release number ---> {}".format(current_release_number))


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
