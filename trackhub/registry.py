# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 23-08-2017 14:40
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This module models the trackhub registry
"""


class TrackhubRegistryService:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.trackhub_registry_base_url = 'https://www.trackhubregistry.org'

    def publish_trackhub(self):
        # TODO
        pass
