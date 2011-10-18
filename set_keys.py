#!/bin/python
from openstack.compute import Compute
import simplejson as json
import urllib
import sys, getopt
from subprocess import call
import time
import shlex


#
# Builds a server for a given project as defined in the Django interface
# The URLs look something like this:
#    http://localhost:8000/project/environment/json/

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

# This helper function splits the command string into component pieces so that it can be passed to process.call
# It uses shlex.split, rather than the plain old split, because it does a better job with command line-style strings. 
# (For exameple, it respecots the subquotes in the command).  Also note that SHLEX can't handle UNICODE, so 
# this function converts it to ascii and then splits the args
def cmd_fix(cmd):
   s = cmd.encode("ascii","ignore")
   return shlex.split(s)

# This procedure creates a new Racspace server based on the infor in the configuration database
# Specifically, it sets up the keys so that the collaborators can push and pull from the server
def set_root_keys(project, _username, _apikey, _image_name, _flavor_name):

   #  Make a file containing the keys we want to install
   f = open("/tmp/keys.txt", 'w')
   for key in project["collaborator-keys"]:
      f.write (key + "\n")
   f.close()


   #Pull up the ip address for the server holding the repo
   compute = Compute(username=_username, apikey=_apikey)
   instance_name = project["shortname"]
   s = compute.servers.find(name=instance_name)

   print "%s is located on %s" % (instance_name, s.public_ip)  

   #
   # copy the key file onto the new server
   #
   cmd = "scp -o 'StrictHostKeyChecking no' /tmp/keys.txt root@%s:/home/git/.ssh/authorized_keys2" % s.public_ip
   rc = call(cmd_fix(cmd))

   #
   # Set the correct permission on the authorized_keys2 file. 
   #
   cmd = "ssh -o 'StrictHostKeyChecking no' root@%s 'cd /home/git/.ssh; chown git:git authorized_keys2'" % s.public_ip
   rc = call(cmd_fix(cmd))

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
      print "Setting keys..."
      set_root_keys (project, username, apikey, image_name, flavor_name)     
   else:
      print "The following error occurred:\n  %s" % project['msg']

if __name__ == "__main__":
    main(sys.argv[1:])


