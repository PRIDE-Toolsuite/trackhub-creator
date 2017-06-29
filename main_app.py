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


def get_cmdl():
    cmdl_version = '2017.06.29'
    parser = argparse.ArgumentParser(conflict_handler='resolve')
    parser.add_argument('-c', "--config_file_name",
                        metavar='config_file',
                        help='Application configuration file',
                        type=str)
    parser.add_argument('-v', '--version',
                        help='display version information',
                        action='version',
                        version=cmdl_version + ' %(prog)s ')
    parser.add_argument('workflow_name',
                        metavar='pipeline_name',
                        help='Module Name that contains the director of the pipeline to run',
                        type=str)
    args = parser.parse_args()
    return args


def main():
    args = get_cmdl()

if __name__ == "__main__":
    main()
