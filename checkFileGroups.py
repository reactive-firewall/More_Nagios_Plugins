#! /usr/bin/env python

# default values
DEFAULT_SEARCH_ROOT='/'

import argparse
import os

parser = argparse.ArgumentParser(description='check for file count by owner')
parser.add_argument('-S', '--search', default=DEFAULT_SEARCH_ROOT, required=True, help='search path root to check')
parser.add_argument('-g', '--gid', default=os.getegid(), required=True, help='search for group owned files with this GID')
parser.add_argument('-c', '--critical', default=6000, required=False, help='critical threshold in filecount or bytes')
parser.add_argument('-w', '--warning', default=1000, required=False, help='warning threshold in filecount or bytes')
group_empty = parser.add_mutually_exclusive_group()
group_empty.add_argument('--empty-critical', default=False, action='store_true', help='return critical instead of warning on empty search path, overides cannot be combined with other reporting modes')
group_empty.add_argument('--empty-ok', default=False, action='store_true', help='return ok on empty search path instead, cannot be combined with optionals')
group_safe = parser.add_mutually_exclusive_group()
group_safe.add_argument('--unsafe', default=False, action='store_true', help='allow unsafe ranges, overides some checks cannot be combined with safe mode')
group_safe.add_argument('--only-safe', default=True, action='store_true', help='allow only safe ranges (default), force some checks cannot be combined with un-safe mode')
group_mode = parser.add_mutually_exclusive_group()
group_mode.add_argument('--count', default=True, action='store_true', help='units are in file counts, cannot be combined with size mode')
group_mode.add_argument('--size', default=False, action='store_true', help='units are in bytes used by files, cannot be combined with count mode')

args = parser.parse_args()
test_is_unsafe = args.unsafe
test_is_safe = args.only_safe
search_path = args.search
empty_is_ok = args.empty_ok
empty_is_NOT_ok = (args.empty_critical or (empty_is_ok))
critical_threshold = int(args.critical)
warning_threshold = int(args.warning)
count_mode = (args.count and (args.size != True))


try:
	search_gid = int(args.gid)
except:
	print "checkFileGroups: SYNTAX ERROR: UNKNOWN value "+str(args.gid)
	exit(3)

if search_gid is None:
	print "checkFileGroups: SYNTAX ERROR: GID can not be set to None!"
	exit(3)
elif ((search_gid < 0) and (test_is_unsafe is False)):
	print "checkFileGroups: SYNTAX ERROR: GID can not be set to negitive! try --unsafe"
	exit(3)
elif ((int(search_gid) > 2147483647) and (test_is_unsafe is False)):
	print "checkFileGroups: SYNTAX ERROR: GID "+str(search_gid)+" can not be set beyond the 32bit limit! try --unsafe"
	exit(3)

from os.path import join

#test_is_critical = args.critical
#test_is_unknown = args.empty_unknown
#test_is_inverted = args.empty_ok

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

def getSize(filename):
    st = os.stat(filename)
    return st.st_size

def getFileGID(fqfp ='.'):
	theResult = None
	try:
		stats = os.lstat(fqfp)
		theResult = stats.st_gid
	except:
		print "Unable to get GID"
	return theResult

def getFileGIDCount(theGID, searchPath='.'):
	theResult = 0
	try:
		for root, dirs, files in os.walk(searchPath, True, None, True):
			try:	
				for name in files:
					if ( theGID == getFileGID( os.path.join(root, name) ) ):
						theResult = theResult + 1;
			except:
				continue
	except:
		print "checkFileGroups UNKNOWN - "+str(searchPath)
		exit(3)
	return theResult

def getFileGIDUsage(theGID, searchPath='.'):
	theResult = 0
	try:
		for root, dirs, files in os.walk(searchPath, True, None, True):
			try:	
				for name in files:
					if ( theGID == getFileGID( os.path.join(root, name) ) ):
						theResult = theResult + getSize(str(os.path.join(root, name) ));
			except:
				continue
	except:
		print "checkFileGroups UNKNOWN - "+str(searchPath)
		exit(3)
	return theResult

if search_path is None:
	print "checkFileGroups: SYNTAX ERROR: MISSING path"
	exit(1)

if search_gid is not None:
	theCount = 0
	if count_mode:
		theCount = getFileGIDCount(search_gid, search_path)
	else:
		theCount = getFileGIDUsage(search_gid, search_path)
	if (theCount is None) or (theCount == 0):
		if empty_is_NOT_ok is True:
			print "checkFileGroups CRITICAL - 0"
			exit(2)
		if empty_is_ok is True:
			print "checkFileGroups OK - 0"
			exit(0)
		else:
			print "checkFileGroups WARNING - 0"
			exit(1)
	elif (theCount is not None) and (theCount > 0):
		if (theCount > critical_threshold) or (theCount >= warning_threshold):
			if (theCount >= critical_threshold):
				print "checkFileGroups CRITICAL - "+str(theCount)
				exit(2)
			else:
				print "checkFileGroups WARNING - "+str(theCount)
				exit(1)
		else:
			print "checkFileGroups OK - "+str(theCount)
	else:
		if empty_is_NOT_ok is True:
			print "checkFileGroups CRITICAL - "+str(theCount)
			exit(2)
		if empty_is_ok is True:
			print "checkFileGroups OK - "+str(theCount)
			exit(0)
		else:
			print "checkFileGroups WARNING - "+str(theCount)
			exit(1)
else:
	print "ARP UNKNOWN"
	exit(3)
exit(0)
