# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 02-08-2017 16:40
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This module contains models for dealing with PoGo stuff
"""


class PogoRunResult:
    def __init__(self):
        self.__ncbi_taxonomy_id = None
        self.__pogo_source_file_path = None
