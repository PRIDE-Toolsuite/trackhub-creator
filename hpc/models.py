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
import abc
# Application imports
import config_manager
from .exceptions import HpcServiceFactoryException, HpcServiceException


class HpcServiceFactory:
    # Constants
    _HPC_TYPE_LSF = 'lsf'
    _HPC_TYPE_NONE = 'no_hpc_environment_present'

    @staticmethod
    def get_hpc_service():
        if HpcServiceFactory.get_hpc_environment_type() == HpcServiceFactory._HPC_TYPE_LSF:
            return HpcServiceLsf()
        raise HpcServiceFactoryException("HPC Environment NOT PRESENT or UNKNOWN")

    @staticmethod
    def get_hpc_environment_type():
        # More HPC environments will be added in the future
        if os.environ.get('LSB_JOBID'):
            return HpcServiceFactory._HPC_TYPE_LSF
        return HpcServiceFactory._HPC_TYPE_NONE


# HPC Service models
# Abstract base class
class HpcService(metaclass=abc.ABCMeta):
    def __init__(self):
        self._logger = config_manager \
            .get_app_config_manager() \
            .get_logger_for("{}.{}".format(__name__, type(self).__name__))

    @abc.abstractmethod
    def get_current_job_id(self):
        ...


# LSF
class HpcServiceLsf(HpcService):
    # Constants
    _LSF_ENVIRONMENT_VAR_JOB_ID = 'LSB_JOBID'
    _LSF_ENVIRONMENT_VAR_FILE_OUTPUT = 'LSB_OUTPUTFILE'
    _LSF_ENVIRONMENT_VAR_FILE_OUTPUT_ERROR = 'LSB_ERRORFILE'

    def __init__(self):
        super().__init__()
        self._logger = config_manager \
            .get_app_config_manager() \
            .get_logger_for("{}.{}".format(__name__, type(self).__name__))

    def get_current_job_id(self):
        if os.environ.get(HpcServiceLsf._LSF_ENVIRONMENT_VAR_JOB_ID):
            return os.environ.get(HpcServiceLsf._LSF_ENVIRONMENT_VAR_JOB_ID)
        raise HpcServiceException("Could not retrieve LSF Job ID from environment variable '{}'"
                                  .format(HpcServiceLsf._LSF_ENVIRONMENT_VAR_JOB_ID))

    def get_current_job_file_output(self):
        if os.environ.get(HpcServiceLsf._LSF_ENVIRONMENT_VAR_FILE_OUTPUT):
            return os.environ.get(HpcServiceLsf._LSF_ENVIRONMENT_VAR_FILE_OUTPUT)
        return ""

    def get_current_job_file_output_error(self):
        pass

if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
