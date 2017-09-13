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


# Execution of commands
class CommandLineRunnerFactory:
    pass


class CommandLineRunner(metaclass=abc.ABCMeta, threading.Thread):
    def __init__(self):
        super().__init__()
        self.command = None
        self.timeout = None
        self._stdout = b' '
        self._stderr = b' '
        self.is_alive()

    def run(self):
        pass

    def cancel(self):
        pass
    
    def wait(self):
        pass

    def get_stdout(self):
        pass

    def get_stderr(self):
        pass


class CommandLineRunnerAsThread(CommandLineRunner):
    pass


class CommandLineRunnerOnHpc(CommandLineRunner):
    pass
