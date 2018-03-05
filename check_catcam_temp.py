#! /usr/bin/env python

"""Rough draft of python implementation of the check_memory monitoring plugin. Advantage: removes need for nagios perl libs. THIS NEEDS TO BE CLEANED UP A BIT BEFORE it is anywhere near prod ready. It should work as PoC on debian with the curl util installed."""

import argparse


def parseArgs(arguments=[]):
	UNIT_OPTIONS = ["""C""", """F""", """K""", """Celsius""", """Fahrenheit""", """Kelvins"""]
	parser = argparse.ArgumentParser(description='check for CatCam temperature')
	parser.add_argument('-u', '--unit', default=UNIT_OPTIONS[0], choices=UNIT_OPTIONS, help='the units')
	parser.add_argument('-C', '--critical', default=25, help='the critical threshold. (Min. Mem.)')
	parser.add_argument('-W', '--warn', default=24, help='the warning threshold. ignored')
	parser.add_argument('-H', '--host', help='the host ip to check')
	return parser.parse_args(arguments)


def extractRegexPattern(theInput_Str, theInputPattern):
	import re
	sourceStr = str(theInput_Str)
	prog = re.compile(theInputPattern)
	theList = prog.findall(sourceStr)
	return theList


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


def main(argv=None):
	args = parseArgs(argv)
	unit = args.unit
	if isinstance(args.critical, int):
		crit_tmp = args.critical
	else:
		crit_tmp = int(args.critical, 10)
	units = 1
	the_host = args.host
	temp_c = None
	if units is not None:
		import subprocess
		import os
		try:
			theResult=subprocess.check_output(["curl", "-fsSLk", "--url", str("http://{}/?action=command&command=value_temperature").format(the_host)])
		except Exception:
			theResult = None
		if theResult is not None:
			theValues = theResult.split(" ")[-1]
			if (theValues is not None):
				if (theValues < crit_tmp):
					print(str("TEMPERATURE {}: Comfortable. | temp={};{};{};;").format("OK.", theValues, (crit_tmp - 2), crit_tmp, 100))
					exit(0)
				elif (theValues >= crit_tmp):
					print(str("TEMPERATURE {}: Uncomfortable. | temp={};{};{};;").format("CRITICAL.", theValues, (crit_tmp - 2), crit_tmp, 100))
					exit(2)
				else:
					print "TEMPERATURE UNKNOWN: No Data."
					exit(3)
			else:
				print "TEMPERATURE UNKNOWN: An Error Occured."
				exit(5)
		else:
			print "TEMPERATURE UNKNOWN: Plugin Failed."
			exit(3)
	exit(3)


if __name__ in '__main__':
	import sys
	main(sys.argv[1:])