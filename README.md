# Maui Smart Grid Project #

[Daniel Zhang (張道博)](http://www.github.com/dz1111), Software Engineer

## Overview ##

The University of Hawaii at Manoa was tasked with maintaining a data repository for use by analysts for the [Maui Smart Grid](http://www.mauismartgrid.com) energy sustainability project through the [Hawaii Natural Energy Institute](http://www.hnei.hawaii.edu). This software provides the data processing and operational resources necessary to accomplish this task. Source data arrives in multiple formats including XML, tab-separated values, and comma-separated values. Issues for this project are tracked at the [Hawaii Smart Energy Project YouTRACK instance](http://smart-energy-project.myjetbrains.com/youtrack/rest/agile/).

### Software Features ###

* Open-source (BSD license) code in Python 2.7x.
* Parsing of source data is provided for multiple formats.
* Insertion of data to a data store (PostgreSQL 9.1) is performed automatically.
* Source files to recreate the structure of the data store are available.
* Unit testing of data processing operations is provided by a test suite implemented through Python's `unittest`.
* Data operations are reported using email notifications including plots as graphic summaries.

### Project Documentation ###

Documentation is maintained as docstrings within the source code files with the intention of conforming to the reStructuredText format. There is also a [GitHub-based wiki](https://github.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/wiki).

## Implementation ##

The code is written in Python 2.7x. It has a testing suite implemented through `unittest`.

The database schema is illustrated in `docs/meco-direct-derived-schema-v3.pdf`.

Data parsing is performed by the ElementTree XML parser. Data store operations are implemented through the psycopg2 PostgreSQL library.

Data processing involves inserting nested sets of data linked by their primary keys, generated as sequential integer values, of the preceding table. Foreign keys are determined by a separate class that holds the last primary key used for each table. The design for this feature is illustrated in `docs/fk-value-determiner.pdf`.

### Database Schema ###

A SQL dump, produced by `pg_dump`, of the database schema is provided for reference only.

The schema consists of the following components.

1. MECO Energy Data
2. MECO Event Data
3. MECO Location Records (deprecated)
4. MECO Meter Records (deprecated)
5. MECO Meter Location History
9. MECO Egauge Energy Data
6. NOAA Weather Data (Kahului Station)
7. Circuit Data
8. Transformer Data
10. Irradiance Data
11. PV Service Points

A [helpful schema diagram](https://github.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/raw/master/diagrams/meco-direct-derived-schema-v3.pdf) is provided in the repository and a version is displayed here illustrating the portion of the schema derived from MECO export data.

![MECO Derived Schema](https://raw.github.com/Hawaii-Smart-Energy-Project/maui-smart-grid/master/diagrams/meco-direct-derived-schema-v3.png)

#### Database Version History ####

v1
: Initial data insertion from first exports. This version is deprecated.

v2
: Eliminated duplicates in the Reading branch by filtering on meter name, interval end time, and channel.

v3 (Production)
: Retroactively adding event data. Duplicate records exist in the Event branch and the Register branch.

v4 (Development)
: Will address duplicates in the Event branch and the Register branch. To include updated weather data.

![MECO Derived Schema](https://raw.github.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/diagrams/2013-07-29_ReadingAndMeterCounts.png)
Plot of readings per meter counts and meter counts per day loaded to meco_v3.

## Installation ##

The software distribution archive is in tar gz format and can be extracted using

    $ tar -zxvf Maui-Smart-Grid-1.0.tar.gz

### Software Dependencies ###

The software has the following dependencies and they can be satisfied through various methods. During development, `pip` was used to install third-party modules.

#### Python Modules Not in the Standard Library ####

* dateutil
* matplotlib
* psycopg2
* pycurl
* pylab

### Python-Based Scripts and Modules ###

> __WARNING: The Python-based installer is not yet fully working.__

The Python-based scripts and modules have their installer implemented through `distutils`. They can be installed using

	$ python setup.py install --home=~/Maui-Smart-Grid-1.0

This example demonstrates installing to a user directory which is sometimes preferred over installing to a system-wide path. For this example, the `PYTHONPATH` environment variable should be set using something like

	$ export PYTHONPATH=~/Maui-Smart-Grid-1.0/lib/python

where this example is specific to bash or sh.

### MSG eGauge Service ###

The MSG eGauge Service is installed separately from the rest of the system and uses its own installer in `/src/msg-egauge-service`.

Here's an example installation command.

	$ sudo perl {$PATH_TO_INSTALLER}/installEgaugeAutomaticDataServices.pl

The install script, `/src/msg_egauge_service/installEgaugeAutomaticDataServices.pl`, should be edited to set the install paths as the installer is not as sophisticated as the Python installer. The installer will work if invoked from other paths and does not have to be run from the path containing the source files.

## Distribution ##

The distribution archive is created using

	$ python setup.py sdist

## Configuration ##

All of the site-specific options are intended to be held in text-based configuration files. 

The software is configured through a text configuration file contained in the user's home directory. The file is named `~/.msg-data-operations.cfg`. Permissions should be limited to owner read/write only. It is read by the `ConfigParser` module.

### Example Main Configuration File Content ###

The reference template can be found in `config/sample-dot-msg-data-operations.cfg.`

    [Debugging]
    debug=False
    limit_commits=False
    
    [Data Paths]
    plot_path=${PLOT_PATH}
    
    [Executable Paths]
    bin_path=${MECO_BIN_DIR}
    
    [Notifications]
    email_fromaddr=${EMAIL_ADDRESS}
    email_username=${EMAIL_USERNAME}
    email_password=${EMAIL_PASSWORD}
    email_recipients=${COMMA_SEPARATED_EMAIL_RECIPIENTS}
    testing_email_recipients=${COMMA_SEPARATED_EMAIL_RECIPIENTS}
    email_smtp_server=${SMTP_SERVER_AND_PORT}
    
    [Weather Data]
    
    ## Example URL: http://cdo.ncdc.noaa.gov/qclcd_ascii/
    weather_data_url=${WEATHER_DATA_URL}
    
    ## Example pattern: <A HREF=".*?">(QCLCD(201208|201209|201210|201211|201212|2013).*?)</A>
    weather_data_pattern=${WEATHER_DATA_PATTERN}
    
    weather_data_path=${WEATHER_DATA_PATH}
    
    [Database]
    db_password=${PASSWORD}
    db_host=${IP_ADDRESS_OR_HOSTNAME}
    db_port=${DB_PORT}
    db_username=${DB_USERNAME}

    ## The name of the database that will be used by automated operations.
    db_name=${DB_NAME}
    
    ## The name of the databased used for testing operations.
    testing_db_name=${TESTING_DB_NAME}
    
    [Hardware]
    multiprocessing_limit = ${MULTIPROCESSING_LIMIT}

### MSG eGauge Service Configuration ###

The following is an example of the configuration file used for configuring the MSG eGauge Service. This file is installed at `/usr/local/msg-egauge-service/config/egauge-automatic-data-services.config`.

    msg_dbname = "${DATABASE_NAME}"
    data_dir = "${DATA_DOWNLOAD_PATH}"
    insert_table = "\"${TABLE_NAME}\""
    loaded_data_dir = "${DATA_ALREADY_LOADED_PATH}"
    invalid_data_dir = "${DATA_PATH_FOR_INVALID_DATA_STORAGE}"
    db_pass = "${DB_PASSWORD}"
    db_user = "${DB_USERNAME}"
    db_host = "${DB_HOST}"
    db_port = "${DB_PORT}"
    
    egauge_user = "${EGAUGE_USERNAME}"
    egauge_password = "${EGAUGE_PASSWORD}"
    
    egauge = ${EGAUGE_ID_1}
    egauge = ${EGAUGE_ID_2}
    egauge = ${EGAUGE_ID_3}

### Database Configuration ###

The database schema can be installed using the following command form where `${DATABASE_NAME}` is a valid database.

    $ psql ${DATABASE_NAME} < ${DATABASE_STRUCTURE}.sql

## Software Operation ##

### Inserting MECO Energy Data from Source XML ###

The exported XML data files contain the energy data. Insertion to the database is performed by running

    $ time python -u ${PATH_TO_SCRIPT}/insertMECOEnergyData.py --email > insert-log.txt
    
in the directory where the data files are contained. The use of `time` is for informational purposes only and is not necessary. Redirecting to `insert-log.txt` is also unneeded but reduces the output to the short form.

#### Sample Output of Data Insertion ####

MECO data is inserted using

    $ insertMECOEnergyData.py --email > insert-run.log 

The output looks like the following and is the concise log output for data loading.
    
    Inserting data to database meco_v3.
    
    3:{0rd,0re,0ev}(0)[3440]<2688rd,56re,0ev,3440,3440>*3:{0rd,0re,0ev}(1)[6880]<2688rd,56re,0ev,
    3440,6880>*3:{0rd,0re,0ev}(2)[10320]<2688rd,56re,0ev,3440,10320>*3:{0rd,0re,0ev}(3)[13760]<2688rd,
    56re,0ev,3440,13760>*3:{0rd,0re,0ev}(4)[20651]<5376rd,112re,10ev,6891,20651>*3:{0rd,0re,0ev}(5)
    [24091]<2688rd,56re,0ev,3440,24091>*3:{0rd,0re,0ev}(6)[27531]<2688rd,56re,0ev,3440,27531>*3:{0rd,0re,
    0ev}(7)[30971]<2688rd,56re,0ev,3440,30971>*3:{0rd,0re,0ev}(8)[37854]<5376rd,112re,2ev,6883,37854>*3:{0rd,
    0re,0ev}(9)[41294]<2688rd,56re,0ev,3440,41294>*3:{0rd,0re,0ev}(10)[44734]<2688rd,56re,0ev,3440,44734>*
    ...
    ---3:{0rd,0re,0ev}(44)[166400]<129024rd,2891re,1019ev,NA,166400>*

Individual processes are denoted by a number and a colon. The numbers in brackets correspond to {dropped duplicates in the reading branch, register branch or the event branch)}, (reading group index), and [element count]. The duplicate count is discrete by group. The element count is cumulative over the data set. 

Dropped reading duplicates are the duplicate entries---determined by meter name, interval end time, and channel number---that are present in the source data. The reading group index is an integer count of the distinct groups of energy readings (MeterData record sets) in the source data. The element count refers to the individual elements within the source data.

Angled brackets contain counts of actual records inserted for each of the branches. They also contain group counts as well as a cumulative count.

The stars (*) indicate when commits are performed.

A final summary report follows the `---` symbol.

Parallel data loading is supported since loading is performed atomically, database commits are made after data verification including taking duplicate records into account.
  
### Testing Mode
The database insertion scripts have a separate testing mode that can be activated using the `--testing` command-line option. When testing mode is enabled, database operations will be performed on the testing database as defined in the site configuration file. Additionally, operations such as notifications will be directed to their appropriate testing mode settings. For example, email notifications will be delivered to testing mode recipients instead of the primary distribution list.

### Inserting Location and Meter Records (DEPRECATED) ###

Location and meter records are stored in separate tab-separated files and are inserted using separate scripts.

    $ insertLocationRecords.py ${FILENAME}

    $ insertMeterRecords.py ${FILENAME}
    
These scripts and their associated data are deprecated in favor of the Meter Location History (MLH).

### Inserting NOAA Weather Data (Kahului Airport Station WBAN 22516) ###

Weather data loading is a two-stage process involving retrieval and insertion.

Retrieval is performed using

    $ retrieveNOAAWeatherData.py
     
Insertion is performed using

    $ insertCompressedNOAAWeatherData.py --email
    
and supports recursive data processing of a set of files from the current directory. Weather data loading supports notifications.

### Utility Scripts ###

`grantAllPermissionsToDatabase.sh ${DATABASE}`
: Set appropriate group permissions to databases.

### MSG eGauge Service Operation ###

Initial loading of eGauge energy data can take a longer time than follow-up data loading. It is also more prone to error conditions as it is processing a much larger data set.

Data exists in three possible states:

1. Data that has been downloaded but not yet loaded.
2. Valid data that has been loaded.
3. Invalid data that cannot be loaded.

There are three corresponding directories that are used to maintain the files for the data in these different states. The paths for these directories are defined in the MSG eGauge Service Configuration.

#### Invalid Data ####

Data downloads are not always able to be completed resulting in invalid data being saved. When this situation occurs, it may be necessary to manually intervene by manually pruning the invalid data. This condition can be recognized when there exists a mismatched number of data values to the data columns. Database operations will not be able to complete when the data is in this state. Data that is not able to be loaded is archived to the invalid data path. It is recommended that this storage be occassionally purged as **invalid data only pertains to the time period between that which was last loaded and the most recent data available.** It is not automatically deleted in case it is needed for reference.

## Notifications ##

Notification of the results of data processing events is provided by the **MSG Notification System**. Notifications are distributed by email to a predefined recipient list (comma-separated) contained in the configuration file.

### Example Notification for Data Loading ###

    Recursively inserting data to the database named meco_v3.
    Starting in /msg-data/2013_07_10
    insertScript = insertMECOEnergyData.py
    
    ./20130710-99bb8b2b-12a1-4db5-8a1c-7312277cf404-1-1.xml.gz
    
    Inserting data to database meco_v3.
    
    Parsing XML in ./20130710-99bb8b2b-12a1-4db5-8a1c-7312277cf404-1-1.xml.gz.
    {0rd,0re,0ev}(0)[8869]<6912rd,144re,24ev,8869,8869>*{0rd,0re,0ev}(1)[13291]<3456rd,72re,0ev,4422,13291>*{0rd,0re,0ev}(2)[17713]<3456rd,72re,0ev,4422,17713>*{0rd,0re,0ev}(3)[26566]<6912rd,144re,8ev,8853,26566>*{0rd,0re,0ev}  ...  ---{0rd,0re,0ev}(37)[191467]<0rd,0re,0ev,0,191459>*
    
    Wall time = 512.54 seconds.
    
    Log Legend: {} = dupes, () = element group, [] = process for insert elements, <> = <reading insert count, register insert count, event insert count, group insert count,total insert count>, * = commit
    rd = reading, re = register, ev = event
    
    Processed file count is 1.
    
    Plot is attached.
    
The final group, after the `---`, is a summary report of the operations performed.

## License ##

Copyright (c) 2013, University of Hawaii Smart Energy Project  
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of the University of Hawaii at Manoa nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.