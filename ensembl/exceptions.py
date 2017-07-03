# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 03-07-2017 11:14
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Ensembl module related exceptions
"""
from exceptions import AppException


class EnsemblServiceException(AppException):
    def __init__(self, value):
        super(EnsemblServiceException, self).__init__(value)
