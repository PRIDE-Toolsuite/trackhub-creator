# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 02-08-2017 16:40
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This module contains models for dealing with PoGo stuff
"""

import os


class PogoRunResult:
    def __init__(self):
        self.__ncbi_taxonomy_id = None
        self.__pogo_source_file_path = None
        self.__protein_sequence_file_path = None
        self.__gtf_file_path = None
        # Map<pogo_result_file_extension, pogo_result_file_path>
        self.__pogo_result_file_paths = {}

    def __init__(self,
                 ncbi_taxonomy_id,
                 pogo_source_file_path,
                 protein_sequence_file_path,
                 gtf_file_path):
        """
        Syntactic sugar constructor
        :param ncbi_taxonomy_id: ncbi taxonomy id for this PoGo run results
        :param pogo_source_file_path: path of the source file used to run PoGo
        """
        self.__init__()
        self.set_ncbi_taxonomy_id(ncbi_taxonomy_id)
        self.set_pogo_source_file_path(pogo_source_file_path)
        self.set_protein_sequence_file_path(protein_sequence_file_path)
        self.set_gtf_file_path(gtf_file_path)

    def __generate_pogo_result_file_paths(self, pogo_source_file_path):
        pogo_results_folder_path = os.path.dirname(pogo_source_file_path)
        pogo_source_file_name = os.path.basename(pogo_source_file_path)

    def set_ncbi_taxonomy_id(self, taxonomy_id):
        self.__ncbi_taxonomy_id = taxonomy_id

    def set_pogo_source_file_path(self, pogo_source_file_path):
        if not self.__pogo_source_file_path or (self.__pogo_source_file_path != pogo_source_file_path):
            self.__pogo_source_file_path = pogo_source_file_path
            # Regenerate pogo result file paths
            self.__generate_pogo_result_file_paths(pogo_source_file_path)

    def set_protein_sequence_file_path(self, protein_sequence_file_path):
        self.__protein_sequence_file_path = protein_sequence_file_path

    def set_gtf_file_path(self, gtf_file_path):
        self.__gtf_file_path = gtf_file_path

    def add_pogo_result_file_path(self, pogo_result_file_path):
        self.__pogo_result_file_paths.add(pogo_result_file_path)
