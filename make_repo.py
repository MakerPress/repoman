# Add django app dir to path
import sys
sys.path.append("/home/odewahn/django/selfpub")


# Set up Django to run as a regular Python script
# See http://www.b-list.org/weblog/2007/sep/22/standalone-django-scripts/
from django.core.management import setup_environ
import settings
setup_environ(settings)

# Now do what I'd normally do in the Django shell
# 
# The basic flow is to:
# * Pull down a fresh project
# * For each prod in the database:
# *    Create a new repo in github
# *    Assign collaborators
# *    Update remote repo in "fresh" copy
# *    Push the fresh copy to GitHub
#
from selfpub.repoman.models import Person, Project, Collaborator, RepoServer
from github2.client import Github
from github2.request import *
from github2 import core
import git
from subprocess import call

# Pull down a new fresh repo

call ("rm -rf freshProject; git clone git@github.com:MakerPress/freshProject.git", shell=True)
gitdir = "/home/odewahn/django/selfpub_scripts/freshProject"
gitcmd = "git --git-dir='%s/.git' --work-tree='%s' " % (gitdir, gitdir)

# Set authentication info in GitHub
g = RepoServer.objects.all()[0]  #Pulls username and login credentials
github = Github(username=g.github_account, api_token=g.api_token)

# Pull list of projects
projects = Project.objects.all()
for p in projects:
   repo_name = "%s:%s/%s.git" % (g.base,g.github_account, p.shortname)
   print "Processing %s" % repo_name
   try:
      # Create the new repo on github
      new_repo = github.repos.create(p.shortname, p.title)
      # Reset the origin and push a new, empty repo up to github
      call("%s remote rm origin" % gitcmd, shell=True)
      call("%s remote add origin %s" % (gitcmd,repo_name), shell=True)
      call("%s push origin master" % gitcmd, shell=True)
      print "-- Created %s" % repo_name
   except RuntimeError as err:
      print " -- Repo could not be created"
      print err

