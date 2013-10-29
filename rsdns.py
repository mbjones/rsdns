#!/usr/bin/python
#
# rsdns.py: a command line utility for managing the Rackspace CloudDNS service
#
# Copyright [2013] [Matthew B. Jones]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Requires: python_clouddns
#
import clouddns
import argparse

# Execute the main program, dispatching to an appropriate handler for each command
def main():
    args = options()
    print args
    for case in switch(args.cmd):
        if case('list'):
            list()
            break
        if case('records'):
            records(args.domain)
            break
        if case('create'):
            create_rec(args.domain, args.host, args.ip, args.rectype)
            break
        if case('update'):
            update_rec(args.domain, args.host, args.ip)
            break
        if case('delete'):
            delete_rec(args.domain, args.host)
            break
        if case('import'):
            import_domain(args.file)
            break
        if case('deldomain'):
            delete_domain(args.domain)
            break
        if case(): # default
            args.print_help()

# Parse our command line arguments
def options():
    parser = argparse.ArgumentParser(description='Commandline tool for managing DNS zones')
    parser.add_argument('cmd', help='Command to be executed', choices=['list', 'records', 'create','update','delete','import','deldomain'])
    parser.add_argument('domain', help='Name of the domain on which to act', nargs='?')
    parser.add_argument('host', help='Hostname to be created or updated', nargs='?')
    parser.add_argument('ip', help='Address to be created or updated', nargs='?')
    parser.add_argument('rectype', help='Address type to be created or updated', nargs='?')
    parser.add_argument('--file', help='file containing a BIND9 zone to be imported')
    args = parser.parse_args()
    return args

# Authenticate using credentials from the file 'credentials'
def authenticate():
    from configobj import ConfigObj
    credentials = 'credentials'

    # Read our credentials
    config = ConfigObj(credentials)
    uname = config['UNAME']
    apikey = config['APIKEY']

    # Open a connection
    dns = clouddns.connection.Connection(uname, apikey)
    return dns

# Import a BIND9 zone file
def import_domain(zonefile):
    dns = authenticate()
    with open(zonefile, 'r') as f:
        dns.import_domain(f)

# List the domains on this account
def list():
    dns = authenticate()
    for domain in dns.get_domains():
        print domain.name

# List all records for a domain::
def records(domain):
    dns = authenticate()
    domain = dns.get_domain(name=domain)
    for record in domain.get_records():
        print '(%s) %s -> %s' % (record.type, record.name, record.data)

# Create new record::
def create_rec(domain, host, ip, rectype):
    dns = authenticate()
    domain = dns.get_domain(name=domain)
    domain.create_record(host, ip, rectype)
    record = domain.get_record(name=host)
    print '(%s) %s -> %s' % (record.type, record.name, record.data)

# Update a record::
def update_rec(domain, host, ip):
    dns = authenticate()
    domain = dns.get_domain(name=domain)
    record = domain.get_record(name=host)
    record.update(data=ip, ttl=600)
    record = domain.get_record(name=host)
    print '(%s) %s -> %s' % (record.type, record.name, record.data)

# Delete a record::
def delete_rec(domain, host):
    dns = authenticate()
    domain = dns.get_domain(name=domain)
    record = domain.get_record(name=host)
    domain.delete_record(record.id)

# Delete a domain
def delete_domain(domain):
    dns = authenticate()
    domain = dns.get_domain(name=domain)
    dns.delete_domain(domain.id)

# switch class provided by Brian Beck under the PSF License from:
# http://code.activestate.com/recipes/410692/
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


main()
