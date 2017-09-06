# More_Nagios_Plugins
Even More Nagios/Shinken/Sensu/etc Monitoring Plugins

#`check_arp.py`
```plain
goal: check for an arp entry

usage: check_arp.py [-h] [-M MAC] -H HOST [-C | -U | --empty-ok]

optional arguments:
  -h, --help            show this help message and exit
  -M MAC, --mac MAC     check for an exact MAC
  -H HOST, --host HOST  check for an exact IP
  -C, --critical        return critical instead of warning on empty MAC,
                        overides other empty values
  -U, --empty-unknown   return unknown instead of warning on empty MAC
  --empty-ok            return ok on empty MAC instead, cannot be combined
                        with optionals
```
#`checkFileGroups.py`

```plain
goal: check for file count by group

usage: checkFileGroups.py [-h] -S SEARCH -g GID [-c CRITICAL] [-w WARNING]
                          [--empty-critical | --empty-ok]
                          [--unsafe | --only-safe] [--count | --size]

optional arguments:
  -h, --help            show this help message and exit
  -S SEARCH, --search SEARCH
                        search path root to check
  -g GID, --gid GID     search for group owned files with this GID
  -c CRITICAL, --critical CRITICAL
                        critical threshold in filecount or bytes
  -w WARNING, --warning WARNING
                        warning threshold in filecount or bytes
  --empty-critical      return critical instead of warning on empty search
                        path, overides cannot be combined with other reporting
                        modes
  --empty-ok            return ok on empty search path instead, cannot be
                        combined with optionals
  --unsafe              allow unsafe ranges, overides some checks cannot be
                        combined with safe mode
  --only-safe           allow only safe ranges (default), force some checks
                        cannot be combined with un-safe mode
  --count               units are in file counts, cannot be combined with size
                        mode
  --size                units are in bytes used by files, cannot be combined
                        with count mode
```
#`checkFileOwners.py`

```plain
goal: check for file count by owner

usage: checkFileOwners.py [-h] -S SEARCH -u UID [-c CRITICAL] [-w WARNING]
                          [--empty-critical | --empty-ok]
                          [--unsafe | --only-safe] [--count | --size]

optional arguments:
  -h, --help            show this help message and exit
  -S SEARCH, --search SEARCH
                        search path root to check
  -u UID, --uid UID     search for user owned files with this UID
  -c CRITICAL, --critical CRITICAL
                        critical threshold in filecount or bytes
  -w WARNING, --warning WARNING
                        warning threshold in filecount or bytes
  --empty-critical      return critical instead of warning on empty search
                        path, overides cannot be combined with other reporting
                        modes
  --empty-ok            return ok on empty search path instead, cannot be
                        combined with optionals
  --unsafe              allow unsafe ranges, overides some checks cannot be
                        combined with safe mode
  --only-safe           allow only safe ranges (default), force some checks
                        cannot be combined with un-safe mode
  --count               units are in file counts, cannot be combined with size
                        mode
  --size                units are in bytes used by files, cannot be combined
                        with count mode
```

License:
- Apache 2.0 License for original work (i.e non-sub moduled)
- sub-modules are referenced for connivence only, please see relevant sub-module's own project for details


PROVIDED AS IS AND WITHOUT WARRANTY
