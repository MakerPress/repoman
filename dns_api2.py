import urllib,urllib2
import json

opener = urllib2.build_opener()

values = {}
headers = {
   'X-Auth-User': 'makerpressadmin',
   'X-Auth-Key': '39a15325f2e67a3ff68d59b76f990616'
}


data = urllib.urlencode(values)
req = urllib2.Request("https://auth.api.rackspacecloud.com/v1.0", data, headers)
response = urllib2.urlopen(req)
the_page = response.read()

