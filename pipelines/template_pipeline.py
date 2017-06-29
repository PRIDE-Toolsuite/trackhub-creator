# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 29-06-2017 15:05
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This is a template pipeline for refactoring out things from final pipelines as I identify how they're gonna look like
"""

from exceptions import PipelineDirectorException


class Director():
    """
    This is the director of the pipeline
    """
    def __init__(self, config_file_name, runner_id = 0):
        #TODO
        pass

    def _before(self):
        # TODO
        pass

    def run(self):
        self._before()
        self._run_pipeline()
        self._after()

    def _run_pipeline(self):
        raise NotImplementedError("Implement your main pipeline logic here")

    def _after(self):
        # TODO
        pass
