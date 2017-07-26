#!/usr/bin/env python3
#
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 29-06-2017 11:47
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Pipeline Runner - Main Application
"""

import nose
import argparse
import unittest
# Modules from package
import config_manager
import ensembl.service
import ensembl.data_downloader

__DEFAULT_CONFIG_FILE = "config_default.json"

# Running mode
__run_test_mode = False
__logger = None
__args = None


def get_cmdl():
    cmdl_version = '2017.06.29'
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', "--config_file",
                        help='Application configuration file')
    parser.add_argument('-p', '--pipeline_config_file',
                        help='Configuration file for the pipeline that is going to be run')
    parser.add_argument('-a', '--pipeline_arguments',
                        help='Comma separated of pipeline command line arguments (key=value pairs)')
    parser.add_argument('-v', '--version',
                        help='display version information',
                        action='version',
                        version=cmdl_version + ' %(prog)s ')
    parser.add_argument('pipeline_name',
                        help='Module Name that contains the director of the pipeline to run')
    args = parser.parse_args()
    return args


def app_bootstrap():
    global __run_test_mode
    global __logger
    global __args
    __args = get_cmdl()
    if __args.config_file:
        config_manager.set_application_config_file(__args.config_file)
    else:
        config_manager.set_application_config_file(__DEFAULT_CONFIG_FILE)
    if __args.pipeline_name:
        config_manager.set_pipeline_name(__args.pipeline_name)
        if __args.pipeline_name == 'test':
            __run_test_mode = True
    __logger = config_manager.get_app_config_manager().get_logger_for(__name__)
    if __run_test_mode:
        __logger.info(
            "Session '{}' STARTED, RUNNING UNIT TESTS".format(config_manager.get_app_config_manager().get_session_id()))
    else:
        __logger.info(
            "Session '{}' STARTED, pipeline '{}'".format(config_manager.get_app_config_manager().get_session_id(),
                                                         __args.pipeline_name))


def modules_bootstrap():
    ensembl_config_file = config_manager.get_app_config_manager().get_file_name_config_modules_ensembl_service()
    __logger.debug("Setting Ensembl configuration file -- {}".format(ensembl_config_file))
    ensembl.service.set_configuration_file(ensembl_config_file)
    # TODO - Should I delegate this to a main entry point for every module?.
    # TODO - REFACTOR THIS IN THE FUTURE, WHEN MODULE FUNCTIONALITY HAS BEEN TESTED
    __logger.debug("Setting Ensembl Data Downloader configuration file -- {}"
                   .format(config_manager
                           .get_app_config_manager()
                           .get_file_name_config_modules_ensembl_data_downloader()))
    ensembl.data_downloader.set_configuration_file(
        config_manager
            .get_app_config_manager()
            .get_file_name_config_modules_ensembl_data_downloader())


def run_unit_tests():
    __logger.debug("Running Unit Tests")
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('.')
    nose.run(suite=test_suite)


def run_pipeline():
    # TODO
    global __args
    pipeline_factory_module = config_manager\
        .get_app_config_manager()\
        .get_pipeline_factory_instance(__args.pipeline_name)
    # TODO I should refactor this in the future, in case I use this information anywhere else
    # Set the configuration file
    __logger.info("Pipeline configuration file '{}'".format(__args.pipeline_config_file))
    pipeline_factory_module.set_configuration_file(__args.pipeline_config_file)
    # Set the pipeline command line arguments
    __logger.info("Pipeline command line arguments: '{}'".format(__args.pipeline_arguments))
    pipeline_factory_module.set_pipeline_arguments(__args.pipeline_arguments)


def main():
    app_bootstrap()
    modules_bootstrap()
    if __run_test_mode:
        run_unit_tests()
    else:
        run_pipeline()


if __name__ == "__main__":
    main()
