#!/bin/sh

TMP=auth-response.xml
CRED=credentials

. ./$CRED 

# Delete any existing TOKENs
sed -e '/TOKEN=/ d' $CRED > ${CRED}2 && mv ${CRED}2 $CRED

# Delete any existing TENANTS
sed -e '/TENANT=/ d' $CRED > ${CRED}2 && mv ${CRED}2 $CRED

curl -s -d \
"<?xml version=\"1.0\" encoding=\"UTF-8\"?>  
<auth>
   <apiKeyCredentials
      xmlns=\"http://docs.rackspace.com/identity/api/ext/RAX-KSKEY/v1.0\"
         username=\"$UNAME\"
         apiKey=\"$APIKEY\"/>
</auth>" \
-H 'Content-Type: application/xml' \
-H 'Accept: application/xml' \
'https://identity.api.rackspacecloud.com/v2.0/tokens' | xmlstarlet fo > $TMP
xmlstarlet sel -N mns=http://docs.openstack.org/identity/api/v2.0 -T -t -m "/mns:access/mns:token" -v "concat('TOKEN=',@id)" --nl $TMP >> ./$CRED
xmlstarlet sel -N mns=http://docs.openstack.org/identity/api/v2.0 -T -t -m "/mns:access/mns:token/mns:tenant" -v "concat('TENANT=',@id)" --nl $TMP >> ./$CRED
rm $TMP
