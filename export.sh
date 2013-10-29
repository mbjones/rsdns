#!/bin/sh
#
# Matt Jones 2013
#
# Export a zone's records in a standard BIND zone format
# Usage: ./export.sh <mydomain.org>

. ./rsdns_functions.sh

DOMAIN=$1
TMP=status.xml
CRED=credentials
NS2=http://docs.rackspacecloud.com/dns/api/v1.0
. ./$CRED 

getDomainId

curl  -s \
-H "X-Auth-Token: $TOKEN"  \
-H 'Accept: application/xml'  \
"https://dns.api.rackspacecloud.com/v1.0/$TENANT/domains/$DOMAINID/export" | xmlstarlet fo > $TMP
CALLBACK=`xmlstarlet sel -N ns2=$NS2 -T -t -m "/ns2:asyncResponse" -v "ns2:callbackUrl" --nl $TMP`
STATUS=`xmlstarlet sel -N ns2=$NS2 -T -t -m "/ns2:asyncResponse" -v "ns2:status" --nl $TMP`
rm $TMP

while [ "$STATUS" != "COMPLETED" ]; do
	curl -s -H "X-Auth-Token: $TOKEN" -H 'Accept: application/xml' "${CALLBACK}?showDetails=true" | xmlstarlet fo > $TMP
	STATUS=`xmlstarlet sel -N ns2=$NS2 -T -t -m "/ns2:asyncResponse" -v "ns2:status" --nl $TMP`
done

xmlstarlet sel -N ns2=$NS2 -T -t -m "/ns2:asyncResponse" -v "ns2:response/ns2:contents" --nl $TMP
rm $TMP
