#!/usr/bin/env python
# simple smtp VRFY checker.. that works! 
# by brad a.

import socket
import getopt
import sys
import re


def usage():
	help = "Options:\n"
	help += "\t-h <host>\t host\n"
	help += "\t-p <port>\t port (Default: 25)\n"
	help += "\t-u <filename>\t userlist\n"
	help += "\t-v \t verbose\n"
	return help


def main():
	print "SMTP VRFY Checker"
	print "By brad a."
	print "---------------------------------"
	
        try:
                opts, args = getopt.getopt(sys.argv[1:], "h:p:u:v",[])

        except getopt.GetoptError:
                print usage()
                return
        port = 25 
        verbose = host = userlist = 0

        for o, a in opts:
                if o == "-h":
                        host = a
                if o == "-p":
                        port = int(a)
                if o == "-u":
                        userlist = a
		if o == "-v":
			verbose = 1
        if (host == 0) or (userlist == 0):
                print usage()
                return

	print "[+] Establishing connection to",host,":",port
	s = socket.socket()
	s.settimeout(10)
	recv_data = 0
	s.connect((host,port))

	banner = s.recv(512)
	if verbose == 1:
		print "[V] Banner:"
		print banner
	
	file = open(userlist,'r')
	count = 1
	for line in file:

		if count % 10 == 0:
			if verbose == 1:
				print "[V] Attempted ten usernames, reconnecting"
			s.shutdown(2) 
			s.close

			s = socket.socket()
			s.settimeout(10)
			recv_data = 0
			s.connect((host,port))

			banner = s.recv(512)
			if verbose == 1:
				print "[V] Banner:"
				print banner

		user = line.rstrip('\n')

		msg = "VRFY "
		msg += user
		msg += "\n"
		if verbose == 1:
			print "[V] Sending:",msg

		error = s.sendall(msg)
		
		if error:
			print "\n[!] Error with user",user,":", error
		else:
			try:
				recv_data = s.recv(512)
			except socket.timeout:
				print "[!] Timeout on user",user,"!"
	
		if recv_data:
#			print recv_data
			if re.match("250",recv_data):
				print "[+] Found User:",user
			if verbose == 1:
				print "[+] User:",user,
				if re.match("550",recv_data):
					print " -> Not Found!"
				else:
					print " -> Unknown Error!"
				print recv_data	
		else:
			print "\nNo recv_data!"
		count+=1

	file.close()
	s.shutdown(2)
	s.close()

main()
