# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 11-09-2017 11:14
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Models representing different HPC environments
"""

import os
# Application imports
import config_manager
from .exceptions import HpcServiceFactoryException


class HpcServiceFactory:
    # Constants
    _HPC_TYPE_LSF = 'lsf'
    _HPC_TYPE_NONE = 'no_hpc_environment_present'

    @staticmethod
    def get_hpc_service():
        pass

    @staticmethod
    def get_hpc_environment_type():
        # More HPC environments will be added in the future
        if os.environ.get('LSB_JOBID'):
            return HpcServiceFactory._HPC_TYPE_LSF
        return HpcServiceFactory._HPC_TYPE_NONE


class HpcServiceLsf:
    def __init__(self):
        self._logger = config_manager\
            .get_app_config_manager()\
            .get_logger_for("{}.{}".format(__name__, type(self).__name__))
