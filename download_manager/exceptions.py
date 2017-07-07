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


class DownloadException(AppException):
    def __init__(self, value):
        super(DownloadException, self).__init__(value)
