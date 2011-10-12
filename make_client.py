#!/bin/python
from openstack.compute import Compute
import simplejson as json
import urllib
import sys, getopt


#
# Builds a server for a given project as defined in the Django interface
# The URLs look something like this:
#    http://localhost:8000/server/environment/json/

# Help function that prints an error message
def usage():
   print '''
      Correct usage is:
         -s <url>   : Specifies source URL for JSON data that describes the project
         -p         : Prints the JSON
         -h         : Prints the help info
   '''

# Pulls the project infor from a given url
def pull_project_info(url):
   try:
      dat = urllib.urlopen(url).read()
      return json.loads(dat)
   except IOError:
      return None

# This procedure creates a new Racspace server based on the infor in the configuration database
# Specifically, it sets up the keys so that the collaborators can push and pull from the server
def create_server(project, _username, _apikey, _image_name, _flavor_name):
   instance_name = "prod-%s" % project["shortname"]
   master_key = "\n".join(project["keys"])

   fileInfo = { 
      '/root/.ssh/authorized_keys2' : master_key,
      '/home/git/.ssh/authorized_keys2': master_key
   }

   #Create a new image based on the given parameters
   compute = Compute(username=_username, apikey=_apikey)
   im = compute.images.find(name=_image_name)
   fl = compute.flavors.find(name=_flavor_name)
   s = compute.servers.create(instance_name, image=im, flavor=fl, files=fileInfo)

   #Now print results
   print "You can log into this server as root@%s" % s.public_ip

#
# Main function to process command line args and call the scripts
#
def main (argv):

   url = ""
   print_flag = False
   username = "makerpressadmin"
   apikey = "39a15325f2e67a3ff68d59b76f990616"
   image_name = "gold-image-8"
   flavor_name = "256 server"

   try:
      opts, args = getopt.getopt(argv, "hps:")   
   except getopt.GetoptError:
      usage()
      sys.exit(2)

   # now process the arguments
   for opt, arg in opts:
      if opt == '-s':
         url = arg
      elif opt == '-h':
         usage()
         sys.exit()
      elif opt == '-p':
         print_flag = True

   # Make sure they supplied a source URL.  If they didn't, then bomb out
   if len(url) == 0:
      usage()
      sys.exit()
   
   # Try to load the URL.  If it can't be found, then bomb out.
   project = pull_project_info (url)
   if not project:
      print "Could not load %s" % url
      sys.exit()

   # Print the JSON if the print flag has been set
   if print_flag :
      print "Project Data"
      print "------------"
      print json.dumps(project,  sort_keys=False, indent=4)

   if project['status'] == 'OK':
      print "Creating server..."
      create_server (project, username, apikey, image_name, flavor_name)
   else:
      print "The following error occurred:\n  %s" % project['msg']

if __name__ == "__main__":
    main(sys.argv[1:])


