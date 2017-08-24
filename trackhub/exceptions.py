# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 24-08-2017 10:09
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Trackhub module exceptions
"""

# App imports
from exceptions import AppException


class TrackhubRegistryServiceException(AppException):
    def __init__(self, value):
        super().__init__(value)
