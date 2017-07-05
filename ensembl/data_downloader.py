# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 03-07-2017 10:38
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This module implements en Ensembl data grabber for a given Ensembl Service instance.

Some of the use cases for this module:
    1. Given a species ID, download its protein sequence data, with the option of decompressing it or not.
    2. Given a species ID, collect its GTF data, with the option of decompressing it or not.
"""

# App imports
import os
import config_manager
from exceptions import ConfigManagerException
from ensembl.service import Service as EnsemblService

# Common configuration for all instances of the download manager
__configuration_file = None
__data_download_service = None


def set_configuration_file(config_file):
    global __configuration_file
    if __configuration_file is None:
        __configuration_file = config_file
    return __configuration_file


def get_data_download_service():
    global __data_download_service
    if __data_download_service is None:
        __data_download_service = DataDownloadService(config_manager.read_config_from_file(__configuration_file),
                                                      __configuration_file)
    return __data_download_service


# Ensembl Data Grabbing Service configuration manager
class ConfigurationManager(config_manager.ConfigurationManager):
    # Configuration keys
    _CONFIG_KEY_DATA_DOWNLOADER = 'data_downloader'
    _CONFIG_KEY_ENSEMBL_FTP = 'ensembl_ftp'
    _CONFIG_KEY_BASE_URL = 'base_url'
    _CONFIG_KEY_FOLDER_PREFIX_RELEASE = 'folder_prefix_release'
    _CONFIG_KEY_FOLDER_NAME_FASTA = 'folder_name_fasta'
    _CONFIG_KEY_FOLDER_NAME_PROTEIN_SEQUENCES = 'folder_name_protein_sequences'
    _CONFIG_KEY_FOLDER_NAME_GTF = 'folder_name_gtf'

    def __init__(self, configuration_object, configuration_file):
        super(ConfigurationManager, self).__init__(configuration_object, configuration_file)
        self.__logger = config_manager.get_app_config_manager().get_logger_for(__name__)
        # Local Ensembl repo parent folder name
        self.__local_folder_ensembl_repo = 'ensembl'

    def _get_logger(self):
        return self.__logger

    def get_local_path_folder_ensembl_repo(self):
        """
        Get the absolute path to the local folder where we are going to store all the data from the different releases
        of Ensembl
        :return: absolute path of the local repository for Ensembl releases data
        """
        return os.path.abspath(os.path.join(config_manager.get_app_config_manager().get_folder_resources(),
                                            self.__local_folder_ensembl_repo))

    def get_ensembl_ftp_base_url(self):
        """
        Get the base URL for Ensembl FTP service, e.g. ftp://ftp.ensembl.org/pub/ .
        This parameter is defined in the configuration file used in the pipeline session for the Ensembl module.
        :return: a string with the configured Ensembl FTP base URL
        """
        try:
            return self._get_configuration_object() \
                [self._CONFIG_KEY_DATA_DOWNLOADER] \
                [self._CONFIG_KEY_ENSEMBL_FTP] \
                [self._CONFIG_KEY_BASE_URL]
        except Exception as e:
            raise ConfigManagerException(
                "MISSING configuration information '{}.{}.{}' in configuration file '{}', because of '{}'".format(
                    self._CONFIG_KEY_DATA_DOWNLOADER,
                    self._CONFIG_KEY_ENSEMBL_FTP,
                    self._CONFIG_KEY_BASE_URL,
                    self._get_configuration_file(),
                    str(e)))

    def get_folder_prefix_ensembl_release(self):
        try:
            return self._get_configuration_object() \
                [self._CONFIG_KEY_DATA_DOWNLOADER] \
                [self._CONFIG_KEY_ENSEMBL_FTP] \
                [self._CONFIG_KEY_FOLDER_PREFIX_RELEASE]
        except Exception as e:
            raise ConfigManagerException(
                "MISSING configuration information '{}.{}.{}' in configuration file '{}', because of '{}'".format(
                    self._CONFIG_KEY_DATA_DOWNLOADER,
                    self._CONFIG_KEY_ENSEMBL_FTP,
                    self._CONFIG_KEY_FOLDER_PREFIX_RELEASE,
                    self._get_configuration_file(),
                    str(e)))

    def get_folder_name_fasta(self):
        try:
            return self._get_configuration_object() \
                [self._CONFIG_KEY_DATA_DOWNLOADER] \
                [self._CONFIG_KEY_ENSEMBL_FTP] \
                [self._CONFIG_KEY_FOLDER_NAME_FASTA]
        except Exception as e:
            raise ConfigManagerException(
                "MISSING configuration information '{}.{}.{}' in configuration file '{}', becuase of '{}'".format(
                    self._CONFIG_KEY_DATA_DOWNLOADER,
                    self._CONFIG_KEY_ENSEMBL_FTP,
                    self._CONFIG_KEY_FOLDER_NAME_FASTA,
                    self._get_configuration_file(),
                    str(e)))

    def get_folder_name_protein_sequences(self):
        try:
            return self._get_configuration_object() \
                [self._CONFIG_KEY_DATA_DOWNLOADER] \
                [self._CONFIG_KEY_ENSEMBL_FTP] \
                [self._CONFIG_KEY_FOLDER_NAME_PROTEIN_SEQUENCES]
        except Exception as e:
            raise ConfigManagerException(
                "MISSING configuration information '{}.{}.{}' in configuration file '{}', becuase of '{}'".format(
                    self._CONFIG_KEY_DATA_DOWNLOADER,
                    self._CONFIG_KEY_ENSEMBL_FTP,
                    self._CONFIG_KEY_FOLDER_NAME_PROTEIN_SEQUENCES,
                    self._get_configuration_file(),
                    str(e)))


class DataDownloadService:
    """
    This Service is in charge of grabbing data (download) from Ensembl to a local repository
    """

    def __init__(self, configuration_object, configuration_file):
        self.__logger = config_manager.get_app_config_manager().get_logger_for(__name__)
        self._get_logger().debug("Using configuration file '{}'".format(configuration_file))
        self.__config_manager = ConfigurationManager(configuration_object, configuration_file)
        # Name for the current release folder, we'll use the same for both the FTP and the local storage
        self.__folder_name_release = None
        # Name for the subfolder that contains per species fasta files
        self.__folder_name_fasta = None
        # Name for the subfolder of species folder that contains protein sequences files
        self.__folder_name_protein_sequences = None

    def __prepare_local_ensembl_repository(self):
        # TODO
        pass

    def _get_logger(self):
        return self.__logger

    def _get_ensembl_service(self):
        # TODO
        pass


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
