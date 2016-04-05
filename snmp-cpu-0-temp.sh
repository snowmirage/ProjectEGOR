#!/bin/sh
if [ "$1" = "-g" ]
then
echo .1.3.6.1.2.6453.25.1.0
echo gauge
sysctl -a | egrep -E "cpu\.0+\.temp" | awk '{print $2}' | cut -c 1,2,4
fi
exit 0
