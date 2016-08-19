#! /usr/bin/env python

# default values
#DEFAULT_MAC_ADDR='ff:ff:ff:ff:ff:ff'

import argparse

parser = argparse.ArgumentParser(description='check for a space weather data entry')
parser.add_argument('--k-wing', default=False, action='store_true', help='check the k-wing index')
#parser.add_argument('-M', '--mac', default=DEFAULT_MAC_ADDR, help='check for an exact MAC')
#parser.add_argument('-H', '--host', required=True, help='check for an exact IP')
#group_empty = parser.add_mutually_exclusive_group()
#group_empty.add_argument('-C', '--critical', default=False, action='store_true', help='return critical instead of warning on empty MAC, overides other empty values')
#group_empty.add_argument('-U', '--empty-unknown', default=False, action='store_true', help='return unknown instead of warning on empty MAC')
#group_empty.add_argument('--empty-ok', default=False, action='store_true', help='return ok on empty MAC instead, cannot be combined with optionals')

def readFile(somefile):
	import os
	read_data = None
	theReadPath = str(somefile)
	try:
		with open(theReadPath, 'r') as f:
			read_data = f.read()
		f.close()
	except:
		try:
			f.close()
		except:
			return False
		return read_data
	return read_data

def writeFile(somefile, somedata):
	import os
	theWritePath = str(somefile)
	try:
		with open(theWritePath, 'r+') as f:
			read_data = f.write(somedata)
		f.close()
	except:
		try:
			f.close()
		except:
			return False
		return False
	return True

def getRemoteData(someURL, outFile):
	"""Downloads the given URL data to the given file"""
	import urllib
	tempfile = urllib.FancyURLopener()
	tempfile.retrieve(someURL, outFile)
	return True

def getRemoteKWingData(outfile):
	"""Downloads the space weather k-wing data to the given file"""
	theResult = getRemoteData('http://services.swpc.noaa.gov/text/wing-kp.txt', outfile)
	return theResult

# make py-regex simpler
def extractRegexPattern(theInput_Str, theInputPattern):
	import re
	sourceStr = str(theInput_Str)
	prog = re.compile(theInputPattern)
	theList = prog.findall(sourceStr)
	return theList

# get timestamps from file
def extractTimes(theInputStr):
#	return extractRegexPattern(theInputStr, "(?:(?:[\s\S]*){0,1}(?P<Timestamp>(?:[19|20]{2}[0-9]{2}\s+[0-2]{1}[0-9]{1}\s+(?:01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31)\s+(?:00|01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24){1}(?:00|15|30|45){1})+)+(?:[\s\S]*){0,1})")
	return extractRegexPattern(theInputStr, "(?P<Timestamp>(?:[19|20]{2}[0-9]{2}\s+[0-2]{1}[0-9]{1}\s+(?:01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31)\s+(?:00|01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24){1}(?:00|15|30|45){1})+)+")[-2]

#def extractLastLine(theInputStr):

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
	
args = parser.parse_args()
test_k_wing = (args.k_wing is not False)
if (test_k_wing is True):
	print(str("START"))
	import os
	tmpName=str('/tmp/k_wing_data.txt')
	if (os.path.isfile(tmpName) is not True):
		getRemoteKWingData(tmpName)
	print(extractTimes(readFile(tmpName)))
	print(str("END"))
else:
	print "check_space_weather: SYNTAX ERROR: MAC can not be set to None!"
	exit(3)

#test_IP = args.host
#test_is_critical = args.critical
#test_is_unknown = args.empty_unknown
#test_is_inverted = args.empty_ok


exit(0)
