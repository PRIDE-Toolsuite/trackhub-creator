# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 28-06-2017 11:03
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This module implements some useful functions for the pipeline runner
"""

import os
import json
from exceptions import ToolBoxException


def read_json(json_file="json_file_not_specified.json"):
    """
    Reads a json file and it returns its object representation, no extra checks
    are performed on the file so, in case anything happens, the exception will
    reach the caller
    :param json_file: path to the file in json format to read
    :return: an object representation of the data in the json file
    """
    with open(json_file) as jf:
        return json.load(jf)


def check_create_folders(folders):
    """
    Check if folders exist, create them otherwise
    :param folders: list of folder paths to check
    :return: no return value
    """
    for folder in folders:
        if not os.path.isdir(folder):
            if os.path.exists(folder):
                raise ToolBoxException("'{}' is not a folder".format(folder))
            else:
                try:
                    os.mkdir(folder)
                except Exception as e:
                    raise ToolBoxException(str(e))


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not met to be run in stand alone mode")
