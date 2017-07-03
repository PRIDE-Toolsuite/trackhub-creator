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