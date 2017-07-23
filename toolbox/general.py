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
import shutil
import subprocess
# Application modules
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
        if not os.path.exists(folder):
            try:
                os.mkdir(folder)
            except Exception as e:
                raise ToolBoxException(str(e))
        else:
            if not os.path.isdir(folder):
                raise ToolBoxException("'{}' is not a folder".format(folder))


def check_create_folders_overwrite(folders):
    """
    Given a list of folders, this method will create them, overwriting them in case they exist
    :param folders: list of folders to create
    :return: no return value
    :except: if any element in the list of folders is not a folder, an exception will be raised
    """
    invalid_folders = []
    for folder in folders:
        if os.path.exists(folder):
            if not os.path.isdir(folder):
                invalid_folders.append(folder)
    if invalid_folders:
        raise ToolBoxException("The following folders ARE NOT FOLDERS - '{}'"
                               .format(invalid_folders))
    for folder in folders:
        shutil.rmtree(folder)
    check_create_folders(folders)


def create_latest_symlink(destination_path):
    """
    Create a symlink 'latest' to the given destination_path in its parent folder, i.e. if the given path is
    '/nfs/production/folder', the symlink will be
            /nfs/production/latest -> /nfs/production/folder
    :param destination_path: destination path where the symlink will point to
    :return: no return value
    """
    symlink_path = os.path.join(os.path.dirname(destination_path), 'latest')
    os.symlink(destination_path, symlink_path)


def gunzip_files(files):
    """
    Given a list of paths for Gzip compressed files, this method will uncompress them, returning a list with the files
    that could not be gunzipped and the reason why that happened
    :param files: list of paths to files that will be un-compressed
    :return: a list of possible failing to uncompress files
    """
    gunzip_command_template = "gunzip {}"
    files_with_error = []
    for file in files:
        if os.path.isfile(file):
            try:
                gunzip_subprocess = subprocess.Popen(gunzip_command_template.format(file),
                                                     stdout=subprocess.PIPE,
                                                     stderr=subprocess.PIPE,
                                                     shell=True)
                # Timeout, in seconds, is either 10 seconds or the size of the file in MB * 10, e.g. 1MB -> 10 seconds
                file_size_mb = os.path.getsize(file) / (1024 * 1024)
                timeout = max(10, int(file_size_mb))
                (stdout, stderr) = gunzip_subprocess.communicate(timeout=timeout)
                if gunzip_subprocess.poll() is not None:
                    if gunzip_subprocess.returncode != 0:
                        # ERROR - Report this
                        err_msg = "ERROR uncompressing file '{}' output from subprocess STDOUT: {}\nSTDERR: {}"\
                            .format(file, stdout.decode('utf8'), stderr.decode('utf8'))
                        files_with_error.append((file, err_msg))
            except subprocess.TimeoutExpired as e:
                err_msg = "TIMEOUT ERROR uncompressing file '{}', size {}MB, given timeframe of '{}seconds', output from subprocess STDOUT: {}\nSTDERR: {}" \
                    .format(file_size_mb,
                            timeout,
                            file,
                            stdout.decode('utf8'),
                            stderr.decode('utf8'))
                files_with_error.append((file, err_msg))
            except Exception as e:
                err_msg = "UNKNOWN ERROR uncompressing file '{}' ---> {}\nOutput from subprocess STDOUT: {}\nSTDERR: {}" \
                    .format(file,
                            e,
                            stdout.decode('utf8'),
                            stderr.decode('utf8'))
                files_with_error.append((file, err_msg))
        else:
            files_with_error.append((file, "it IS NOT A FILE"))
    return files_with_error

if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
