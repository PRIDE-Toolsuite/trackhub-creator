#!/usr/bin/env bash

# This script contains helper functions for the pipeline runner
#
# Manuel Bernal Llinares <mbdebian@gmail.com>

# Simple logger
function logger() {
    echo -e "[$($DATE +%G%m%d_%H.%M)] $@"
}