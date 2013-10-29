RS DNS Tools
============

Rackspace provides a [distributed DNS service](http://docs.rackspace.com/cdns/api/v1.0/cdns-devguide/content/overview.html) 
with a REST API for accessing and modifying zone information.  RS DNS Tools is a simple set of 
utility scripts for manipulating a Rackspace-managed DNS zone.  At this point, these scripts 
were developed solely to make it easier for me to automate some tasks, but they may be useful 
to others.  Have at it. Contributions including code, bug reports, and feedback are all welcome.

There are two main types of tools in this package:
* rsdns.py: a Python commandline tool that allows you to list domains, list records in a domain, create a record in a domain, update a record in a domain, delete a record from a domain, import a domain from a BIND9 file, and to delete a whole domain
* bash scripts: a set of Bash scripts that let you call the Rackspace API directly to authenticate (auth.sh), export a domain (export.sh), and show records for a domain (records.sh).  These are not as useful as the python commandline tool, but are included due to the export feature.

* Contributors: Matthew Jones
* Bug reports: http://github.com/mbjones/rsdns/issues

Installation
------------
For rsdns.py, you must first install python\_clouddns using a command such as:
```sh
sudo pip install python_clouddns
```
The argparse module ships with Python 2.7 and should be standard.

License
-------
```
Copyright [2013] [Matthew B. Jones]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

