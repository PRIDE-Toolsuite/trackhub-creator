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

import time
import random
import threading
import subprocess


class Agent(threading.Thread):
    def __init__(self, url, dst_folder, download_attempts=32, timeout_attempts=3, download_timeout=600):
        super(Agent, self).__init__()
        self.__download_url = url
        self.__dst_folder = dst_folder
        self.__download_attempts = download_attempts
        self.__timeout_attempts = timeout_attempts
        self.__download_timeout = download_timeout
        # Compute destination file name, using the same file name as in the given URL
        self.__dst_filename = url[url.rfind("/") + 1:]
        # Prepare standard output and error output
        self.__stdout = b' '
        self.__stderr = b' '
        # Result object
        self.__result = {'msg': '', 'success': True, 'url': str(self.__download_url)}
        # Seed random module
        random.seed(time.time())
        # We have everything we need, auto-start the thread
        self.start()

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

    def __download_with_timeout(self):
        """
        This is a helper method that will download the given URL setting a timeout limit.
        :return: True if success
        :except: a subprocess.TimeoutExpired exception is raised if the download can't be completed within the given
        temporal constraints
        """
        download_command = "cd " + str(self.get_dst_folder()) + "; curl -L -O -C - " + str(self.get_download_url())
        download_subprocess = subprocess.Popen(download_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                               shell=True)
        stdout = b' '
        stderr = b' '
        try:
            self._build_result("Downloading '{}' with timeout set to {} seconds"
                               .format(self.get_download_url(),
                                       self.get_download_timeout()))
            (stdout, stderr) = download_subprocess.communicate(timeout=self.get_download_timeout())
        except subprocess.TimeoutExpired as exception_download_timeout:
            self._build_result("Timeout ({} seconds) ERROR downloading '{}', STDOUT: |||> {} <|||, STDERR XXX> {} <XXX"
                               .format(self.get_download_timeout(),
                                       self.get_download_url(),
                                       stdout.decode('utf8'),
                                       stderr.decode('utf8')))
            raise
        # Let's check the result from downloading the file
        if download_subprocess.poll() is not None:
            if download_subprocess.returncode != 0:
                # ERROR
                self._build_result("ERROR downloading '{}', STDOUT: |||> {} <|||, STDERR XXX> {} <XXX"
                                   .format(self.get_download_timeout(),
                                           self.get_download_url(),
                                           stdout.decode('utf8'),
                                           stderr.decode('utf8')))
                return False
            # SUCCESS
            self._build_result("SUCCESSFUL download for '{}', STDOUT: |||> {} <|||, STDERR XXX> {} <XXX"
                               .format(self.get_download_timeout(),
                                       self.get_download_url(),
                                       stdout.decode('utf8'),
                                       stderr.decode('utf8')))
        else:
            # TODO
            # The child process is still running, and this is weird stuff because we are using a timeout parameter, we
            # should never reach this part of the code
            self._build_result("WEIRD DOWNLOAD - THE SUBPROCESS IS STILL RUNNING FOR '{}' DESPITE THE TIME OUT "
                               "PARAMETER, STDOUT: |||> {} <|||, STDERR XXX> {} <XXX"
                               .format(self.get_download_timeout(),
                                       self.get_download_url(),
                                       stdout.decode('utf8'),
                                       stderr.decode('utf8')))
            download_subprocess.kill()
            return False
        return True

    def __download_with_timeout_attempts(self):
        """
        Download the given URL given a time constraint with a limited number of attempts upon timeout errors.
        :return: True if success, False if we reached the maximum number of attempts
        """
        timeout_attempt_counter = 0
        while timeout_attempt_counter < self.get_timeout_attempts():
            self._build_result("Downloading '{}', timeout attempt #{} out of #{}"
                               .format(self.get_download_url(),
                                       timeout_attempt_counter,
                                       self.get_timeout_attempts()))
            timeout_attempt_counter += 1
            try:
                return self.__download_with_timeout()
            except subprocess.TimeoutExpired as exception_download_timeout:
                self._build_result("Download of '{}' TIMED OUT, timeout attempt #{} out of #{}"
                                   .format(self.get_download_url(),
                                           timeout_attempt_counter,
                                           self.get_timeout_attempts()))
                # wait for a random amount of time before retrying the download
                # WARNING! - MAGIC NUMBER AHEAD!!!
                time.sleep(random.randint(0, 60))
        return False

    def run(self):
        """
        This is the main thread for the download agent
        :return: no value is returned
        """
        # TODO - Validate URL
        attempt_counter = 0
        download_completion = False
        while attempt_counter < self.get_download_attempts():
            attempt_counter += 1
            self._build_result("Downloading '{}', download attempt #{} out of #{}"
                               .format(self.get_download_url(),
                                       attempt_counter,
                                       self.get_download_attempts()))
            try:
                download_completion = self.__download_with_timeout_attempts()
                if download_completion:
                    # Quit as soon as we succeed on downloading the file
                    break
            except Exception as e:
                self._build_result("ERROR downloading '{}', on download attempt #{} out of #{}, ERROR: {}"
                                   .format(self.get_download_url(),
                                           attempt_counter,
                                           self.get_download_attempts(),
                                           str(e)))
        if download_completion:
            self._build_result("Download for '{}' COMPLETED, on download attempt #{} out of #{}"
                               .format(self.get_download_url(),
                                       attempt_counter,
                                       self.get_download_attempts()),
                               True)
        else:
            self._build_result("Download for '{}' FAILED, on download attempt #{} out of #{}"
                               .format(self.get_download_url(),
                                       attempt_counter,
                                       self.get_download_attempts()),
                               False)

    def cancel(self):
        """
        I think this is the way to stop the thread, but I'm not sure, because the documentation about it is a little bit
        tricky, or I didn't find the right documentation.
        :return: no value is returned
        """
        self.alive = False
        self.join()

    def wait(self):
        """
        Wait for this thread to finish its job (download a file), and get the result object.
        :return: result object with information on the finished download process
        """
        self.join()
        return self.get_result()

    def get_result(self):
        """
        Get the result object built by this Agent.

        This method should be called when the agent finishes its job, but not in the middle of it.
        :return: result object with information on the finished download process
        """
        return self.__result

    def get_dst_folder(self):
        return self.__dst_folder

    def get_download_timeout(self):
        return self.__download_timeout

    def get_download_url(self):
        return self.__download_url

    def get_timeout_attempts(self):
        return self.__timeout_attempts

    def get_download_attempts(self):
        return self.__download_attempts


class Manager:
    def __init__(self, urls, download_destination_folder, logger, download_attempts=32, timeout_attempts=3,
                 download_timeout=120):
        self.__urls = urls
        self.__download_destination_folder = download_destination_folder
        self.__logger = logger
        self.__download_attempts = download_attempts
        self.__timeout_attempts = timeout_attempts
        self.__download_timeout = download_timeout
        self.__agents = {}
        self.__success = True

    def __add_agent_for_url(self, url, agent):
        self.__agents[url] = agent

    def __get_count_of_running_agents(self):
        return len(self.__agents)

    def __get_agent_entries(self):
        return [(url, self.__agents[url]) for url in self.__agents]

    def __set_success(self):
        self.__success = self.__success and True
        return self.__success

    def __set_fail(self):
        self.__success = self.__success and False
        return self.__success

    def _get_logger(self):
        return self.__logger

    def start_downloads(self):
        for url in self.get_urls_to_download():
            self._get_logger().debug("Launching download agent for URL '{}'".format(url))
            self.__add_agent_for_url(url,
                                     Agent(url,
                                           self.get_download_destination_folder(),
                                           download_attempts=self.get_download_attempts(),
                                           timeout_attempts=self.get_timeout_attempts(),
                                           download_timeout=self.get_download_timeout()))

    def wait_all(self):
        self._get_logger().debug("Waiting for #{} download agents to finish"
                                 .format(self.__get_count_of_running_agents()))
        for (url, agent) in self.__get_agent_entries():
            self._get_logger().debug("Checking on Download Agent for '{}'".format(url))
            result = agent.wait()
            if result['success']:
                self._get_logger().debug(result['msg'])
                self.__set_success()
            else:
                self._get_logger().error(result['msg'])
                self.__set_fail()
        self.__set_success()

    def is_success(self):
        return self.__success

    def get_urls_to_download(self):
        return self.__urls

    def get_download_destination_folder(self):
        return self.__download_destination_folder

    def get_download_attempts(self):
        return self.__download_attempts

    def get_timeout_attempts(self):
        return self.__timeout_attempts

    def get_download_timeout(self):
        return self.__download_timeout


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")


