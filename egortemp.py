#!/usr/bin/python
# Pull the temp in F, realative humid, and dew point and send to check_mk
import os
import re

output = os.popen("/home/dev@egor.betoria.dyndns.org/temphumid/TEMPered/build/utils/tempered -s Fahrenheit").read()
output2 = re.compile('\S+').findall(output)

#print output
#print output2
#print output2[3]
print "0 EgorTemp tempf=%s;85;95;0;115 OK - Temp of Garage in F" % output2[3]
