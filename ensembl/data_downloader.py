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

# TODO - This file just got too large, refactor it in the future to make it more simple

import os

# App imports
import config_manager
import ensembl.service
from exceptions import ConfigManagerException
from download_manager.manager import Manager as DownloadManager
from ensembl.exceptions import EnsemblDownloadManagerException
from toolbox import general

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
    _CONFIG_KEY_FILE_SUFFIXES = 'file_suffixes'
    _CONFIG_KEY_FILE_EXTENSION = 'file_extension'
    _CONFIG_KEY_GTF_FILE = 'gtf_file'

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
                "MISSING configuration information '{}.{}.{}' in configuration file '{}', because of '{}'".format(
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
                "MISSING configuration information '{}.{}.{}' in configuration file '{}', because of '{}'".format(
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
                "MISSING configuration information '{}.{}.{}' in configuration file '{}', because of '{}'".format(
                    self._CONFIG_KEY_DATA_DOWNLOADER,
                    self._CONFIG_KEY_ENSEMBL_FTP,
                    self._CONFIG_KEY_FOLDER_NAME_GTF,
                    self._get_configuration_file(),
                    str(e)))

    def get_ensembl_protein_sequence_file_type(self):
        """
        For protein sequence files, the file type string is usually 'pep', and it is found at the end of the file name,
        just before the suffixes, e.g. all or abinitio.

        Just in case Ensembl decides to change it in the future, it has been introduced in the software as a
        configuration defined value.
        :return: file type string for ensembl protein sequence files as specified in the configuration file
        """
        try:
            return self._get_configuration_object() \
                [self._CONFIG_KEY_DATA_DOWNLOADER] \
                [self._CONFIG_KEY_ENSEMBL_FILE_NAMES] \
                [self._CONFIG_KEY_PROTEIN_SEQUENCE_FILE] \
                [self._CONFIG_KEY_FILE_TYPE]
        except Exception as e:
            # TODO - Refactor this code whenever you have time, because a pattern has emerged here
            raise ConfigManagerException(
                "MISSING configuration information  '{}.{}.{}.{}' in configuration file '{}', because of '{}'".format(
                    self._CONFIG_KEY_DATA_DOWNLOADER,
                    self._CONFIG_KEY_ENSEMBL_FILE_NAMES,
                    self._CONFIG_KEY_PROTEIN_SEQUENCE_FILE,
                    self._CONFIG_KEY_FILE_TYPE,
                    self._get_configuration_file(),
                    str(e)))

    def get_ensembl_protein_sequence_file_suffixes(self):
        """
        Usually, protein sequence files in Ensembl have two suffixes (just before the file extension): 'all' and
        'abinitio'. But it's been set in the application as a configurable parameter just in case they change that (very
        unlikely) future.
        :return: a list of suffixes for protein sequence files on Ensembl
        """
        try:
            return self._get_configuration_object() \
                [self._CONFIG_KEY_DATA_DOWNLOADER] \
                [self._CONFIG_KEY_ENSEMBL_FILE_NAMES] \
                [self._CONFIG_KEY_PROTEIN_SEQUENCE_FILE] \
                [self._CONFIG_KEY_FILE_SUFFIXES]
        except Exception as e:
            # TODO - Refactor this code whenever you have time, because a pattern has emerged here
            raise ConfigManagerException(
                "MISSING configuration information '{}.{}.{}.{}' in configuration file '{}', because of '{}'".format(
                    self._CONFIG_KEY_DATA_DOWNLOADER,
                    self._CONFIG_KEY_ENSEMBL_FILE_NAMES,
                    self._CONFIG_KEY_PROTEIN_SEQUENCE_FILE,
                    self._CONFIG_KEY_FILE_SUFFIXES,
                    self._get_configuration_file(),
                    str(e)))

    def get_ensembl_protein_sequence_file_extension(self):
        """
        Usually, protein sequence files have extension ".fa" in Ensembl, but it has been included here as a configurable
        parameter just in case they change that in the future.
        :return: the file extension, very likely to be 'fa'
        """
        try:
            return self._get_configuration_object() \
                [self._CONFIG_KEY_DATA_DOWNLOADER] \
                [self._CONFIG_KEY_ENSEMBL_FILE_NAMES] \
                [self._CONFIG_KEY_PROTEIN_SEQUENCE_FILE] \
                [self._CONFIG_KEY_FILE_EXTENSION]
        except Exception as e:
            # TODO - Refactor this code whenever you have time, because a pattern has emerged here
            raise ConfigManagerException(
                "MISSING configuration information '{}.{}.{}.{}' in configuration file '{}', because of '{}'".format(
                    self._CONFIG_KEY_DATA_DOWNLOADER,
                    self._CONFIG_KEY_ENSEMBL_FILE_NAMES,
                    self._CONFIG_KEY_PROTEIN_SEQUENCE_FILE,
                    self._CONFIG_KEY_FILE_EXTENSION,
                    self._get_configuration_file(),
                    str(e)))

    def get_ensembl_gtf_file_suffixes(self):
        """
        Usually, GTF files in Ensembl have four suffixes (just before the file extension):
        '', 'chr', 'chr_patch_hapl_scaff' and 'abinitio'. But it's been set in the application as a configurable
        parameter just in case they change that (very unlikely) future.
        :return: a list of suffixes for GTF files on Ensembl
        """
        try:
            return self._get_configuration_object() \
                [self._CONFIG_KEY_DATA_DOWNLOADER] \
                [self._CONFIG_KEY_ENSEMBL_FILE_NAMES] \
                [self._CONFIG_KEY_GTF_FILE] \
                [self._CONFIG_KEY_FILE_SUFFIXES]
        except Exception as e:
            # TODO - Refactor this code whenever you have time, because a pattern has emerged here
            raise ConfigManagerException(
                "MISSING configuration information '{}.{}.{}.{}' in configuration file '{}', because of '{}'".format(
                    self._CONFIG_KEY_DATA_DOWNLOADER,
                    self._CONFIG_KEY_ENSEMBL_FILE_NAMES,
                    self._CONFIG_KEY_GTF_FILE,
                    self._CONFIG_KEY_FILE_SUFFIXES,
                    self._get_configuration_file(),
                    str(e)))

    def get_ensembl_gtf_file_extension(self):
        """
        Usually, GTF files have extension ".gtf" in Ensembl, but it has been included here as a configurable
        parameter just in case they change that in the future.
        :return: the file extension, very likely to be 'gtf'
        """
        try:
            return self._get_configuration_object() \
                [self._CONFIG_KEY_DATA_DOWNLOADER] \
                [self._CONFIG_KEY_ENSEMBL_FILE_NAMES] \
                [self._CONFIG_KEY_GTF_FILE] \
                [self._CONFIG_KEY_FILE_EXTENSION]
        except Exception as e:
            # TODO - Refactor this code whenever you have time, because a pattern has emerged here
            raise ConfigManagerException(
                "MISSING configuration information '{}.{}.{}.{}' in configuration file '{}', because of '{}'".format(
                    self._CONFIG_KEY_DATA_DOWNLOADER,
                    self._CONFIG_KEY_ENSEMBL_FILE_NAMES,
                    self._CONFIG_KEY_GTF_FILE,
                    self._CONFIG_KEY_FILE_EXTENSION,
                    self._get_configuration_file(),
                    str(e)))

    def is_rewrite_local_path_ensembl_repo(self):
        """
        Find out whether we are required to overwrite the local Ensembl repository or not, in case there is an existing
        one for the same release we are collecting data from.
        :return: True if we have to rewrite it, False otherwise
        """
        try:
            return self._get_configuration_object() \
                       [self._CONFIG_KEY_DATA_DOWNLOADER] \
                       [self._CONFIG_KEY_REWRITE_LOCAL_PATH_ENSEMBL_REPO] == "True"
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
        self.__remote_path_ensembl_release = None
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
        general.check_create_folders([self.get_local_path_root_ensembl_repo()])
        self._get_logger().debug("Local path for Ensembl Release - '{}'"
                                 .format(self.get_local_path_ensembl_release()))
        if self._get_configuration_manager().is_rewrite_local_path_ensembl_repo():
            self._get_logger().debug("Creating folder in 'OVERWRITE' mode - '{}'"
                                     .format(self.get_local_path_ensembl_release()))
            general.check_create_folders_overwrite([self.get_local_path_ensembl_release()])
        else:
            self._get_logger().debug("Creating folder if it doesn't exist - '{}'"
                                     .format(self.get_local_path_ensembl_release()))
            general.check_create_folders([self.get_local_path_ensembl_release()])
        general.create_latest_symlink_overwrite(self.get_local_path_ensembl_release())

    def __get_subpath_fasta_for_species(self, taxonomy_id):
        # The subpath is fasta/species.name
        self._get_logger().debug("__get_subpath_fasta_for_species for taxonomy id '{}'".format(taxonomy_id))
        return "{}/{}".format(self._get_configuration_manager().get_folder_name_fasta(),
                              self._get_ensembl_service()
                              .get_species_data_service()
                              .get_species_entry_for_taxonomy_id(taxonomy_id)
                              .get_name())

    def __get_subpath_protein_sequence_for_species(self, taxonomy_id):
        # The subpath is fasta/species.name/pep
        self._get_logger().debug("__get_subpath_protein_sequence_for_species for taxonomy id '{}'".format(taxonomy_id))
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

    def get_remote_path_root_ensembl_repo(self):
        """
        Get the root URL for the Ensembl remote repository, usually an FTP URL like 'ftp://ftp.ensembl.org/pub'
        :return: Ensembl root repo URL
        """
        return self._get_configuration_manager().get_ensembl_ftp_base_url()

    def get_remote_path_ensembl_release(self):
        """
        Get the remote URL for the current release of Ensembl, usually an FTP URL like
        'ftp://ftp.ensembl.org/pub/release-89'
        :return: Current Ensembl release repository URL
        """
        if not self.__remote_path_ensembl_release:
            self.__remote_path_ensembl_release = "{}/{}".format(self.get_remote_path_root_ensembl_repo(),
                                                                self.get_ensembl_release_name())
        return self.__remote_path_ensembl_release

    def get_ensembl_release_name(self):
        if self.__ensembl_release_name is None:
            ensembl_service = ensembl.service.get_service()
            self.__ensembl_release_name = "{}{}" \
                .format(self._get_configuration_manager().get_folder_prefix_ensembl_release(),
                        ensembl_service.get_release_number())
        return self.__ensembl_release_name

    def _get_protein_sequence_ensembl_file_name_for_species(self, taxonomy_id):
        """
        The name for a protein sequence file in Ensembl is
        <species_name_with_first_capital_letter>.<species_assembly>.<file_type e.g. 'pep'>.[all,abinitio].fa
        e.g. Homo_sapiens.GRCh38.pep.all.fa, on Ensembl will have the extension .gz, because it is a compressed file
        :param taxonomy_id: taxonomy ID for which to work out the file name
        :return: the file name, without the .gz extension that is found on Ensembl FTP
        """
        species_name = self._get_ensembl_service() \
            .get_species_data_service() \
            .get_species_entry_for_taxonomy_id(taxonomy_id) \
            .get_name().capitalize()
        assembly = self._get_ensembl_service() \
            .get_species_data_service() \
            .get_species_entry_for_taxonomy_id(taxonomy_id) \
            .get_assembly()
        file_type = self._get_configuration_manager().get_ensembl_protein_sequence_file_type()
        file_extension = self._get_configuration_manager().get_ensembl_protein_sequence_file_extension()
        return ["{}.{}.{}.{}.{}".format(species_name,
                                        assembly,
                                        file_type,
                                        suffix,
                                        file_extension)
                for suffix in self._get_configuration_manager().get_ensembl_protein_sequence_file_suffixes()]

    def _get_protein_sequence_file_destination_path_local(self, taxonomy_id):
        """
        Get the local destination folder for protein sequence files given a taxonomy.

        Usually like <local_ensembl_root_repo>/<current_ensembl_release>/fasta/<taxonomy_name>/pep
        :param taxonomy_id: species for which to calculate the local destination path
        :return: local destination path for protein sequence files for the given taxonomy and the current Ensembl release
        """
        return os.path.join(self.get_local_path_ensembl_release(),
                            self.__get_subpath_protein_sequence_for_species(taxonomy_id))

    def _get_protein_sequence_file_path_local(self, taxonomy_id, file_names):
        """
        The local file path for a protein file name is
        <local_path_ensembl_release>/<subpath_protein_sequence_for_species>/file_name (local copies of Ensembl files are
        stored uncompressed, that's why we use the given name for every file)
        :param file_names: protein sequence file names
        :return: a list of tuples of the form (file_name, absolute path to that file in the local Ensembl repository)
        """
        return [(file_name, os.path.abspath(
            os.path.join(self._get_protein_sequence_file_destination_path_local(taxonomy_id),
                         file_name))) for file_name in file_names]

    def _get_protein_sequence_file_path_remote(self, file_names, species):
        """
        Given a list of protein sequence file names, this will return a list of tuples, each with the file name and its
        remote URL in the current Ensembl release.

        Note that it will add them the extension .gz as that's the way they are on Ensembl
        :param file_names: protein sequence file names
        :param species: the species we want the files for
        :return: a list of tuples containing the file name and its remote path on Ensembl FTP
        """
        base_url = "{}/{}".format(
            self.get_remote_path_ensembl_release(),
            self.__get_subpath_protein_sequence_for_species(species)
        )
        return [(file_name, "{}/{}.gz".format(base_url, file_name)) for file_name in file_names]

    def get_protein_sequences_for_species(self, taxonomy_id):
        # Work out the file names for the data to retrieve from Ensembl
        file_names = self._get_protein_sequence_ensembl_file_name_for_species(taxonomy_id)
        self._get_logger().debug("Working with Ensembl protein sequence file names for taxonomy ID '{}' - '{}'"
                                 .format(taxonomy_id, str(file_names)))
        # Work out their path in the local repository
        protein_sequence_files_local_path = self._get_protein_sequence_file_path_local(taxonomy_id, file_names)
        self._get_logger().debug("Local Ensembl Repo protein sequence paths for taxonomy ID '{}', file paths '{}'"
                                 .format(taxonomy_id, str(protein_sequence_files_local_path)))
        # Check if they already exist locally
        missing_files = [(missing_file_name, missing_file_path)
                         for missing_file_name, missing_file_path
                         in protein_sequence_files_local_path
                         if not os.path.exists(missing_file_path)]
        if missing_files:
            # Work out their remote path on Ensembl FTP
            self._get_logger() \
                .debug("There are {} protein sequence files missing from the local repository "
                       "for taxonomy ID '{}': {}"
                       .format(len(missing_files),
                               taxonomy_id,
                               "[{}]".format(","
                                             .join(["'{} -> {}'"
                                                   .format(missing_file_name, missing_file_path)
                                                    for missing_file_name, missing_file_path
                                                    in missing_files]))))
            # Retrieve the files, keep in mind that _get_protein_sequence_file_path_remote operates on file names
            download_information = self._get_protein_sequence_file_path_remote(
                [file_entry[0] for file_entry in missing_files],
                taxonomy_id)
            destination_folder = self._get_protein_sequence_file_destination_path_local(taxonomy_id)
            # Make sure that the destination folder exists
            general.check_create_folders([destination_folder])
            download_urls = [url for file_name, url in download_information]
            self._get_logger().info("Protein Sequence files to download to '{}': '{}'".format(
                destination_folder,
                ",".join(download_urls)))
            download_manager = DownloadManager(download_urls,
                                               destination_folder,
                                               self._get_logger())
            download_manager.start_downloads()
            download_manager.wait_all()
            if not download_manager.is_success():
                self._get_logger().error("ERROR Downloading files from Ensembl !!!")

            # Once the files have been downloaded, we know they come compressed from Ensembl, with .gz extension
            # Uncompress the files
            # I have their local paths in 'missin_files' second component of the pairs in the list, I just need to add
            # the '.gz' extension for them, as they come gzipped from Ensembl
            errors = general.gunzip_files(
                ["{}.gz".format(file_local_path) for file_name, file_local_path in missing_files])
            # Deal with possible errors
            if errors:
                msg = "An ERROR occurred while obtaining the following protein sequence files " \
                      "for taxonomy ID '{}' -> '{}'".format(taxonomy_id,
                                                            ",".join(
                                                                ["File '{}', ERROR '{}'"
                                                                     .format(file, error) for file, error in errors]
                                                            ))
                self._get_logger().error(msg)
                raise EnsemblDownloadManagerException(msg)

    def _get_genome_reference_file_destination_path_local(self, taxonomy_id):
        """
        Get the local destination folder for GTF files given a taxonomy.

        Usually like <local_ensembl_root_repo>/<current_ensembl_release>/gtf/<taxonomy_name>
        :param taxonomy_id: species for which to calculate the local destination path
        :return: local destination path for GTF files for the given taxonomy and the current Ensembl release
        """
        return os.path.join(self.get_local_path_ensembl_release(),
                            self.__get_subpath_genome_reference_gtf_for_species(taxonomy_id))

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
