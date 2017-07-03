# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 03-07-2017 16:50
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This module contains Ensembl models used as Entities and DAO/Services
"""


class Species:
    def __init__(self, ensembl_species_entry):
        self.__ensembl_species_entry = ensembl_species_entry


class SpeciesService:
    # TODO
    pass
