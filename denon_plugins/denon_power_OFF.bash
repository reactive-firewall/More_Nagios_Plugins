#! /bin/bash

HOST_TARGET=${1}

if [[ ( $(curl -fsSL -H 'DNT: 1' --tlsv1.2 --url "http://${HOST_TARGET}/index.asp" 2>/dev/null 3>/dev/null | fgrep "MAIN ZONE" | fgrep "Status" | fgrep -o "img/Power_OFF.gif" | wc -l ) -gt 0 ) ]] ; then 

echo "DOWN"
exit 0;
fi

if [[ ( $(curl -fsSL -H 'DNT: 1' --tlsv1.2 --url "http://${HOST_TARGET}/index.asp" 2>/dev/null 3>/dev/null | fgrep "MAIN ZONE" | fgrep "Status" | fgrep -o "img/Power.gif" | wc -l ) -gt 0 ) ]] ; then 

curl 'http://${HOST_TARGET}/MainZone/index.put.asp' \
-XPOST \
-H 'Referer: http://${HOST_TARGET}/MainZone/index.html' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-H 'Origin: http://${HOST_TARGET}' \
-H 'Host: ${HOST_TARGET}' \
-H 'Connection: close' \
-H 'Accept-Language: en-us' \
-H 'DNT: 1' \
-H 'User-Agent: Mozilla/5.0 (Linux; Nagios event handler)' \
-H 'Cookie: ZoneName=MAIN%20ZONE' \
-H 'X-Requested-With: XMLHttpRequest' \
--data 'cmd0=PutZone_OnOff%2FOFF&cmd1=aspMainZone_WebUpdateStatus%2F'

fi

if [[ ( $(curl -fsSL -H 'DNT: 1' --tlsv1.2 --url "http://${HOST_TARGET}/index.asp" 2>/dev/null 3>/dev/null | fgrep "MAIN ZONE" | fgrep "Status" | fgrep -o "img/Power.gif" | wc -l ) -gt 0 ) ]] ; then 

echo "UP"
exit 1 ;
fi

if [[ ( $(curl -fsSL -H 'DNT: 1' --tlsv1.2 --url "http://${HOST_TARGET}/index.asp" 2>/dev/null 3>/dev/null | fgrep "MAIN ZONE" | fgrep "Status" | fgrep -o "img/Power_OFF.gif" | wc -l ) -gt 0 ) ]] ; then 

echo "DOWN"

fi

exit 0 ;