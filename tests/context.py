# -*- coding: utf-8 -*-

# From Python Repo Template for More Nagios Plugins repo
# ..................................
# Copyright (c) 2016-2017, Kendrick Walls
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


try:
	import sys
	import os
	if 'pythonrepo' in __file__:
		sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
except Exception as ImportErr:
	print(str(type(ImportErr)))
	print(str(ImportErr))
	print(str((ImportErr.args)))
	ImportErr = None
	del ImportErr
	raise ImportError("Python Repo Failed to Import")


#try:
#	import pythonrepo as pythonrepo
#	if pythonrepo.__name__ is None:
#		raise ImportError("Failed to import pythonrepo.")
#except Exception as importErr:
#	importErr = None
#	del importErr
#	raise ImportError("Test module failed to load pythonrepo for test.")
#	exit(0)
