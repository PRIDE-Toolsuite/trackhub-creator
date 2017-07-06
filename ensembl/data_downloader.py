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

import os
# App imports
import config_manager
import toolbox
import ensembl.service
from exceptions import ConfigManagerException

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
        __data_download_service.post_constructor()
    return __data_download_service


# Ensembl Data Grabbing Service configuration manager
class ConfigurationManager(config_manager.ConfigurationManager):
    # Configuration keys
    _CONFIG_KEY_DATA_DOWNLOADER = 'data_downloader'
    # Ensembl FTP section
    _CONFIG_KEY_ENSEMBL_FTP = 'ensembl_ftp'
    _CONFIG_KEY_BASE_URL = 'base_url'
    _CONFIG_KEY_FOLDER_PREFIX_RELEASE = 'folder_prefix_release'
    _CONFIG_KEY_FOLDER_NAME_FASTA = 'folder_name_fasta'
    _CONFIG_KEY_FOLDER_NAME_PROTEIN_SEQUENCES = 'folder_name_protein_sequences'
    _CONFIG_KEY_FOLDER_NAME_GTF = 'folder_name_gtf'
    # Rewrite option
    _CONFIG_KEY_REWRITE_LOCAL_PATH_ENSEMBL_REPO = 'rewrite_local_path_ensembl_repo'
    # Ensembl file names
    _CONFIG_KEY_ENSEMBL_FILE_NAMES = 'ensembl_file_names'
    _CONFIG_KEY_PROTEIN_SEQUENCE_FILE = 'protein_sequence_file'
    _CONFIG_KEY_FILE_TYPE = 'file_type'
    _CONFIG_KEY_SUFFIXES = 'suffixes'
    _CONFIG_KEY_FILE_EXTENSION = 'file_extension'

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
        """
        Get the prefix for the ensembl release folder, e.g. Ensembl has been making releases in folders like
        'release-89', so the prefix would be 'release-'.

        This parameter is specified in the configuration file that is used in the pipeline session for the Ensembl module.
        :return: a string with the prefix for ensembl release folder name
        """
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
        """
        Get the name for the folder that contains per-species fasta data, e.g. it is used to work out the path to access
        FASTA data for a given species on the Ensembl FTP service.

        This parameter is specified in the configuration file that is used in the pipeline session for the Ensembl
        module.
        :return: name of the folder as set in the configuration file
        """
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
        """
        Get the name for the sub-folder that contains protein sequence data for a particular species, e.g. it is used to
        work out the path to access protein sequence data for a given species.

        This parameter is specified in the configuration file that is used in the pipeline session for the Ensembl
        module.
        :return: name of the sub-folder as set in the configuration file
        """
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

    def get_folder_name_gtf(self):
        """
        Get the name for the sub-folder that contains GTF data for a particular species, e.g. it is used to work out the
        path to access GTF data for a given species, to download it from Ensembl.

        This parameter is specified in the configuration file that is used in the pipeline session for the Ensembl
        module.
        :return: name fo the sub-folder as set in the configuration file
        """
        try:
            return self._get_configuration_object() \
                [self._CONFIG_KEY_DATA_DOWNLOADER] \
                [self._CONFIG_KEY_ENSEMBL_FTP] \
                [self._CONFIG_KEY_FOLDER_NAME_GTF]
        except Exception as e:
            raise ConfigManagerException(
                "MISSING configuration information '{}.{}.{}' in configuration file '{}', becuase of '{}'".format(
                    self._CONFIG_KEY_DATA_DOWNLOADER,
                    self._CONFIG_KEY_ENSEMBL_FTP,
                    self._CONFIG_KEY_FOLDER_NAME_GTF,
                    self._get_configuration_file(),
                    str(e)))

    def is_rewrite_local_path_ensembl_repo(self):
        """
        Find out whether we are required to overwrite the local Ensembl repository or not, in case there is an existing
        one for the same release we are collecting data from.
        :return: True if we have to rewrite it, False otherwise
        """
        try:
            if self._get_configuration_object() \
                    [self._CONFIG_KEY_DATA_DOWNLOADER] \
                    [self._CONFIG_KEY_REWRITE_LOCAL_PATH_ENSEMBL_REPO] == "True":
                return True
            return False
        except Exception as e:
            raise ConfigManagerException(
                "MISSING configuration information '{}.{}' in configuration file '{}', becuase of '{}'".format(
                    self._CONFIG_KEY_DATA_DOWNLOADER,
                    self._CONFIG_KEY_REWRITE_LOCAL_PATH_ENSEMBL_REPO,
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
        self.__local_path_ensembl_repo = None
        self.__local_path_ensembl_release = None
        # Name for the current release
        self.__ensembl_release_name = None
        # Name for the subfolder that contains per species fasta files
        self.__folder_name_fasta = None
        # Name for the subfolder of species folder that contains protein sequences files
        self.__folder_name_protein_sequences = None

    def post_constructor(self):
        """
        This is an initialization method that should be called just after building an instance of this class
        :return: no return value
        """
        self.__prepare_local_ensembl_repository()

    def __prepare_local_ensembl_repository(self):
        self._get_logger().debug("Preparing local Ensembl repository, root folder - '{}'"
                                 .format(self.get_local_path_root_ensembl_repo()))
        toolbox.check_create_folders([self.get_local_path_root_ensembl_repo()])
        self._get_logger().debug("Local path for Ensembl Release - '{}'"
                                 .format(self.get_local_path_ensembl_release()))
        if self._get_configuration_manager().is_rewrite_local_path_ensembl_repo():
            self._get_logger().debug("Creating folder in 'OVERWRITE' mode - '{}'"
                                     .format(self.get_local_path_ensembl_release()))
            toolbox.check_create_folders_overwrite([self.get_local_path_ensembl_release()])
        else:
            self._get_logger().debug("Creating folder if it doesn't exist - '{}'"
                                     .format(self.get_local_path_ensembl_release()))
            toolbox.check_create_folders([self.get_local_path_ensembl_release()])
        toolbox.create_latest_symlink(self.get_local_path_ensembl_release())

    def __get_subpath_fasta_for_species(self, taxonomy_id):
        # The subpath is fasta/species.name
        return "{}/{}".format(self._get_configuration_manager().get_folder_name_fasta(),
                              self._get_ensembl_service()
                                 .get_species_data_service()
                                 .get_species_entry_for_taxonomy_id(taxonomy_id)
                                 .get_name())


    def __get_subpath_protein_sequence_for_species(self, taxonomy_id):
        # The subpath is fasta/species.name/pep
        return "{}/{}".format(self.__get_subpath_fasta_for_species(taxonomy_id),
                              self._get_configuration_manager().get_folder_name_protein_sequences())

    def __get_subpath_genome_reference_gtf_for_species(self, taxonomy_id):
        # The subpath is gtf/species.name
        return "{}/{}".format(self._get_configuration_manager().get_folder_name_gtf(),
                              self._get_ensembl_service()
                              .get_species_data_service()
                              .get_species_entry_for_taxonomy_id(taxonomy_id)
                              .get_name()
                              )

    def _get_logger(self):
        return self.__logger

    @staticmethod
    def _get_ensembl_service():
        return ensembl.service.get_service()

    def _get_configuration_manager(self):
        return self.__config_manager

    def get_local_path_root_ensembl_repo(self):
        if self.__local_path_ensembl_repo is None:
            # For improved reading and code maintenance later
            resources_folder_path = os.path.abspath(config_manager.get_app_config_manager().get_folder_resources())
            root_folder_ensembl_repo = self._get_configuration_manager().get_local_path_folder_ensembl_repo()
            self.__local_path_ensembl_repo = os.path.join(resources_folder_path, root_folder_ensembl_repo)
        return self.__local_path_ensembl_repo

    def get_local_path_ensembl_release(self):
        if self.__local_path_ensembl_release is None:
            self.__local_path_ensembl_release = os.path.join(self.get_local_path_root_ensembl_repo(),
                                                             self.get_ensembl_release_name())
        return self.__local_path_ensembl_release

    def get_ensembl_release_name(self):
        if self.__ensembl_release_name is None:
            ensembl_service = ensembl.service.get_service()
            self.__ensembl_release_name = "{}{}" \
                .format(self._get_configuration_manager().get_folder_prefix_ensembl_release(),
                        ensembl_service.get_release_number())
        return self.__ensembl_release_name

    def _get_protein_sequence_ensembl_file_name_for_species(self, taxonomy_id):
        # TODO
        # The name for a protein sequence file in Ensembl is
        # <species_name_with_first_capital_letter>.<species_assembly>.<file_type e.g. 'pep'>.[all,abinitio].fa
        # e.g. Homo_sapiens.GRCh38.pep.all.fa, on Ensembl will have the extension .gz, because it is a compressed file
        pass

    def get_protein_sequences_for_species(self, taxonomy_id):
        # TODO
        # Work out the file names for the data to retrieve from Ensembl
        # Work out their path in the local repository
        # Check if they already exist locally
        # If not, work out their remote path on Ensembl FTP
        # Retrieve the files
        pass

    def _get_genome_reference_gtf_ensembl_file_name_for_species(self, taxonomy_id):
        # TODO
        pass

    def get_genome_reference_gtf_for_species(self, taxonomy_id):
        # TODO
        # Work out the file names for the data to retrieve from Ensembl
        # Work out their path in the local repository
        # Check if they already exist locally
        # If not, work out their remote path on Ensembl FTP
        # Retrieve the files
        pass


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
