# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='trackhub-creator',
    version='1.0.0',
    description='This is a pipeline to generate trackhubs for Ensembl, from either PRIDE Cluster or single projects',
    long_description=readme,
    author='Manuel Bernal-Llinares',
    author_email='mbdebian@gmail.com',
    url='https://github.com/Proteogenomics/trackhub-creator',
    license=license,
    packages=find_packages(exclude('tests', 'docs'))
)
