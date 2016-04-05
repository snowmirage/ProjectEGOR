#!/usr/bin/python

import subprocess
import sys

host = "192.168.0.40"
keyfile = "/home/dev@egor.betoria.dyndns.org/powerpc_id_rsa"
command = "sysctl -a | egrep -E \"cpu\.[0-9]+\.temp\""

# ssh part
#http://python-for-system-administrators.readthedocs.org/en/latest/ssh.html


ssh = subprocess.Popen(["ssh", "-i", keyfile, "powerpc@%s" % host, command],
	shell=False,
	stdout=subprocess.PIPE,
	stderr=subprocess.PIPE)
result = ssh.stdout.readlines()
if result == []:
	error = ssh.stderr.readlines()
	print >>sys.stderr, "ERROR: %s" % error
else:
	#print result


# here's the output
#[powerpc@oliver ~]$ sysctl -a |egrep -E "cpu\.[0-9]+\.temp"
#dev.cpu.0.temperature: 41.0C
#dev.cpu.1.temperature: 39.0C
#dev.cpu.2.temperature: 42.0C
#dev.cpu.3.temperature: 39.0C
#dev.cpu.4.temperature: 36.0C
#dev.cpu.5.temperature: 31.0C
#dev.cpu.6.temperature: 36.0C
#dev.cpu.7.temperature: 35.0C

	cputemps = []

	for c in result:
		t=c.split()
		#print t[1]
		#print t[1].replace("C", "")
		cputemps.append(t[1].replace("C", ""))

#print cputemps

print "0 FreenasTemp core0=%s;85;95;0;100|core1=%s;85;95;0;100|core2=%s;85;95;0;100|core3=%s;85;95;0;100|core4=%s;85;95;0;100|core5=%s;85;95;0;100|core6=%s;85;95;0;100|core7=%s;85;95;0;100 OK - Temp of all 8 cores on freenas" % (cputemps[0], cputemps[1], cputemps[2], cputemps[3], cputemps[4], cputemps[5], cputemps[6], cputemps[7])

