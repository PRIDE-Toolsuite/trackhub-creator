#!/usr/bin/env bash

# This script contains helper functions for the pipeline runner
#
# Manuel Bernal Llinares <mbdebian@gmail.com>

# Commands
DATE=$(which date)

# Simple logger
function logger() {
    echo -e "[$($DATE +%G%m%d_%H.%M)] $@"
}