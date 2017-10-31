#!/usr/bin/env bash

# Publish a trackhub described by the given json formatted input file
#   usage: launcher.sh <trackhub_registry_url> <trackhub_registry_username> <trackhub_registry_password> <trackhub_description_data.json>
#
# Manuel Bernal Llinares <mbdebian@gmail.com>

# Include helpers
source scripts/commons/helper_functions.sh

# Commands
PWD=$(which pwd)

