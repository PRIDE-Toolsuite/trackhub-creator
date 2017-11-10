# Overview
_TODO_

# How to set up the application
First thing, check out the application code using the _--recursive_ flag like
```
git clone --recursive <repo_url>
```
as this repository uses submodules, some of them will require having the access right for, at least, deploy the module code, otherwise, some of the pipelines shipped with this application will not work. 

Once the source code has been checked out, this software counts on a _Makefile_ for doing a lot of DevOps related heavy lifting.

There are two main installation targets:
- _**install**_, this is the usual installation target used when preparing a development setup of the application, or a production installation that doesn't have into account the possible presence of an HPC environment.
A _Python virtual environment_ will be prepared with all the application requirements, also, external tools needed by the application will be collected and made available.
- _**install_lsf**_, like the other installation target, this one will do the same, but taking into account the possible presence of an HPC environment.

# Using the Pipelines shipped with the application
For running any pipeline shipped with the application (or added to it), from the root folder of the application, the following command must be issued
```
time python_install/bin/python main_app.py -a pipeline_cmd_param1=pipeline_cmd_param1_value,...,pipeline_cmd_paramN=pipeline_cmd_paramN_value <pipeline_name>
```
This command will time the execution of the application, using the application's _Python virtual environment_ to run the given pipeline with the given command line _key=value_ parameters.

The following pipelines are shipped with the application:
- _**ensembl_data_collector**_
- _**pride_cluster_export**_
- _**create_trackhub_for_project**_
- _**publish_trackhub**_

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
This pipeline creates and registers / updates a trackhub for PRIDE Cluster data.

It is launched by the following script
```
scripts/pride-cluster-export/ebi-lsf-launch-pipeline.sh
```
straight away or as a job on the HPC environment.

It will create a subfolder at [PRIDE Cluster Trackhubs FTP](http://ftp.pride.ebi.ac.uk/pride/data/cluster/trackhubs/) as 'YYYY-MM', with the year and month information of the trackhub creation, and update a 'latest' link that points to the last created trackhub for [PRIDE Cluster](https://www.ebi.ac.uk/pride/cluster/#/).

More information on the process of creating a trackhub for  [PRIDE Cluster Trackhubs FTP](http://ftp.pride.ebi.ac.uk/pride/data/cluster/trackhubs/) as 'YYYY-MM', with the year and month information of the trackhub creation, and update a 'latest' link that points to the last created trackhub for [PRIDE Cluster](https://www.ebi.ac.uk/pride/cluster/#/) can be found [here](http://ftp.pride.ebi.ac.uk/pride/data/cluster/docs/trackhubs/).

## PRIDE Project Trackhub Creation Pipeline
This pipeline creates a trackhub for the given PRIDE project. It is launched by the script
```
scripts/create_trackhub_for_project/launch_pipeline_for_project.sh
```
and the only parameter it needs is the absolute path to a JSON formatted file that contains all the information related to the project being processed and the trackhub that is going to be created, e.g. title, long and short description, etc.

The following is a sample project description file content passed to this pipeline as a parameter
```json
{
  "trackHubName" : "PXD000625",
  "trackHubShortLabel" : "<a href=\"http://www.ebi.ac.uk/pride/archive/projects/PXD000625\">PXD000625</a> - Hepatoc...",
  "trackHubLongLabel" : "Experimental design For the label-free ...",
  "trackHubType" : "PROTEOMICS",
  "trackHubEmail" : "pride-support@ebi.ac.uk",
  "trackHubInternalAbsolutePath" : "...",
  "trackhubCreationReportFilePath": "...",
  "trackMaps" : [ {
    "trackName" : "PXD000625_10090_Original",
    "trackShortLabel" : "<a href=\"http://www.ebi.ac.uk/pride/archive/projects/PXD000625\">PXD000625</a> - Mus musc...",
    "trackLongLabel" : "Experimental design For the label-free proteome analysis 17 mice were used composed of 5 ...",
    "trackSpecies" : "10090",
    "pogoFile" : "..."
  } ]
}
```

_trackhubCreationReportFilePath_ points to a file where the pipeline, once it is done running, will dump a JSON formatted report on the trackhub creation process, as it can be seen in the sample underneath these lines.
```json
{
"status": "SUCCESS", 
"success_messages": [], 
"warning_messages": [], 
"error_messages": [],
"pipeline_session_working_dir": "...", 
"log_files": [], 
"hub_descriptor_file_path": "..."
}
```
where
- _**status**_, represents three possible outcomes on how the pipeline worked out
    - _SUCCESS_, all the project data has been successfully processed and the trackhub created.
    - _WARNING_, some project data failed to process but a trackhub was created with at least one track. More information can be found in the accompanying messages within this report.
    - _ERROR_, a trackhub could not be created for the given project data. More information can be found in the accompanying messages within this report.
- _**success_messages**_, a list of informative messages about the creation of the trackhub for the given project.
- _**warning_messages**_, a list of messages raising issues about the trackhub creation for the given project.
- _**error_messages**_, a list of messages stating the errors that rendered the trackhub creation process for the given project impossible.
- _**pipeline_session_working_dir**_, this is the working directory used by the application when running this pipeline.
- _**log_files**_, the list of absolute paths to all the log files related to the pipeline run for the given project, as with the working directory, this information is included in the report for forensic purposes.
- _**hub_descriptor_file_path**_, absolute path to the _hub.txt_ file created as part of the trackhub for the given project.

## Trackhub Publishing / Registering / Update Pipeline
This pipeline registers a trackhub at [Trackhub Registry](https://www.trackhubregistry.org/) and it can be launched by the script at
> scripts/publish_trackhub/publish_trackhub.sh

providing the following parameters
- _**user name**_, this is the user name to be used for registering the trackhub at the [Trackhub Registry](https://www.trackhubregistry.org/).
- _**password**_, to be used for registering the trackhub at the [Trackhub Registry](https://www.trackhubregistry.org/).
- _**trackhub description data file**_, this file describes the trackhub to be publish by this pipeline, as it can be seen in following sample file content.

```json
{
    "trackhubUrl": "http://host.com/hub.txt",
    "publicVisibility": "1",
    "type": "PROTEOMICS",
    "pipelineReportFilePath": "pipeline.report"
}
```
where
- _**trackhubUrl**_ is the public URL of the _hub.txt_ file for the trackhub to be published.
- _**publicVisibility**_, configures whether the trackhub being published is going to be public or private, if not included in the file, the default value is 'private'.
- _**type**_, this is the 'type' information to be assigned to the trakchub being published, if not included in the file, the default value is 'PROTEOMICS'.
- _**pipelineReportFilePath**_, absolute path to the file where the pipeline should provide a report on the process. As sample of that report content can be seen underneath these lines.

```json
{
"status": "...", 
"success_messages": [],
"warning_messages": [], 
"error_messages": [], 
"pipeline_session_working_dir": "...", 
"trackhub_url": "...", 
"log_files": [], 
"trackhub_registration_analysis": []
}
```
where
- _**status**_, represents three possible outcomes on how the pipeline worked out
    - _SUCCESS_, the trackhub was successfully published / updated.
    - _WARNING_, the trackhub was published / updated, but some errors occurred.
    - _ERROR_, the trackhub could not be published / updated.
- _**success_messages**_, a list of informative messages about the trackhub publishing process.
- _**warning_messages**_, a list of messages raising issues about the trackhub publishing process.
- _**error_messages**_, a list of messages stating the errors that rendered the trackhub publishing process.
- _**pipeline_session_working_dir**_, this is the working directory used by the application when running this pipeline.
- _**trackhub_url**_, URL of the _hub.txt_ trackhub file.
- _**log_files**_, the list of absolute paths to all the log files related to the pipeline run for the given project, as with the working directory, this information is included in the report for forensic purposes.

# For Developers
## Application Architecture
Along the following lines, there is a description of the different folders that are part of the application.

#### /bin
Contains well known locations to the binary files of the external tools used by the application, e.g. _cluster-file-exporter_, _PoGo_, etc.

#### /config
This folders holds all the configuration files, application and module wide, usually in JSON format.

There is a linked submodule, _private_, that contains sensitive configuration data, hosted in a private repository.

#### /data_formats
This is a helper module that contains _helpers_ for dealing with different data formats. At this iteration of the software, it mainly provides file format conversion for _Bed_ files into _BigBed_ files.

As for most of the modules that are shipped with the application, it counts on a _config_manager_ that manages module wide configuration.

#### /docs
It is a placeholder for documentation related to the application, although the general preference is having all the documentation available on-line, it may be useful for documenting some parts of the application itself from the point of view of the processing it models, or some external tools used by the application.

#### /download_manager
This module contains a _Download Manager_ for the application, that will grab files from the internet in a multithreaded way. An example on how to use this module for downloading files from the internet can be found in the _unit tests_.

#### /ensembl
Ensembl services, through a [REST API](https://rest.ensembl.org), are used for processing _species_ data, and gathering _protein sequence_ and _genome reference_ files, e.g. for producing _Bed_ files that are part of the _trackhub_ creation process. This module contains service wrappers for accessing all that information and automatically grab those data files from the internet.

####  /hpc
An HPC environment may be present when running the application, this module models the detection and interaction with such an environment. This is useful in cases when, for example, we want to parallelize subtasks by fully leveraging the computing system available.

As with other modules in the application, it counts on a _Configuration Manager_ to shape some aspects of the module.

#### /logs
Everytime the application is launched, a _session_ is started, and two log files are created, associated with that running session, with two different suffixes:
- _debug_, contains all log messages down to _debug_ level.
- _info_, contains only those log messages that are _info_ or upper logging level.

#### /parallel
Within this module, base classes and factories provide scaffolding for parallelizing subtasks as either separated threads (at this iteration of the software) or HPC jobs. A simple _Manager_ implementation is provided for dealing with launching multiple parallel subtasks and waiting for them to finish, as well as error handling.

#### /pipelines
Available pipelines **must** be placed in this folder, and they should follow a similar structure to the one in _template_pipeline.py_, also using it as the "abstract base" definition of a pipeline for best integration results.

Examples on how to extend the application with more pipelines can be taken from the ones already shipped with the application in this iteration:
- _create_trackhub_for_project_
- _ensembl_data_collector_
- _pride_cluster_export_
- _publish_trackhub_

#### /pogo
[PoGo](https://github.com/cschlaffner/PoGo) is used by the application to create the _Bed_ files that will be part (as _BigBed_) of the newly created trackhub. This module implements the models for working with this external tool.

#### /resources
This folder is a _well known_ location for the application, it is devoted to resources (mainly data assets) used by the application when running a pipeline, e.g. the mirrored Ensembl data.

#### /run
Everytime a pipeline is launched with this application, a new session is started, and a **unique** _working directory_ is created for that session to mess with, within this folder.

#### /scripts
Launching helper scripts for the different pipelines are provided here as either a private or public submodule link, depending on whether they contain sensitive information or not.

Some of the scripts already linked to the application (some of them are private, so the corresponding access rights are required)

##### commons/helper_functions.sh
Public common helper functions.

##### commons-priv/*
General environment cleaning and preparation scripts that are private, as they contain sensitive information.

## Unit Testing
## Extending the Application with more Pipelines

# Final Notes
The default Trackhub Registry service used by the pipelines is the one at [www.trackhubregistry.org](https://www.trackhubregistry.org/).

### Contact
Manuel Bernal Llinares
