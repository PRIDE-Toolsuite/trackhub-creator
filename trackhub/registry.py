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

import json
import time
import requests
# App imports
import config_manager
import ensembl.service
from . import models as trackhub_models
from . import exceptions as trackhub_exceptions


# Registry request body model
class TrackhubRegistryRequestBodyModel:
    """
    This class models the payload used to register a trackub at http://trackhubregistry.org
    """
    def __init__(self):
        self.logger = config_manager.get_app_config_manager().get_logger_for(
            "{}.{}".format(__name__, type(self).__name__))
        # hub.txt URL
        self.url = None
        self.assembly_accession_map = {}
        # Trackhub is public by default
        self.public = '1'
        # Default type for trackhubs is PROTEOMICS
        self.type = 'PROTEOMICS'

    def add_accession_for_assembly(self, assembly, accession):
        if assembly in self.assembly_accession_map:
            self.logger.error(
                "DUPLICATED Assembly '{}' add request, existing accession '{}', "
                "accession requested to be added '{}' - SKIPPED".format(assembly, self.assembly_accession_map[assembly],
                                                                        accession))
        else:
            self.assembly_accession_map[assembly] = accession
            self.logger.info("Assembly '{}' entry added to request body with accession '{}'"
                             .format(assembly, accession))

    def as_payload_object(self):
        return {'url': self.url,
                'public': self.public,
                'type': self.type}
        # TODO - Refactor this once the testing with trackhubregistry.org is done and verified
        # ,'assemblies': self.assembly_accession_map}

    def __str__(self):
        return json.dumps({'url': self.url,
                           'public': self.public,
                           'type': self.type,
                           'assemblies': self.assembly_accession_map})


# Visitor to export the trackhub as an instance of TrackhubRegistryRequestBodyModel
class TrackhubRegistryRequestBodyModelExporter(trackhub_models.TrackHubExporter):
    """
    This visitor of trackhub builders will create a TrackhubRegistryRequestBodyModel as a product from the information
    present in the builder
    """
    def __init__(self):
        super().__init__()

    def export_simple_trackhub(self, trackhub_builder):
        # In this case, the export summary will be an instance of TrackhubRegistryRequestBodyModelExporter
        if not self.export_summary:
            self.export_summary = TrackhubRegistryRequestBodyModel()
            ensembl_species_service = ensembl.service.get_service().get_species_data_service()
            for assembly in trackhub_builder.assemblies:
                self.export_summary \
                    .add_accession_for_assembly(assembly,
                                                ensembl_species_service
                                                .get_species_entry_for_assembly(assembly)
                                                .get_assembly_accession())
        return self.export_summary


class TrackhubRegistryService:
    """
    This class models a wrapper for the trackhubregistry.org service API,
    as specified at https://www.trackhubregistry.org/docs/management/overview
    """
    __TRACKHUB_REGISTRY_API_SUBPATH_LOGIN = '/api/login'
    __TRACKHUB_REGISTRY_API_SUBPATH_LOGOUT = '/api/logout'
    __TRACKHUB_REGISTRY_API_SUBPATH_TRACKHUB = '/api/trackhub'

    def __init__(self, username, password):
        self.logger = config_manager.get_app_config_manager().get_logger_for("{}.{}"
                                                                             .format(__name__, type(self).__name__))
        self.username = username
        self.password = password
        self.trackhub_registry_base_url = 'https://www.trackhubregistry.org'
        self.__auth_token = None

    def __login(self):
        if not self.__auth_token:
            response = requests.get("{}{}"
                                    .format(self.trackhub_registry_base_url,
                                            self.__TRACKHUB_REGISTRY_API_SUBPATH_LOGIN),
                                    auth=(self.username, self.password),
                                    verify=True)
            if not response.ok:
                raise trackhub_exceptions.TrackhubRegistryServiceException(
                    "LOGIN ERROR '{}', HTTP status '{}'".format(response.text, response.status_code))
            self.__auth_token = response.json()[u'auth_token']
            self.logger.info("LOGGED IN at '{}'".format(self.trackhub_registry_base_url))
        return self.__auth_token

    def __logout(self):
        if self.__auth_token:
            response = requests.get("{}{}"
                                    .format(self.trackhub_registry_base_url,
                                            self.__TRACKHUB_REGISTRY_API_SUBPATH_LOGOUT),
                                    headers={'user': self.username, 'auth_token': self.__auth_token})
            if not response.ok:
                raise trackhub_exceptions.TrackhubRegistryServiceException(
                    "LOGOUT ERROR '{}', HTTP status '{}'".format(response.text, response.status_code))
            self.__auth_token = None
            self.logger.info("LOGGED OUT from '{}'".format(self.trackhub_registry_base_url))

    def __analyze_success_trackhub_registration(self, response):
        # TODO
        self.logger.debug("Trackhub Registration Response: '{}'".format(response.json()))
        return response.json()

    def register_trackhub(self, trackhub_registry_model):
        auth_token = self.__login()
        headers = {'user': self.username, 'auth_token': auth_token}
        payload = trackhub_registry_model.as_payload_object()
        api_register_endpoint = "{}{}".format(self.trackhub_registry_base_url,
                                              self.__TRACKHUB_REGISTRY_API_SUBPATH_TRACKHUB)
        self.logger.debug("REGISTER TRACKHUB, endpoint '{}', payload '{}'".format(api_register_endpoint, payload))
        try:
            # TODO - magic number here!!! OMG!!!
            try_counter = 10
            while try_counter:
                try_counter -= 1
                self.logger.error("<--- TRACKHUB REGISTRATION ATTEMPT (#{} attempts left) --->".format(try_counter))
                # Register Trackhub
                response = requests.post(api_register_endpoint,
                                         headers=headers, json=payload, verify=True)
                if response.ok:
                    self.logger.info("HOLY CRAP! Trackhub REGISTERED!, #{} attempts left".format(try_counter))
                    break
                if not response.ok and (not try_counter):
                    raise trackhub_exceptions.TrackhubRegistryServiceException(
                        "TRACKHUB REGISTRATION ERROR '{}', HTTP status '{}'"
                            .format(response.text, response.status_code))
                self.logger.error("<xxx FAILED ATTEMPT to Register Trackhub !!! xxx> HTTP Status '{}' - Response: '{}'"
                                  .format(response.status_code, response.text))
                # TODO - magic number here!!! OMG!!!
                time.sleep(10)
        finally:
            self.__logout()
        # Analyze response
        return self.__analyze_success_trackhub_registration(response)

    def register_update_trackhub(self, trackhub_registry_model):
        # TODO - I'm not sure I need these extra methods, as the API says on its documentation that registering an
        # TODO - existing owned trackhub, would update it
        raise NotImplementedError("This method is NOT SUPPORTED in this version of the application")

    def update_trackhub(self, trackhub_registry_model):
        # TODO
        raise NotImplementedError("This method is NOT SUPPORTED in this version of the application")

    def is_trackhub_already_registered(self, trackhub_registry_model):
        # TODO
        raise NotImplementedError("This method is NOT SUPPORTED in this version of the application")


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
