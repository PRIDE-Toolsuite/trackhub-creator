# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 18-09-2017 09:48
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This toolbox models assembly mapping services between Ensembl and UCSC
"""

import abc
# Application imports
import config_manager


# Abstract Factory
class AssemblyMappingServiceFactory:
    pass


class AssemblyMappingService(metaclass=abc.ABCMeta):
    pass


class AssemblyMappingServiceFromStaticFile(AssemblyMappingService):
    pass


class AssemblyMappingServiceFromEnsembl(AssemblyMappingService):
    pass


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
