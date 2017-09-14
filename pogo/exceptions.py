# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 14-09-2017 7:09
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Exceptions for 'pogo' module
"""

# App imports
from exceptions import AppException


class PogoRunnerFactoryException(AppException):
    def __init__(self, value):
        super().__init__(value)


class PogoRunnerException(AppException):
    def __init__(self, value):
        super().__init__(value)


class PogoRunnerLocalThreadException(PogoRunnerException):
    def __init__(self, value):
        super().__init__(value)


class PogoRunnerHpcException(PogoRunnerException):
    def __init__(self, value):
        super().__init__(value)


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
