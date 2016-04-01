#!/usr/bin/python
# Pull the temp in F, realative humid, and dew point and send to check_mk
import os
import re

output = os.popen("/home/dev@egor.betoria.dyndns.org/temphumid/TEMPered/build/utils/tempered -s Fahrenheit").read()
output2 = re.compile('\S+').findall(output)

#print output
#print output2
#print output2[7]

output3 = re.sub('[%,]', '', output2[7])
#print output3
print "0 EgorHum relhumid=%s;90;95;0;100 OK - Relative Humidity in Garage" % output3

