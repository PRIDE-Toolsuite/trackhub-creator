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

import config_manager
from exceptions import PipelineDirectorException


class Director:
    """
    This is the director of the pipeline
    """
    def __init__(self, config_file_name, runner_id = 0):
        self.__logger = config_manager.get_app_config_manager().get_logger_for(__name__)

    def _before(self):
        self._get_logger().debug("No behaviour has been defined for 'before' running the pipeline")
        return True

    def run(self):
        self._before()
        self._run_pipeline()
        self._after()

    def _run_pipeline(self):
        raise NotImplementedError("Implement your main pipeline logic here")

    def _after(self):
        # TODO
        pass

    def _get_logger(self):
        return self.__logger

    def _set_logger(self, new_logger):
        self.__logger = new_logger
        return self._get_logger()