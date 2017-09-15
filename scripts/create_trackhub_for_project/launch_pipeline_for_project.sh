#!/usr/bin/env bash

# Create Trackhub for PRIDE Project pipeline launcher
#   usage: launcher.sh <project_description_data.json>
#
# Manuel Bernal Llinares <mbdebian@gmail.com>

# Include helpers
source scripts/commons/helper_functions.sh

# Logging with prefix
function mylogger() {
    logger "[Trackhub] $@"
}

# Command line parameters
PROJECT_DESCRIPTION_DATA_FILE=$1