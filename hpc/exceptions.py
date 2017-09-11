# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 11-09-2017 11:39
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
HPC module exceptions
"""

# App imports
from exceptions import AppException


class HpcServiceFactoryException(AppException):
    def __init__(self, value):
        super().__init__(value)


class HpcServiceException(AppException):
    def __init__(self, value):
        super().__init__(value)


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
