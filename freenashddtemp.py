#!/usr/bin/python

import subprocess
import sys

host = "192.168.0.40"
keyfile = "/home/powerpc/.ssh/id_rsa"
command1 = "sysctl -n kern.disks"


ssh = subprocess.Popen(["ssh", "-i", keyfile, "powerpc@%s" % host, command1],
    shell=False,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
hdd = ssh.stdout.readlines()
if hdd == []:
    error = ssh.stderr.readlines()
    print >>sys.stderr, "ERROR: %s" % error
else:
    print hdd
    something = 1

hddlist = hdd.split()


for i in hddlist:
    print "In for loop"
    if i != "da19" and i != 'da18':
        print "in if statement"
        command2 = "smartctl -a /dev/" + str(i) + " | awk '/Temperature_Celsius/{print $0}' | awk '{print $10 \"C\"}'"
        print "The command to run is ------ " + command2 + " --------"
        #           smartctl -a /dev/$i | awk '/Temperature_Celsius/{print $0}' | awk '{print $10 "C"}'
        ssh = subprocess.Popen(["ssh", "-i", keyfile, "powerpc@%s" % host, command2],
                               shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        hddtemp = ssh.stdout.readlines()
        if hddtemp == []:
            error = ssh.stderr.readlines()
            print >> sys.stderr, "ERROR: %s" % error
        else:
            print hddtemp



# print "0 FreenasTemp core0=%s;150;165;0;200|core1=%s;150;165;0;200|core2=%s;150;165;0;200|core3=%s;150;165;0;200|core4=%s;150;165;0;200|core5=%s;150;165;0;200|core6=%s;150;165;0;200|core7=%s;150;165;0;200 OK - Temp of all 8 cores on freenas" % (cputempsF[0], cputempsF[1], cputempsF[2], cputempsF[3], cputempsF[4], cputempsF[5], cputempsF[6], cputempsF[7])

# THIS ######
# echo "HDD temp :"
# for i in $(sysctl -n kern.disks)
# do
#         DevTemp=`smartctl -a /dev/$i | awk '/Temperature_Celsius/{print $0}' | awk '{print $10 "C"}'`
#         DevSerNum=`smartctl -a /dev/$i | awk '/Serial Number:/{print $0}' | awk '{print $3}'`
#         DevName=`smartctl -a /dev/$i | awk '/Device Model:/{print $0}' | awk '{print $3}'`
#         echo $i $DevTemp $DevSerNum $DevName
# done
#
# Should give you THIS ######
# HDD temp :
# ada7 26C S2H7J9AB807313 SAMSUNG
# ada6 28C S2H7J9AB807309 SAMSUNG
# ada5 28C S2H7J9AB807310 SAMSUNG
# ada4 29C S2H7J1BB208475 SAMSUNG
# ada3 37C 5XW1J1S1 ST32000542AS
# ada2 39C 5XW1EXHR ST32000542AS
# ada1 41C 5YD5RZNG ST2000DL003-9VT166
# ada0 45C WD-WCAVY2756609 WDC
# da0