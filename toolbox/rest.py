# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 03-07-2017 13:36
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Toolbox related to REST services
"""

import requests


def make_rest_request_content_type_json(url):
    # TODO - Add multiple attempts with random timeouts
    # TODO - Magic number here!!!
    n_attempts = 10
    response = None
    while n_attempts:
        n_attempts -= 1
        response = requests.get(url, headers={"Content-Type": "application/json"})
        if response.ok:
            break
        # TODO - Random wait
    if not response.ok:
        response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
