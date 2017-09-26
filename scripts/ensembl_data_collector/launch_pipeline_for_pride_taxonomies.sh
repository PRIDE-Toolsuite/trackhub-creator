#!/usr/bin/env bash

# Collect data from the latest Ensembl Release, pipeline launcher
#   usage: launcher.sh <project_description_data.json>
#
# Manuel Bernal Llinares <mbdebian@gmail.com>

# Include helpers
source scripts/commons/helper_functions.sh

# Commands
PWD=$(which pwd)

# Logging with prefix
function mylogger() {
    logger "[Ensembl_Data_Collector] $@"
}

