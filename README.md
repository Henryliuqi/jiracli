[TOC]

### Introduction

This tool is to manage the JIRA by command line.  All task/bugs are expected to be logged into JIRA to make the project manageable/trackable and also to avoid the unnecessary communication. 

### Installation

1. install python 2
2. pip install jira
3. pip install cmd2
4. pip install openpyxl
5. Python Timeline: http://thetimelineproj.sourceforge.net/ 
   1. NOTE: only windows are well supported now. 
6. Install pandoc
   1. Download the pandoc from [download](https://github.com/jgm/pandoc/releases/tag/1.19.2.1) or from internal \\10.193.108.156\packages\share\tools\pandoc

### Whole Picture

Here is the picture showing the design of this tool:



![][jiracli_arch]



JIRACLI consists of 2 parts: JIRAbase and JIRACLI applications.  JIRABase provides the fundamental operations method to do with JIRA `Issues` and `Versions`.  The operations are about `create`, `update`, `search`.  JIRACLI application call the JIRABase to implement the specific functionality.  For example, JIRACLI provide the command line interpreter to do with the JIRA `versions` and `issues`. 

#### JIRABase

2 entities are the key of the JIRA resources: `version` and `issue`. `MyIssue` and `MyVersion` are classes designed for these resources. They are all inherited from the class of `MyJIRAResource` to share some comment method and parameters. 

#### JIRA APP: JIRACLI

JIRA command line interpreter. 

**Usage**

See the content below.  When you use the `search`, search.xlsx for versions and versionsearch.xlsx will be created including the search results. 

```
$ python jiracli.py
User:b36089
Password:
Getting veresions for project [KPSDK]
JIRA CLI>>help

Documented commands (type help <topic>):
========================================
_relative_load  edit  help     list  pause  quit  save  shell      show
cmdenvironment  eof   history  load  py     run   set   shortcuts

Undocumented commands:
======================
create_issues    search_issues    update_issues
create_versions  search_versions  update_versions

JIRA CLI>>search_versions NIOBE1
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Searching Versions....
TAG: NIOBE1
KSDK_2.2.0_NIOBE1_RFP_RC1
KSDK_2.2.0_NIOBE1_RFP_RC2                   2017-12-30
KSDK_2.2.0_NIOBE1_RFP                       2017-12-30
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
Write resources to versionsearch.xlsx
JIRA CLI>>search_issues key in (KPSDK-14900)
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Searching Issues....
JQL: key in (KPSDK-14900)
KPSDK-14900 MCUXpresso SDK KSDK_2.3.0_REL7_RFP
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
Write resources to search.xlsx
JIRA CLI>>

```

#### JIRA-APP: JIRA Report

The target of this script is to create a base on creating the weekly report and encourge developer to always record status/analysis/resolution to JIRA ticket to enhance the efficiency of collabration. Also to encourge developer to create JIRA ticket for each task if possible. It will create the HTML report `report.html`, `report.xlsx`, `myrelease.timeline` . The timeline file can be opened by `timeline` and it will display all the JIRA version concerned in figure.  The html file will list/sort the concerned JIRA tickets inside.

**What is collected from JIRA ticket**

Bacially, the script will collect information for a JIRA tickets from fields below and user is required to put the status in the JIRA ticket to let the script to collect these information automatcially. 

1. `resolutiontext`
2. `analysis report`
3. `comment`: only comment contains identifier `STATUS_UPDATE` will be collected. Other comments will be ignored. 

NOTE:

> NOTE:
>
> format in these fields will be removed. All the end of line character \r or \r\n will be removed to avoid messing the created report.  So the tables, picture, hyper links will be displayed as the raw source mode. User need to refine these format accordingly.

**What kind of JIRA will be collected**

The script can collect JIRA informaiton from different apsect:

1. Tickets assigned to specified assignees with the coreid in JIRA account. see the parameter of `-a`. By default, the SDK core team are the assignees if assignees are not specified.
2. Tickets updated during specified date to now.  You can specify the date (`d`) or weeks (`w`).  see the parameter of `-d`. By default, the ticket updated in past week will be collected if no `-d` parameter provided.
3. Tickets that is not resolved assigned to specified assignees.  see the parameter of `-u`. 
4. Tickets whose fix versions or affected version are specified by identifier. see the parameter of `-v`. script will get all JIRA versions contained identifier specified by `-v` and check the relevant JIRA ticket.  you can specify `-v RT1050` to collect all JIRA inforamtion relevant to NPI RT1050.  You can specify multiple `-v` to get JIRA tickets with either of these identifier satisfied. 


**How to ignore the some JIRAs and recreate the report**

Sometimes, though the ticket is updated in the past period but these update are not needed. User can ignore these tickets by updating the created excel files with the field of `visible`.  The default value of `visible` is NA. Once user update the field apart from the `NA`,  the regenerted HTML report will ignore these JIRA tickets.  To regenerate the report, here is an example:

> Examples: python jirareport.py -e report.xlsx

**How to sort the report per request**

User can also specify the sorted level of the HTML report. see parameter of `-s`.  Multiple `-s` can be specified in sequence and the HTML report will be generated according to these levels. Multiple items can be specified for sorting: `npi`, `version`, `priority`, `status`. The default sort sequence is `-s npi -s version -s status` if no `-s` parameter is provied.

> Example: python jirareport.py -a b36089 -v REL7 -s npi -s version -s priority
>
> It will generate HTML report below:
>
> - REL7
>   - KSDK_2.3.0_REL7_RFP_RC1
>     - 3- Major
>       - [KPSDK-16966](https://jira.sw.nxp.com/browse/KPSDK-16966) [Closed][ftm_quad_decoder]case fail because interrupt function name is different with its macro
>         - RESOLUTION `commit a55e5bd0fa85731f3a61fa0b4c88fec481cf5093Author: Susan Su <susan.su@nxp.com>Date: Mon Jul 10 20:38:44 2017 +0800 KPSDK-16653 Add DSB before the BX LR in interrupt handler - As a workaround for ARM Errata 838869 for all kinetis M4/M4F cores Signed-off-by: Susan Su <susan.su@nxp.com>`
>   - KSDK_2.3.0_REL7_RFP_RC2
>     - 2- Critical
>       - [KPSDK-17789](https://jira.sw.nxp.com/browse/KPSDK-17789) [Closed][REL7_RC1][USB][dev_composite_hid_mouse_hid_keyboard]case build fail.
>         - RESOLUTION `The workaround is to increase the level of the folder whether the SDKpackage is unzipped. Â There is no official solution for the long cache file created by CMAKE in windows.`
>   - KSDK_2.3.0_REL7_RFP_RC3
>     - 3- Major
>       - [KPSDK-17782](https://jira.sw.nxp.com/browse/KPSDK-17782) [In Progress] Put the generator log into jason format

**Full documentation**

```
usage: jirareport.py [-h] [-u] [-e EXCEL] [-s SORTER] [-v VERSIONS]
                     [-d UPDATE] [-a]

Create Weekly report for specified assigned. Get the Markdown report from report.md and get the html report from report.html. You can copy the html report into onenote as basis of weekly report.

optional arguments:
  -h, --help            show this help message and exit
  -u, --unresolved      Whether to list unresolved tickets to this report but
                        not limited to the update time.
  -e EXCEL, --excel EXCEL
                        After the generation of report. Excel file will be
                        created. However, some tickets make no sense in report
                        you may want to ignore it. You can open the excel and
                        change the visible column value to other value but not
                        NA. Then you can specify the excel file and the report
                        html file will be regenerated.
  -s SORTER, --sorter SORTER
                        It tell how to sort the report in html. Several fields
                        are supported, npi, version, priority, assignee,
                        status. To specify multiple level of sorters, use
                        multile -s. Example, -s npi -s version -s status. Note
                        here this is the default sort sequence.
  -v VERSIONS, --versions VERSIONS
                        Specify the version the report cares. For example, -v
                        2.4.0, you only care JIRA ticket with fix version with
                        2.4.0 inside. You can specify multiple verison tags
                        like -s 2.2.0 -s 2.3.0 -s 2.4.0. These conditions will
                        be ORed. If not specified, JQL won't take the version
                        as part of search condition
  -d UPDATE, --update UPDATE
                        w means week. d means day. Assign a value that this
                        will checked tickets assigned to you and it is updated
                        >= the update time specified by you. The default value
                        is 1w, which means in the past week. Example, -d 1d,
                        -d 3w
  -a , --assignees      Assignees of the team to be calculater. It is combined
                        by ',' and it use the core id as identifier. For
                        example, b36089,b12345
```

**Typical case**

```python
python jirareport.py -a b36089  ## Get the tickets assigned to b36089 which was updated in past week.

python jirareport.py -s RT1050 -d 9d -s npi -s version -s priority ## Get the tickets assigned to b36089 and upated in the past 9 days. These ticket either with RT1050 relevant JIRA version in affectedVersion or in fixVersions.

python jirareport.py -e report.xlsx -s npi -s priority ## parse the previously generated excel files and resort the report accoding to firstly npi name then priority and then generate the html report again.

python jirareport.py -a b36089 -d 3d -u  ## Get the tickets assign to b36089 which was updated in last 3 days or that is not resolved.
```

#### JIRAAPP: JIRA Release

Script to create/update JIRA tickets for a given releases.  For a NPI release, [release requirement]([Template for the software release ticket](onenote:https://nxp1.sharepoint.com/sites/mcu_mcux_scm/SiteAssets/MCU_MCUX_SCM%20Notebook/Release%20Model.one#Template%20for%20the%20software%20release%20ticket&section-id={F5924ACC-3DF7-4447-84B9-C174F00FB04E}&page-id={B9BAACF0-1AA3-0F44-B578-24C604313F16}&end)  ([Web view](https://nxp1.sharepoint.com/sites/mcu_mcux_scm/_layouts/OneNote.aspx?id=%2Fsites%2Fmcu_mcux_scm%2FSiteAssets%2FMCU_MCUX_SCM%20Notebook&wd=target%28Release%20Model.one%7CF5924ACC-3DF7-4447-84B9-C174F00FB04E%2FTemplate%20for%20the%20software%20release%20ticket%7CB9BAACF0-1AA3-0F44-B578-24C604313F16%2F%29)) are describe here.  The script will check all the stuff according to input excel file. Get the input excel template from the metadate/release_template.xlsx

![][create_release]

**Usage**

With the picture above, it will create the specified versions or just update if these versions exist.  It will also create the tasks lists. Make sure don't delete the highlight parts. 

```
$ python jirarelease.py -f release_template.xlsx
User:b36089
Password:
Getting veresions for project [KPSDK]

**********Checking release information**********
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Searching Issues....
JQL: labels in (release_info) AND resolution = "Unresolved" AND summary ~ MXRT512
KPSDK-10852 MCUXpresso SDK MXRT512 release information
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

**********Checking versions**********
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Searching Versions....
TAG: MXRT512
KSDK_2.3.0_MXRT512_RFP          2017-10-16  2017-10-26
KSDK_2.3.0_MXRT512_EAR1         2017-05-01  2017-07-25
KSDK_2.3.0_MXRT512_RFP_RC2      2017-09-15  2017-10-16
KSDK_2.3.0_MXRT512_RFP_RC1      2017-08-24  2017-09-15
KSDK_2.3.0_MXRT512_EAR2         2017-07-25  2017-08-24
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

**********Checking SW Release Requset JIRA issues**********
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Searching Issues....
JQL: issuetype = "SW Release Request" AND fixVersion in (KSDK_2.3.0_MXRT512_RFP_RC2,KSDK_2.3.0_MXRT512_EAR1,KSDK_2.3.0_MXRT512_RFP_RC1,KSDK_2.3.0_MXRT512_RFP,KSDK_2.3.0_MXRT512_EAR2)
KPSDK-15108 MCUXpresso SDK MXRT512 KSDK_2.3.0_MXRT512_RFP_RC1
KPSDK-15100 MCUXpresso SDK MXRT512 KSDK_2.3.0_MXRT512_RFP
KPSDK-15091 MCUXpresso SDK MXRT512 KSDK_2.3.0_MXRT512_RFP_RC2
KPSDK-15079 MCUXpresso SDK MXRT512 KSDK_2.3.0_MXRT512_EAR2
KPSDK-15071 MCUXpresso SDK MXRT512 KSDK_2.3.0_MXRT512_EAR1
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
>>>>>>>
Doing with [link] [KPSDK-10852,Dependency]
Updated JIRA ISSUE:
KPSDK-15091 MCUXpresso SDK MXRT512 KSDK_2.3.0_MXRT512_RFP_RC2
<<<<<<<
>>>>>>>
Doing with [link] [KPSDK-10852,Dependency]
Updated JIRA ISSUE:
KPSDK-15071 MCUXpresso SDK MXRT512 KSDK_2.3.0_MXRT512_EAR1
<<<<<<<
>>>>>>>
Doing with [link] [KPSDK-10852,Dependency]
Updated JIRA ISSUE:
KPSDK-15108 MCUXpresso SDK MXRT512 KSDK_2.3.0_MXRT512_RFP_RC1
<<<<<<<
>>>>>>>
Doing with [link] [KPSDK-10852,Dependency]
Updated JIRA ISSUE:
KPSDK-15100 MCUXpresso SDK MXRT512 KSDK_2.3.0_MXRT512_RFP
<<<<<<<
>>>>>>>
Doing with [link] [KPSDK-10852,Dependency]
Updated JIRA ISSUE:
KPSDK-15079 MCUXpresso SDK MXRT512 KSDK_2.3.0_MXRT512_EAR2
<<<<<<<

**********Checking subtasks**********
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Searching Issues....
JQL: issuetype = "Sub-task" AND labels in (RR_DOC,MCU_SW_PE) AND resolution = "Unresolved" AND parent in (KPSDK-15091,KPSDK-15071,KPSDK-15108,KPSDK-15100,KPSDK-15079)
KPSDK-15123 MCUXpresso SDK MXRT512 KSDK_2.3.0_MXRT512_RFP_RC2: Deployment
KPSDK-15120 MCUXpresso SDK MXRT512 KSDK_2.3.0_MXRT512_RFP: Deployment
KPSDK-15118 MCUXpresso SDK MXRT512 KSDK_2.3.0_MXRT512_RFP_RC1: Deployment
KPSDK-15114 MCUXpresso SDK MXRT512 KSDK_V2_MXRT512_PRC1: Documentation
KPSDK-15106 MCUXpresso SDK MXRT512 KSDK_V2_MXRT512_RFP: Documentation
KPSDK-15097 MCUXpresso SDK MXRT512 KSDK_V2_MXRT512_PRC2: Documentation
KPSDK-15090 MCUXpresso SDK MXRT512 KSDK_2.3.0_MXRT512_EAR1: Deployment
KPSDK-15088 MCUXpresso SDK MXRT512 KSDK_2.3.0_MXRT512_EAR2: Deployment
KPSDK-15085 MCUXpresso SDK MXRT512 KSDK_V2_MXRT512_EAR2: Documentation
KPSDK-15077 MCUXpresso SDK MXRT512 KSDK_V2_MXRT512_EAR1: Documentation
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

*********Creating Tasks**********

*********Generating Report**********
Write resources to myrelease_issue.xlsx
Write resources to myrelease_version.xlsx
```



### Join the development

join the development by create pull request to the stash repository.  Jimmy Chen is creating the initial version and it is welcomed to fix the bugs and create more functionality basing on the jirabase modules. 

[jiracli_arch]: ./document/jiracli_arch.jpg

[create_release]: ./document/create_release.JPG

[timeline]: ./document/timeline.jpg


