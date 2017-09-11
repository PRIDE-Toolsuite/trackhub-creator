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


class HpcServiceFactory:
    # Constants
    _HPC_TYPE_LSF = 'lsf'

    @staticmethod
    def get_hpc_service():
        pass

    @staticmethod
    def get_hpc_environment_type():
        # More HPC environments will be added in the future
        if os.environ.get('LSB_JOBID'):
            return HpcServiceFactory._HPC_TYPE_LSF


class HpcServiceLsf:
    def __init__(self):
        pass
