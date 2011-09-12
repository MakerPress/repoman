import pycurl
import json

URL = "https://auth.api.rackspacecloud.com/v1.0/makerpressadmin/domains/"
USER = "makerpressadmin"
PASS = "39a15325f2e67a3ff68d59b76f990616"

c = pycurl.Curl()
c.setopt(pycurl.URL, URL)
c.setopt(pycurl.HTTPHEADER, [
   'X-Auth-User: %s' % USER,  
   'X-Auth-Key: %s' % PASS])





c.perform()

print c.getinfo(pycurl.HTTP_CODE), c.getinfo(pycurl.EFFECTIVE_URL)



