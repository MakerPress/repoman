
#
# Example of how to use httplib2 against the Rackspace DNS API
# Good resource on what's required is here: http://developer.yahoo.com/python/python-rest.html
# Be sure you also install httplib2 with "pip install httplib2"
#
# Andrew Odewahn
# odewahn@oreilly.com
#
import urllib
import httplib2
import json
import sys

username = "makerpressadmin"
api_key = "39a15325f2e67a3ff68d59b76f990616"  #Obtain this from the control panel
domain = "makerpress.com"

x_auth_token = ""
account_id = ""

http = httplib2.Http()


#
# Define API credientials for use in the header
#
head = {
   'X-Auth-User': username,
   'X-Auth-Key': api_key
}

# First step is to authenticate and obtain and x-auth-token
# This is described on page 6
response, content = http.request("https://auth.api.rackspacecloud.com/v1.0", headers=head)
if response['status'] != "204":
   print "An error occurred!  Here is what the server said...\n" 
   print json.dumps(response, indent = 3)
   sys.exit(1)

x_auth_token = response['x-auth-token']
account_id = response['x-server-management-url'].split("/")[-1]  #Pull account id, per page 7 of the Rackspace docs

print "Auth token is %s" % x_auth_token
print "Account ID is %s" % account_id

# Must pass auth token in the header for all API calls
auth_head = {
   'X-Auth-Token' : x_auth_token,
}  

base_service_url = "https://dns.api.rackspacecloud.com/v1.0/%s" % account_id

# Fetch domain information for the makerpress.com domain
response, content = http.request("%s/domains/?name=%s" % (base_service_url, domain), headers =  auth_head)
if response['status'] != "200":
   print "An error occurred!  Here is what the server said...\n" 
   print json.dumps(response, indent = 3)
   sys.exit(1)

c = json.loads(content) # load JSON string into a data structure
domain_id = c['domains'][0]['id']
print "Domain ID is %s" % domain_id


rec = { 'records': [
   {
   'name': "test.makershed.com",
   'data': "50.57.77.147",
   'type': "A",
   'ttl': 300
  }
]}


post_head = {
   'X-Auth-Token' : x_auth_token,
   'Content-type': 'application/json'   
}  


# Fetch domain information for the makerpress.com domain
response, content = http.request("%s/domains/%s/records" % (base_service_url, domain_id), 
   'POST',
   body = json.dumps(rec),
   headers =  post_head)

print response
print content




