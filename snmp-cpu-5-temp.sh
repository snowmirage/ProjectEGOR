#!/bin/sh
if [ "$1" = "-g" ]
then
echo .1.3.6.1.2.6453.25.1.5
echo gauge
sysctl -a | egrep -E "cpu\.5+\.temp" | awk '{print $2}' | cut -c 1,2,4
fi
exit 0
