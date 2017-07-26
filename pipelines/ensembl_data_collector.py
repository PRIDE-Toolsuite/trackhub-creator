# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 26-07-2017 12:29
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This pipeline collects data from Ensembl to avoid race conditions when running other pipelines that use this data
"""

import time
# Application imports
import config_manager
from toolbox import general
from pipelines.template_pipeline import DirectorConfigurationManager, Director

__configuration_file = None
__pipeline_arguments = None


class ConfigManager(DirectorConfigurationManager):
    def __init__(self, configuration_object, configuration_file, pipeline_arguments):
        super(ConfigManager, self).__init__(configuration_object, configuration_file)


class EnsemblDataCollector(Director):
    def __init__(self):
        runner_id = "{}-{}".format(__name__, time.time())
        super(EnsemblDataCollector, self).__init__(runner_id)
