# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 07-07-2017 11:39
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Download manager and its helper agents
"""


class Agent():
    def __init__(self, url, dst_folder, n_attemps=32, n_timeout_errors=3, download_timeout=120):
        self.__url = url
        self.__dst_folder = dst_folder
        self.__n_tries = n_attemps
        self.__n_timeout_errors = n_timeout_errors
        self.__download_timeout = download_timeout
        # Compute destination file name, using the same file name as in the given URL
        self.__dst_filename = url[url.rfind("/") + 1:]
        # Prepare standard output and error output
        self.__stdout = b' '
        self.__stderr = b' '
        # Result object
        self.__result = {'msg': '', 'success': True, 'url': str(self.__url)}

    def _build_result(self, msg, success=True):
        """
        Result object builder.

        The result object will contain anything that happened during the process of downloading a file from the given
        URL, and whether it was successful or not.
        :param msg: message to add to the final result object
        :param success: whether this extra informatoin makes the process successful or not
        :return: no value is returned
        """
        self.__result['msg'] = self.__result['msg'] + "\n" + msg
        self.__result['success'] = self.__result['success'] and success

    def run(self):
        pass

    def cancel(self):
        pass

    def wait(self):
        pass

    def get_result(self):
        pass


class Manager:
    def __init__(self, urls, dst_folder, logger, n_tries=32, n_timeouts=3, download_timeout=120):
        self.__urls = urls
        self.__dst_folder = dst_folder
        self.__logger = logger
        self.__n_tries = n_tries
        self.__n_timeouts = n_timeouts
        self.__download_timeout = download_timeout
        self.__agents = {}
        self.__success = True

    def start_downloads(self):
        # TODO
        pass

    def wait_all(self):
        # TODO
        pass

    def is_success(self):
        return self.__success
