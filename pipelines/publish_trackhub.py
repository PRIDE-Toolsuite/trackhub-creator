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

import os
import time
import json
# Application imports
import config_manager
from pipelines.template_pipeline import Director, DirectorConfigurationManager

# Globals
__configuration_file = None
__pipeline_arguments = None
__pipeline_director = None


# TODO Pipeline Singleton Accessors
def set_configuration_file(config_file):
    global __configuration_file
    if __configuration_file is None:
        __configuration_file = config_file
    return __configuration_file


def set_pipeline_arguments(pipeline_arguments):
    global __pipeline_arguments
    if __pipeline_arguments is None:
        __pipeline_arguments = pipeline_arguments
    return __pipeline_arguments


def get_pipeline_director():
    global __pipeline_director
    if __pipeline_director is None:
        __pipeline_director = TrackhubPublisher(config_manager.read_config_from_file(__configuration_file),
                                                        __configuration_file,
                                                        __pipeline_arguments)
    return __pipeline_director


# Pipeline Configuration Manager
class ConfigManager(DirectorConfigurationManager):
    # Command Line Arguments for this pipeline look like
    #   # This is a JSON formatted file that contains all the relevant information needed for publishing the trackhub
    #   trackhub_description=input_file.json

    # Command Line Argument keys
    _CONFIG_COMMAND_LINE_ARGUMENT_KEY_TRACKHUB_DESCRIPTOR_FILE = 'trackhub_description'

    def __init__(self, configuration_object, configuration_file, pipeline_arguments):
        super().__init__(configuration_object, configuration_file, pipeline_arguments)
        # Lazy Process command line arguments
        self.__pipeline_arguments_object = None
        self.__running_mode = None

    def _get_allowed_configuration_keys(self):
        return {self._CONFIG_COMMAND_LINE_ARGUMENT_KEY_TRACKHUB_DESCRIPTOR_FILE}

    def get_trackhub_descriptor_file_path(self):
        return self._get_value_for_pipeline_argument_key(
            self._CONFIG_COMMAND_LINE_ARGUMENT_KEY_TRACKHUB_DESCRIPTOR_FILE)

    def get_file_path_pipeline_report(self):
        return os.path.join(config_manager.get_app_config_manager().get_session_working_dir(),
                            "pipeline-publish_trackhub.report")


class PipelineData:
    """
    This class models the data used by the pipeline, and given as input of it in the command line parameter
    """
    # Keys
    _PIPELINE_DATA_KEY_TRACKHUB_URL = 'trackhubUrl'
    _PIPELINE_DATA_KEY_TRACKHUB_PUBLIC = 'public'
    _PIPELINE_DATA_KEY_TRACKHUB_TYPE = 'type'
    _PIPELINE_DATA_KEY_PIPELINE_REPORT_FILE_PATH = 'pipelineReportFilePath'

    def __init__(self, pipeline_data_file_path):
        self.__pipeline_data_file_path = pipeline_data_file_path
        self.__pipeline_data_object = None

    def _get_pipeline_data_object(self):
        if not self.__pipeline_data_object:
            self.__pipeline_data_object = json.load(self.__pipeline_data_file_path)
        return self.__pipeline_data_object

    def _get_value_for_key(self, key, default=""):
        # TODO - I should start thinking about refactoring this out
        if key in self._get_pipeline_data_object():
            return self._get_pipeline_data_object()[key]
        return default

    def get_trackhub_url(self):
        return self._get_value_for_key(self._PIPELINE_DATA_KEY_TRACKHUB_URL)

    def get_trackhub_public_flag_value(self):
        return self._get_value_for_key(self._PIPELINE_DATA_KEY_TRACKHUB_URL, default='0')

    def get_trackhub_type(self):
        return self._get_value_for_key(self._PIPELINE_DATA_KEY_TRACKHUB_URL, default='PROTEOMICS')


class PipelineResult:
    """
    This class models the pipeline report that will be made available at the end of the pipeline execution
    """
    _VALUE_STATUS_SUCCESS = 'SUCCESS'
    _VALUE_STATUS_ERROR = 'ERROR'
    _VALUE_STATUS_WARNING = 'WARNING'

    def __init__(self):
        self.status = self._VALUE_STATUS_SUCCESS
        self.error_messages = []
        self.success_messages = []
        self.warning_messages = []
        self.trackhub_url = ""
        # Absolute file path to the folder that represents the running session of the pipeline
        self.file_path_pipeline_session = ""
        # Absolute file path to the log files that belong to the running session of the pipeline
        self.file_path_log_files = []

    def set_status_error(self):
        self.status = self._VALUE_STATUS_ERROR

    def add_error_message(self, error_message):
        """
        Adds an error message to the pipeline report. As this report is the final word on how the pipeline performed,
        the first error message that is set will set the status of the pipeline as 'failed'
        :param error_message: error message
        :return: no return value
        """
        # This is the report on the final result from running the pipeline
        self.set_status_error()
        self.error_messages.append(error_message)

    def add_success_message(self, success_message):
        """
        This will add messages to the pipeline report, but it doesn't change its status.
        :param success_message: message to add
        :return: no return value
        """
        self.success_messages.append(success_message)

    def add_warning_message(self, warning_message):
        """
        This will add warning messages to the pipeline report, setting the status to 'WARNING' if it wasn't in 'ERROR'
        status.
        :param warning_message: warning message to add
        :return: no return value
        """
        self.warning_messages.append(warning_message)
        if self.status != self._VALUE_STATUS_ERROR:
            self.status = self._VALUE_STATUS_WARNING

    def add_log_files(self, log_files):
        """
        Add all the log files produce by the pipeline to its final report
        :param log_files: a list of log files to add
        :return: no return value
        """
        self.file_path_log_files.extend(log_files)

    def __str__(self):
        return json.dumps({'status': self.status,
                           'success_messages': self.success_messages,
                           'warning_messages': self.warning_messages,
                           'error_messages': self.error_messages,
                           'trackhub_url': self.trackhub_url,
                           'pipeline_session_working_dir': self.file_path_pipeline_session,
                           'log_files': self.file_path_log_files})


# Pipeline Director
class TrackhubPublisher(Director):
    """
    Given input data regarding trackhub details, this pipeline will publish that trackhub
    """
    def __init__(self, configuration_object, configuration_file, pipeline_arguments):
        runner_id = "{}-{}".format(__name__, time.time())
        super().__init__(runner_id)
        self.__config_manager = ConfigManager(configuration_object, configuration_file, pipeline_arguments)
        self.__pipeline_data_object = PipelineData(self.__config_manager.get_trackhub_descriptor_file_path())
        # Pipeline result object
        self.__pipeline_result_object = PipelineResult()
        self.__trackhub_descriptor = None

    def _after(self):
        """
        Dump to a file the pipeline report
        :return: no return value
        """
        if not self.is_pipeline_status_ok():
            self._get_logger().warning("This Pipeline is finishing with NON-OK status.")
        report_files = [self.__config_manager.get_file_path_pipeline_report()]
        if self.__ \
                and self.__project_trackhub_descriptor.get_trackhub_report_file_path():
            report_files.append(self.__project_trackhub_descriptor.get_trackhub_report_file_path())
        for report_file in report_files:
            self._get_logger().info("Dumping Pipeline Report to '{}'".format(report_file))
            with open(report_file, 'w') as f:
                f.write(str(self.__pipeline_result_object))
        return True


