#!/usr/bin/python
# Pull the temp in F of the outside from weather.com
import os
import re
import pywapi

weather_com_result = pywapi.get_weather_from_weather_com('USMD0112:1:US')
tempc = weather_com_result['current_conditions']['temperature']
#print "The current temp in C is: " + str(tempc)
tempf = 9.0/5.0*float(tempc)+32
#print "The current temp in F is: " + str(tempf)
print "0 EgorOutSideTemp tempf=%s;85;95;-50;120 OK - Temp outside in F" % tempf
