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

# Application imports
import config_manager
from toolbox import general
from pipelines.template_pipeline import DirectorConfigurationManager, Director