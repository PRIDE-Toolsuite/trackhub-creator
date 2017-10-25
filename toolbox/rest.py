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

import time
import random
import requests

# Initialize pseudo-random number generator
random.seed(time.time())


def make_rest_request_content_type_json(url):
    # TODO - Magic number here!!!
    n_attempts = 10
    response = None
    while n_attempts:
        n_attempts -= 1
        try:
            response = requests.get(url, headers={"Content-Type": "application/json"})
        except Exception as e:
            # Any possible exception counts towards the attempt counter
            continue
        if response.ok:
            return response.json()
        # Random wait - TODO - Another magic number!!!
        time.sleep(random.randint(10))
    response.raise_for_status()


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
