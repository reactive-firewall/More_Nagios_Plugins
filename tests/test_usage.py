#! /usr/bin/env python
# -*- coding: utf-8 -*-

# From Python Repo Template for More Nagios Plugins repo
# ..................................
# Copyright (c) 2016-2018, Kendrick Walls
# ..................................
# Licensed under MIT (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# ..........................................
# http://www.github.com/reactive-firewall/More_Nagios_Plugins/LICENSE
# ..........................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import subprocess
import sys
#import profiling as profiling

def getThisPythonCommand():
        thepython = "exit 1 ; #"
        try:
            thepython = str(sys.executable)
        except Exception:
            thepython = "exit 1 ; #"
        return str(thepython)


def getPythonCommand():
        """function for backend python command"""
        thepython = "exit 1 ; #"
        try:
                thepython = checkPythonCommand(["which", "coverage"])
                if (str("/coverage") in str(thepython)) and (sys.version_info >= (3, 3)):
                        thepython = str("coverage run -p")
                elif (str("/coverage") in str(thepython)) and (sys.version_info <= (3, 2)):
                        try:
                                import coverage
                                if coverage.__name__ is not None:
                                        thepython = str("{} -m coverage run -p").format(str(sys.executable))
                                else:
                                        thepython = str(sys.executable)
                        except Exception:
                                thepython = str(sys.executable)
                else:
                        thepython = str(sys.executable)
        except Exception:
                thepython = getThisPythonCommand()
        if thepython is None:
                thepython = getThisPythonCommand()
        return str(thepython)

def checkPythonCommand(args=[None], stderr=None):
	"""Function for backend subprocess check_output command like testing with coverage support"""
	theOutput = None
	try:
		if args is None or args is [None]:
			theOutput = subprocess.check_output(["exit 1 ; #"])
		else:
			if str("coverage ") in args[0]:
				if sys.__name__ is None:
					raise ImportError("Failed to import system. WTF?!!")
				if str("{} -m coverage ").format(str(sys.executable)) in str(args[0]):
					args[0] = str(sys.executable)
					args.insert(1, str("-m"))
					args.insert(2, str("coverage"))
					args.insert(3, str("run"))
					args.insert(4, str("-p"))
					args.insert(4, str("--source=pythonrepo"))
				else:
					args[0] = str("coverage")
					args.insert(1, str("run"))
					args.insert(2, str("-p"))
					args.insert(2, str("--source=pythonrepo"))
			theOutput = subprocess.check_output(args, stderr=stderr)
	except Exception:
		theOutput = None
	try:
		if isinstance(theOutput, bytes):
			theOutput = theOutput.decode('utf8')
	except UnicodeDecodeError:
		theOutput = bytes(theOutput)
	return theOutput


#@profiling.do_cprofile
#def timePythonCommand(args=[None], stderr=None):
#	"""Function for backend subprocess check_output command
#	with support for coverage and profiling."""
#	return checkPythonCommand(args, stderr)


def checkPythonErrors(args=[None], stderr=None):
	"""Function like checkPythonCommand, but with error passing."""
	theOutput = None
	try:
		if args is None or args is [None]:
			theOutput = subprocess.check_output(["exit 1 ; #"])
		else:
			if str("coverage ") in args[0]:
				import sys
				if sys.__name__ is None:
					raise ImportError("Failed to import system. WTF?!!")
				if str("{} -m coverage ").format(str(sys.executable)) in str(args[0]):
					args[0] = str(sys.executable)
					args.insert(1, str("-m"))
					args.insert(2, str("coverage"))
					args.insert(3, str("run"))
					args.insert(4, str("-p"))
					# you need to change this to the name of your project
					args.insert(4, str("--source=pythonrepo"))
				else:
					args[0] = str("coverage")
					args.insert(1, str("run"))
					args.insert(2, str("-p"))
					args.insert(2, str("--source=pythonrepo"))
			theOutput = subprocess.check_output(args, stderr=stderr)
		if isinstance(theOutput, bytes):
			# default to utf8 your milage may vary
			theOutput = theOutput.decode('utf8')
	except Exception as err:
		theOutput = None
		raise RuntimeError(err)
	return theOutput


def debugBlob(blob=None):
	"""In case you need it."""
	try:
		print(str(""))
		print(str("String:"))
		print(str("""\""""))
		print(str(blob))
		print(str("""\""""))
		print(str(""))
		print(str("CODE:"))
		print(str("""\""""))
		print(repr(blob))
		print(str("""\""""))
		print(str(""))
	except Exception:
		return False
	return True


class BasicUsageTestSuite(unittest.TestCase):
	"""Basic functional test cases."""

	def test_absolute_truth_and_meaning(self):
		"""Insanity Test."""
		assert True

	def test_template_case(self):
		"""Test case template for: python -m check* --help """
		theResult = False
		thepython = getPythonCommand()
		if (thepython is not None):
			try:
				for test_case in ["check_arp", "checkFileOwners", "checkFileGroups", "check_memory"]:
					args = [
						str(thepython),
						str("-m"),
						str("{}").format(
							str(test_case)
						),
						str("--help")
					]
					theOutputtext = checkPythonCommand(args, stderr=subprocess.STDOUT)
					# now test it
					if (theOutputtext is not None):
						try:
							if isinstance(theOutputtext, bytes):
								theOutputtext = theOutputtext.decode('utf8')
						except UnicodeDecodeError:
							theOutputtext = str(repr(bytes(theOutputtext)))
						theResult = True
					else:
						theResult = False
						print(str(""))
						print(str("python exe is {}").format(str(sys.executable)))
						print(str("python cmd used is {}").format(str(thepython)))
						print(str("arguments used were {}").format(str(args)))
						print(str(""))
						print(str("actual output was..."))
						print(str(""))
						print(str("{}").format(str(theOutputtext)))
						print(str(""))
					# or simply:
					self.assertIsNotNone(theOutputtext)
			except Exception as err:
				print(str(""))
				print(str("python exe is {}").format(str(sys.executable)))
				print(str("arguments used were {}").format(str(thepython)))
				print(str(""))
				print(str("actual error was..."))
				print(str(""))
				print(str("{} with args {}").format(str(err),str(err.args)))
				print(str(""))
				err = None
				del err
				theResult = False
		assert theResult


if __name__ == '__main__':
	unittest.main()

