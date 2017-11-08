#! /usr/bin/env python

"""Rough draft of python implementation of the check_memory monitoring plugin. Advantage: removes need for nagios perl libs. THIS NEEDS TO BE CLEANED UP A BIT BEFORE it is anywhere near prod ready. It should work as PoC on debian with the free util installed. check back later for polished revisions."""

import argparse

UNIT_OPTIONS = ["""b""", """bytes""", """K""", """kilobytes""", """M""", """megabytes""", """G""", """gigbytes"""]
parser = argparse.ArgumentParser(description='check for an arp entry')
parser.add_argument('-u', '--unit', default=UNIT_OPTIONS[0], choices=UNIT_OPTIONS, help='the units')
parser.add_argument('-C', '--critical', default=100, help='the critical threshold. (Min. Mem.)')
parser.add_argument('-W', '--warn', default=1000, help='the warning threshold. ignored')
parser.add_argument('-U', '--no-warn-on-used', dest='no_warn_used', default=True, action='store_false', help='ignores the warning on used < free.')

def extractRegexPattern(theInput_Str, theInputPattern):
	import re
	sourceStr = str(theInput_Str)
	prog = re.compile(theInputPattern)
	theList = prog.findall(sourceStr)
	return theList

def extractMemoryAddr(theInputStr):
	return extractRegexPattern(theInputStr, "(?:(?:[^0-9\n]+)(?P<Total_Memory>[0-9]+){1}(?:[^0-9\n]+)(?P<Used_Memory>[0-9]+){1}(?:[^0-9\n]+)(?P<Free_Memory>[0-9]+){1}(?:[^\n]+)*)")

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


args = parser.parse_args()
unit = args.unit
test_used = args.no_warn_used
if isinstance(args.critical, int):
	crit_mem = args.critical
else:
	crit_mem = int(args.critical, 10)
units = 1
if unit.lower() in u'bytes':
	units = 1
elif unit.lower() in u'kilobytes':
	units = 1024
elif unit.lower() in u'megabytes':
	units = (1024 * 1024)
elif unit.lower() in u'gigbytes':
	units = (1024 * 1024 * 1024)
elif unit.lower() in u'terabytes':
	units = (1024 * 1024* 1024 * 1024)
else:
	print(str("UNKNOWN, - Unit must be one of 'b', 'K', 'M' 'G' or 'T'."))
	exit(3)


if units is not None:
	import subprocess
	try:
		theResult=subprocess.check_output(["free", str("-{}").format(str(unit.lower())[0])])
	except Exception:
		theResult = None
	if theResult is not None:
		theValues = extractMemoryAddr(theResult)
		if (theValues is not None):
			total_mem = 0
			used_mem = 0
			free_mem = 0
			for total_mem_i, used_mem_i, free_mem_i in theValues:
				total_mem = total_mem + (int(total_mem_i, 10) * units)
				used_mem = used_mem + (int(used_mem_i, 10) * units)
				free_mem = free_mem + (int(free_mem_i, 10) * units)
			if (free_mem > crit_mem) and (((free_mem >= used_mem) and (test_used is True)) or test_used is False):
				print(str("MEMORY {} | free={};{};{};0;{}").format("OK.", free_mem, used_mem, crit_mem, total_mem))
				exit(0)
			elif (free_mem < crit_mem):
				print(str("MEMORY {} | free={};{};{};0;{}").format("CRITICAL. OOM.", free_mem, used_mem, crit_mem, total_mem))
				exit(2)
			elif (free_mem <= crit_mem) or ((free_mem <= used_mem) and (test_used is True)):
				print(str("MEMORY {} | free={};{};{};0;{}").format("WARNING. Low MEMORY.", free_mem, used_mem, crit_mem, total_mem))
				exit(1)
			else:
				print "MEMORY UNKNOWN"
				exit(3)
		else:
			print "MEMORY UNKNOWN. An Error Occured."
			exit(5)
	else:
		print "MEMORY UNKNOWN"
		exit(3)
exit(3)