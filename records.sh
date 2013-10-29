#!/bin/sh
#
# Matt Jones 2013
#
# Output a basic set of zone records for the domain.
# Usage: ./details.sh <mydomain.org>

. ./rsdns_functions.sh

DOMAIN=$1
CRED=credentials
. ./$CRED 

getDomainId

curl  -s \
-H "X-Auth-Token: $TOKEN"  \
-H 'Accept: application/xml'  \
"https://dns.api.rackspacecloud.com/v1.0/${TENANT}/domains/${DOMAINID}" | xmlstarlet fo
