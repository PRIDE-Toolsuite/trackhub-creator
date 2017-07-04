# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 03-07-2017 11:10
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Pipeline related exceptions
"""
from exceptions import AppException


class PipelineDirectorException(AppException):
    def __init__(self, value):
        super(AppException, self).__init__(value)


if __name__ == '__main__':
    print(
        "ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
