# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 13-09-2017 13:10
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Unit tests for the parallelization module
"""

import unittest
# App imports
import config_manager
from parallel.models import CommandLineRunnerFactory, ParallelRunnerManagerFactory


class TestCommandLineRunner(unittest.TestCase):
    __logger = config_manager.get_app_config_manager().get_logger_for(__name__)

    def test_success_on_running_simple_command_without_timeout(self):
        command = "echo Successful_run"
        runner = CommandLineRunnerFactory.get_command_line_runner()
        runner.command = command
        runner.start()
        runner.wait()
        self.assertTrue(runner.command_success, "Command finishes with success")
        self.__logger.debug("Command '{}', STDOUT - '{}', STDERR - '{}'"
                            .format(command,
                                    runner.get_stdout().decode('utf8'),
                                    runner.get_stderr().decode('utf8')))

    def test_simple_commands_with_parallel_runner_manager(self):
        commands = ["echo Successful_run-{:03}".format(i) for i in range(0, 16)]
        parallel_runner_manager = ParallelRunnerManagerFactory.get_parallel_runner_manager()
        for command in commands:
            runner = CommandLineRunnerFactory.get_command_line_runner()
            runner.command = command
            parallel_runner_manager.add_runner(runner)
        parallel_runner_manager.start_runners()
        parallel_runner_manager.wait_all()
        for runner in parallel_runner_manager.get_finished_runners():
            self.assertTrue(runner.is_done(), "Runner is Done")
            self.assertTrue(runner.command_success, "Run command was successful")


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
