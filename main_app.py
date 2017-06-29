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

import argparse
# Modules from package
import config_manager


def get_cmdl():
    cmdl_version = '2017.06.29'
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', "--config_file",
                        help='Application configuration file')
    parser.add_argument('-v', '--version',
                        help='display version information',
                        action='version',
                        version=cmdl_version + ' %(prog)s ')
    parser.add_argument('pipeline_name',
                        help='Module Name that contains the director of the pipeline to run')
    args = parser.parse_args()
    return args


def main():
    args = get_cmdl()
    if args.config_file:
        config_manager.set_application_config_file(args.config_file)
    if args.pipeline_name:
        config_manager.set_pipeline_name(args.pipeline_name)


if __name__ == "__main__":
    main()
