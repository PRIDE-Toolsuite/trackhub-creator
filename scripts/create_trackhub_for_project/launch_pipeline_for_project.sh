#!/usr/bin/env bash

# Create Trackhub for PRIDE Project pipeline launcher
#   usage: launcher.sh <project_description_data.json>
#
# Manuel Bernal Llinares <mbdebian@gmail.com>

# Include helpers
source scripts/commons/helper_functions.sh

# Commands
PWD=$(which pwd)

# Logging with prefix
function mylogger() {
    logger "[Trackhub] $@"
}

# Command line parameters
PROJECT_DESCRIPTION_DATA_FILE=$1

mylogger "Starting trackhub export for PRIDE Project described at '${PROJECT_DESCRIPTION_DATA_FILE}'"
mylogger "Current directory is $($PWD)"
mylogger "<--- Running create_trackhub_for_project --->"
time python_install/bin/python ./main_app.py -a project_data_file=${PROJECT_DESCRIPTION_DATA_FILE} create_trackhub_for_project
