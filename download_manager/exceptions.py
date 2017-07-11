# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 07-07-2017 11:17
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Exceptions related to the download manager module
"""

from exceptions import AppException


class ManagerException(AppException):
    def __init__(self, value):
        super(ManagerException, self).__init__(value)


class AgentException(AppException):
    def __init__(self, value):
        super(AgentException, self).__init__(value)


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
