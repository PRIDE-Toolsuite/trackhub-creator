#!/usr/bin/env bash

# This script contains helper functions for the pipeline runner
#
# Manuel Bernal Llinares <mbdebian@gmail.com>

# Simple logger
function log() {
    echo -e "[$($DATE +%G%m%d_%H.%M)] $@"
}