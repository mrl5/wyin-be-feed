## Purpose

The script runs history/get/event and (if chosen) history/get/events action for set of time values. In ./logs folder, it creates log file and if any request status code differ than 200 an error_log file. It can be used to run a regression tests.

## Prerequisites

wyin-be-feed must be built and run in a docker.

## Running a script

Open console in wyin-be-feed/scripts folder and run
```
./regression.sh
```

## Parameters -port, -events, -values

Without any parameters, script uses port 8080 and default time values written in time_array variable. To run some specific conditions, use parameters.

## -port

To change the port number value, use parameter -port and set a new value. This parameter is optional, but it must be first in a commend line
```
./regression.sh -port 8080
```

## get/event, get/events or both endpoints

In default script runs get/event endpoint. To switch it for get/events use param:
```
./regression.sh -events
```
To run both endpoints, use param:
```
./regression.sh -both
```

## Values

To run script for all hour [00:00-23:59] use parameter:
```
./regression.sh -all_hours
```
To run script for all values without years from the future, use parameter:
```
./regression.sh -real_hours
```

For running script with chosen values, use parameter -type_hours and list values in notation HH:MM separated with space:
```
./regression.sh -type_hours 00:20 01:20 03:59
```

## Interruption

To interrupt running script press CTRL+'C'

## Regression2.sh

It can be run in local git bash window
```
./regression2.sh
```

It needs a directory ./logs to create logs in.

Range of years can be changed inside the script inside for loop
```
for i in {<starting_value>..<ending_value>}
```
