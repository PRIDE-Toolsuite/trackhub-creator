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
import toolbox
from exceptions import PipelineDirectorException

# The config manager singleton is just an example that only makes sense for specialized pipeline modules, not really for
# this template
__configuration_file = None
__configuration_manager = None


def __get_configuration_manager():
    global __configuration_manager
    if __configuration_manager is None:
        __configuration_manager = DirectorConfigurationManager(toolbox.read_json(__configuration_file),
                                                               __configuration_file)
    return __configuration_manager


class DirectorConfigurationManager(config_manager.ConfigurationManager):
    def __init__(self, configuration_object, configuration_file):
        super(DirectorConfigurationManager, self).__init__(configuration_object, configuration_file)


class Director:
    """
    This is the director of the pipeline
    """

    def __init__(self, config_file_name, runner_id=0):
        self.__logger = config_manager.get_app_config_manager().get_logger_for(__name__)

    def _before(self):
        """
        This method implements some logic that is run before running the main pipeline director.
        Subclasses implementing the pipeline logic, can override this method for establishing pre-pipeline logic.
        :return: it returns True if there was no problem, False otherwise
        """
        self._get_logger().debug("No behaviour has been defined for 'before' running the pipeline")
        return True

    def run(self):
        """
        Pipeline template director algorithm, it executes 'before' logic, then the 'pipeline' logic, and 'after' logic once the pipeline is finished
        :return: True if the pipeline has been successful, False otherwise
        """
        if not self._before():
            self._get_logger().error("The logic executed BEFORE running the pipeline has FAILED")
            return False
        if not self._run_pipeline():
            self._get_logger().error("The PIPELINE execution has FAILED")
            return False
        if not self._after():
            self._get_logger().error("The logic executed AFTER running the pipeline has FAILED")
            return False
        return True

    def _run_pipeline(self):
        """
        This abstract method must be implemented by the subclasses with the strategy / director logic that drives the
        pipeline they are performing
        :return: True if the pipeline is successful, False otherwise
        """
        raise NotImplementedError("Implement your main pipeline logic here")

    def _after(self):
        """
        This method implements the logic that must be executed after the pipeline workflow has run.
        Subclasses implementing the pipeline logic, can override this method for establishing post-pipeline logic.
        :return: True if success, False otherwise
        """
        self._get_logger().debug("No behaviour has been defined for 'after' running the pipeline")
        return True

    def _get_logger(self):
        """
        Get the logger to be used for logging messages
        :return: it returns the logger set for the current instance of the class
        """
        return self.__logger

    def _set_logger(self, new_logger):
        """
        This method allows subclasses to change the default logger created when instantiating an implementation of this abstract class.
        :param new_logger: a new logger to set up as the default logger for a particular implementation subclass instance
        :return: the newly set logger
        """
        self.__logger = new_logger
        return self._get_logger()


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not met to be run in stand alone mode")
