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

# App imports
import ensembl.service
from . import models as trackhub_models


# Registry request body model
class TrackhubRegistryequestBodyModel():
    def __init__(self):
        # hub.txt URL
        self.url = None
        self.assembly_accession_map = {}


# Visitor to export the trackhub as an instance of TrackhubRegistryRequestBodyModel
class TrackhubRegistryRequestBodyModelExporter(trackhub_models.TrackHubExporter):
    def __init__(self):
        super().__init__()

    def export_simple_trackhub(self, track_hub_builder):
        # In this case, the export summary will be an instance of TrackhubRegistryRequestBodyModelExporter
        if not self.export_summary:
            self.export_summary = TrackhubRegistryequestBodyModel()
        return self.export_summary


class TrackhubRegistryService:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.trackhub_registry_base_url = 'https://www.trackhubregistry.org'

    def publish_trackhub(self, hub_url, trackhub_registry_model):
        # TODO
        pass


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
