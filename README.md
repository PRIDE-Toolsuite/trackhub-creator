# Overview
# How to set up the application
First thing, check out the application code using the _--recursive_ flag like
```
git clone --recursive <repo_url>
```
as this repository uses submodules, some of them will require having the access right for, at least, deploy the module code, otherwise, some of the pipelines shipped with this application will not work. 

Once the source code has been checked out, this software counts on a _Makefile_ for doing a lot of DevOps related heavy lifting.

There are two main installation targets:
- _install_, this is the usual installation target used when preparing a development setup of the application, or a production installation that doesn't have into account the possible presence of an HPC environment.
A _Python virtual environment_ will be prepared with all the application requirements, also, external tools needed by the application will be collected and made available.
- _install_lsf_, like the other installation target, this one will do the same, but taking into account the possible presence of an HPC environment.

# Using the Pipelines shipped with the application
For running any pipeline shipped with the application (or added to it), from the root folder of the application, the following command must be issued
```
time python_install/bin/python main_app.py -a pipeline_cmd_param1=pipeline_cmd_param1_value,...,pipeline_cmd_paramN=pipeline_cmd_paramN_value <pipeline_name>
```
This command will time the execution of the application, using the application's _Python virtual environment_ to run the given pipeline with the given command line _key=value_ parameters.

The following pipelines are shipped with the application:
- _ensembl_data_collector_
- _pride_cluster_export_
- _create_trackhub_for_project_
- _publish_trackhub_

## Enemsebl Data Collector Pipeline
Other pipelines shipped with this application, e.g. _create_trackhub_for_project_, use Ensembl protein sequence and genome reference files as part of the _trackhub_ creation process, this files are mirrored locally in the application from the latest [Ensembl](https://www.ensembl.org/info/data/ftp/index.html) release, as the same application can be running different pipelines in parallel, this pipeline is recommended to be used in order to avoid race conditions mirroring those files.

This pipeline will mirror _protein sequence_ and _genome_reference_ files from [Ensembl](https://www.ensembl.org/info/data/ftp/index.html), for the given list of _NCBI Taxonomy IDs_, e.g. Mouse and Human as it can be seen beneath this line.
```
time python_install/bin/python main_app.py -a ncbi_taxonomy_ids=10090,9606 ensembl_data_collector 
```
Those files will be made locally available at 
> resources/ensembl/release-XX

within the application folder, where _XX_ is the latest Ensembl Release Number.

There is a launch script specific to PRIDE data, that collects Ensembl data for all the taxonomies present in PRIDE, it can be found at
> scripts/ensembl_data_collector

and it can be launched either straight away or as an HPC job
```
scripts/ensembl_data_collector/launch_pipeline_for_pride_taxonomies.sh 
```

## PRIDE Cluster Export Pipeline

## PRIDE Project Trackhub Creation Pipeline

## Trackhub Publishing / Registering / Update Pipeline

# Application Architecture

### Contact
Manuel Bernal Llinares