#!/usr/bin/python
# This will live in the local checks folder for check_mk and should out put check_mk formated info on the power draw of the UPS

import time
import sys
import os
#output needs to be the following (each line is a desciption of the column)
#Status                  0 OK 1 WARNING 2 CRITICAL 3 UNKNOWN
#Item Name               nagios service desciption
#Performance data        varname=value;warn;crit;min;max
#Check ouput             the output of the check will be displayed in nagios

#thats 4 columns

#see https://mathias-kettner.de/checkmk_localchecks.html

#Set some variables



now=time.strftime("%Y/%m/%d/%I/%M/%S")          #get the current date + time when this script started, need to adjust this to match format of log file
status=3                #set status to 3 "unknown" to start
perfdata=""             #set perfdata to null to start
output="NOTSET" #set output string to "NOTSET" to start


# Determine the status
# Logic - In our log file we should find enteries every second. If we find consecutive enteries for the last 60 seconds
# there isn't a problem, and status should return OK (aka 0).  If we find less than 60 for the last 60 seconds, or if
# any are missing then WARNING (aka 1).  If we don't find any for the last 60 seconds then CRITICAL (aka 2)

# Open the file stream
#with open(filename, 'r') as fh
#       all_lines = fh.readlines()

# Test stuff
#print "now is set to"
#print now
#print "all_lines"
#print all_lines
watts = os.popen("pwrstat -status | sed '17q;d' | awk -F' ' '{print $2}'").read()
watts2 = watts.replace('\n', '')
#print "watts is set to", watts, "\n"
print "0 EgorWattsUsed watts=%s;900;1000;0;1200 OK - actuall wall watts is about 25 more" % watts2#egorpower.py
