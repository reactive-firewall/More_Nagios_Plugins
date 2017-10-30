#! /usr/bin/env python


# default values
DEFAULT_MAC_ADDR = str("""ff:ff:ff:ff:ff:ff""")
"""The Default MAC address to check is all one bits, i.e. broadcast address."""

import argparse


def parseArgs(arguments=None):
	parser = argparse.ArgumentParser(description='check for an arp entry')
	parser.add_argument('-M', '--mac', default=DEFAULT_MAC_ADDR, help='check for an exact MAC')
	parser.add_argument('-H', '--host', required=True, help='check for an exact IP')
	group_empty = parser.add_mutually_exclusive_group()
	group_empty.add_argument('-C', '--critical', default=False, action='store_true', help='return critical instead of warning on empty MAC, overides other empty values')
	group_empty.add_argument('-U', '--empty-unknown', default=False, action='store_true', help='return unknown instead of warning on empty MAC')
	group_empty.add_argument('--empty-ok', default=False, action='store_true', help='return ok on empty MAC instead, cannot be combined with optionals')
	return parser.parse_args(arguments)


def readFile(somefile):
	import os
	read_data = None
	theReadPath = str(somefile)
	with open(theReadPath, 'r') as f:
		read_data = f.read()
	f.close()
	return read_data


def extractRegexPattern(theInput_Str, theInputPattern):
	import re
	sourceStr = str(theInput_Str)
	prog = re.compile(theInputPattern)
	theList = prog.findall(sourceStr)
	return theList


def extractMACAddr(theInputStr):
	return extractRegexPattern(theInputStr, "(?:(?:[[:print:]]*){0,1}(?P<Mac>(?:(?:[0-9a-fA-F]{1,2}[\:]{1}){5}(?:[0-9a-fA-F]{1,2}){1}){1})+(?:[[:print:]]*){0,1})+")


def compactList(list, intern_func=None):
   if intern_func is None:
       def intern_func(x): return x
   seen = {}
   result = []
   for item in list:
       marker = intern_func(item)
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result


def main(argv=[]):
	args = parseArgs(argv)
	test_MAC = (args.mac).lower()
	if (test_MAC is None):
		print("check_arp: SYNTAX ERROR: MAC can not be set to None!")
		exit(3)
	test_IP = args.host
	test_is_critical = args.critical
	test_is_unknown = args.empty_unknown
	test_is_inverted = args.empty_ok
	if test_IP is not None:
		import subprocess
		theResult=subprocess.check_output(["arp", "-n", test_IP])
		if theResult is not None:
			theMAC = extractMACAddr(theResult)
			if (theMAC is None) and (len(theMAC) is 0):
				# too complex move to function
				if test_is_critical is True:
					print "ARP CRITICAL - "+str(theMAC)
					exit(2)
				if test_is_unknown is True:
					print "ARP UNKNOWN - "+str(theMAC)
					exit(3)
				if test_is_inverted is True:
					print "ARP OK - "+str(theMAC)
					exit(0)
				else:
					print "ARP WARNING - "+str(theMAC)
				exit(1)
			elif (theMAC is not None) and (len(theMAC) > 0) and (theMAC[0] is not None):
				if (test_MAC != DEFAULT_MAC_ADDR) and (len(test_MAC) > 0) and (str(theMAC[0]).lower() != test_MAC):
					# too complex move to function
					if test_is_critical is True:
						print "ARP CRITICAL - "+str(theMAC)
						exit(2)
					if test_is_unknown is True:
						print "ARP UNKNOWN - "+str(theMAC)
						exit(3)
					if test_is_inverted is True:
						print "ARP OK - "+str(theMAC)
						exit(0)
					else:
						print "ARP WARNING - "+str(theMAC)
						exit(1)
				else:
					print "ARP OK - "+str(theMAC[0])
			else:
				# too complex move to function
				if test_is_critical is True:
					print "ARP CRITICAL - EMPTY"
					exit(2)
				if test_is_unknown is True:
					print "ARP UNKNOWN"
					exit(3)
				if test_is_inverted is True:
					print "ARP OK - EMPTY"
					exit(0)
				else:
					print "ARP WARNING - EMPTY"
					exit(1)
		else:
			print "ARP UNKNOWN"
			exit(3)
	exit(0)


if __name__ in '__main__':
	import sys
	main(sys.argv[1:])

