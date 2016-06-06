#!/usr/bin/python

import subprocess
import sys

host = "192.168.0.40"
keyfile = "/home/powerpc/.ssh/id_rsa"
command1 = "sysctl -n kern.disks"


ssh = subprocess.Popen(["ssh", "-i", keyfile, "powerpc@%s" % host, command],
	shell=False,
	stdout=subprocess.PIPE,
	stderr=subprocess.PIPE)
result = ssh.stdout.readlines()
if result == []:
	error = ssh.stderr.readlines()
	print >>sys.stderr, "ERROR: %s" % error
else:
	print result


# print "0 FreenasTemp core0=%s;150;165;0;200|core1=%s;150;165;0;200|core2=%s;150;165;0;200|core3=%s;150;165;0;200|core4=%s;150;165;0;200|core5=%s;150;165;0;200|core6=%s;150;165;0;200|core7=%s;150;165;0;200 OK - Temp of all 8 cores on freenas" % (cputempsF[0], cputempsF[1], cputempsF[2], cputempsF[3], cputempsF[4], cputempsF[5], cputempsF[6], cputempsF[7])


