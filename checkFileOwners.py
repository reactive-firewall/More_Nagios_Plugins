#! /usr/bin/env python

# default values
DEFAULT_SEARCH_ROOT='/'

import argparse
import os

parser = argparse.ArgumentParser(description='check for file count by owner')
parser.add_argument('-S', '--search', default=DEFAULT_SEARCH_ROOT, required=True, help='search path root to check')
parser.add_argument('-u', '--uid', default=os.geteuid(), required=True, help='search for user owned files with this UID')
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
	search_uid = int(args.uid)
except:
	print "checkFileOwners: SYNTAX ERROR: UNKNOWN value "+str(args.uid)
	exit(3)

if search_uid is None:
	print "checkFileOwners: SYNTAX ERROR: UID can not be set to None!"
	exit(3)
elif ((search_uid < 0) and (test_is_unsafe is False)):
	print "checkFileOwners: SYNTAX ERROR: UID can not be set to negitive! try --unsafe"
	exit(3)
elif ((int(search_uid) > 2147483647) and (test_is_unsafe is False)):
	print "checkFileOwners: SYNTAX ERROR: UID "+str(search_uid)+" can not be set beyond the 32bit limit! try --unsafe"
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

def getFileUID(fqfp ='.'):
	theResult = None
	try:
		stats = os.lstat(fqfp)
		theResult = stats.st_uid
	except:
		print "Unable to get UID"
	return theResult

def getFileUIDCount(theUID, searchPath='.'):
	theResult = 0
	try:
		for root, dirs, files in os.walk(searchPath, True, None, True):
			try:	
				for name in files:
					if ( theUID == getFileUID( os.path.join(root, name) ) ):
						theResult = theResult + 1;
			except:
				continue
	except:
		print "checkFileOwners UNKNOWN - "+str(searchPath)
		exit(3)
	return theResult

def getFileUIDUsage(theUID, searchPath='.'):
	theResult = 0
	try:
		for root, dirs, files in os.walk(searchPath, True, None, True):
			try:	
				for name in files:
					if ( theUID == getFileUID( os.path.join(root, name) ) ):
						theResult = theResult + getSize(str(os.path.join(root, name) ));
			except:
				continue
	except:
		print "checkFileOwners UNKNOWN - "+str(searchPath)
		exit(3)
	return theResult

if search_path is None:
	print "checkFileOwners: SYNTAX ERROR: MISSING path"
	exit(1)

if search_uid is not None:
	theCount = 0
	if count_mode:
		theCount = getFileUIDCount(search_uid, search_path)
	else:
		theCount = getFileUIDUsage(search_uid, search_path)

	if (theCount is None) or (theCount == 0):
		if empty_is_NOT_ok is True:
			print "checkFileOwners CRITICAL - 0"
			exit(2)
		if empty_is_ok is True:
			print "checkFileOwners OK - 0"
			exit(0)
		else:
			print "checkFileOwners WARNING - 0"
			exit(1)
	elif (theCount is not None) and (theCount > 0):
		if ((theCount > critical_threshold) or (theCount >= warning_threshold)):
			if (theCount >= critical_threshold):
				print "checkFileOwners CRITICAL - "+str(theCount)
				exit(2)
			else:
				print "checkFileOwners WARNING - "+str(theCount)
				exit(1)
		elif ((theCount > critical_threshold) or (theCount >= warning_threshold) is False):
			print "checkFileOwners OK - "+str(theCount)
	else:
		if empty_is_NOT_ok is True:
			print "checkFileOwners CRITICAL - "+str(theCount)
			exit(2)
		if empty_is_ok is True:
			print "checkFileOwners OK - "+str(theCount)
			exit(0)
		else:
			print "checkFileOwners WARNING - "+str(theCount)
			exit(1)
else:
	print "ARP UNKNOWN"
	exit(3)
exit(0)