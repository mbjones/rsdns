#
# Utility functions that are used across the RSDNS scripts and provide common functionality
#
# Matt Jones, 2013

# Get the Identifier for a Domain given the DOMAIN name and the TENANT, as well as an authorization TOKEN
function getDomainId() {
	DOMAINID=`curl  -s -H "X-Auth-Token: $TOKEN" -H 'Accept: application/xml' "https://dns.api.rackspacecloud.com/v1.0/${TENANT}/domains?name=$DOMAIN" | xmlstarlet fo | xmlstarlet sel -N ns2=http://docs.rackspacecloud.com/dns/api/v1.0 -T -t -m "/ns2:domains/ns2:domain" -v "@id" --nl`
}
