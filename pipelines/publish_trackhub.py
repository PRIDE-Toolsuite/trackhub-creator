# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 30-10-2017 09:33
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This pipeline publishes the given trackhub to trackhubregistry.org

A JSON formatted file is given as a parameter to the pipeline
    trackhub_description=input_file.json
And this file contains the following information:
{
    "trackhubUrl": "Name for the trackhub being published",
    "public": "1",
    "type": "PROTEOMICS",
    "pipelineReportFilePath": "pipeline.report"
}

Description of parameters:
    pipelineReportFilePath  ->  Absolute path to a JSON formatted file that contains information about the pipeline
                                execution
"""

# Globals
__configuration_file = None
__pipeline_arguments = None
__pipeline_director = None
