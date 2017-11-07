# Overview
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
- _pipelineReportFilePath_, absolute path to the file where the pipeline should provide a report on the process. As sample of that report content can be seen underneath these lines.

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
- _status_, represents three possible outcomes on how the pipeline worked out
    - _SUCCESS_, the trackhub was successfully published / updated.
    - _WARNING_, the trackhub was published / updated, but some errors occurred.
    - _ERROR_, the trackhub could not be published / updated.
- _success_messages_, a list of informative messages about the trackhub publishing process.
- _warning_messages_, a list of messages raising issues about the trackhub publishing process.
- _error_messages_, a list of messages stating the errors that rendered the trackhub publishing process.
- _pipeline_session_working_dir_, this is the working directory used by the application when running this pipeline.
- _trackhub_url_, URL of the _hub.txt_ trackhub file.
- _log_files_, the list of absolute paths to all the log files related to the pipeline run for the given project, as with the working directory, this information is included in the report for forensic purposes.

# Application Architecture

### Contact
Manuel Bernal Llinares