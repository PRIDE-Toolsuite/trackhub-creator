# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 12-09-2017 16:10
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This file contains different models for the execution of subprocesses / external processes, e.g. via the command line
"""

import abc
import threading
# App imports
import config_manager


# Execution of commands
class CommandLineRunnerFactory:
    pass


class ParallelManager:
    pass


class ParallelRunner(metaclass=abc.ABCMeta, threading.Thread):
    def __init__(self):
        super().__init__()
        self._logger = config_manager \
            .get_app_config_manager() \
            .get_logger_for("{}.{}".format(__name__, type(self).__name__))
        self.command = None
        self.timeout = None
        self._stdout = b' '
        self._stderr = b' '
        self._done = False
        self._shutdown = False

    @abc.abstractmethod
    def _run(self):
        ...

    def run(self):
        self._logger.debug("Parallel Runner ID '{}' --- START ---".format(threading.current_thread().getName()))
        self._run()

    def cancel(self):
        self._logger.debug("Parallel Runner ID '{}' --- CANCEL ---".format(threading.current_thread().getName()))
        self._shutdown = True
        self._stop()

    def wait(self):
        self._logger.debug("Parallel Runner ID '{}' --- WAIT ---".format(threading.current_thread().getName()))
        self.join()

    def get_stdout(self):
        pass

    def get_stderr(self):
        pass


class CommandLineRunner(ParallelRunner):
    pass


class CommandLineRunnerAsThread(CommandLineRunner):
    pass


class CommandLineRunnerOnHpc(CommandLineRunner):
    pass
