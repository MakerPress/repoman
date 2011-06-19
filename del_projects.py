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


# Set authentication info in GitHub
g = RepoServer.objects.all()[0]  #Pulls username and login credentials
github = Github(username=g.github_account, api_token=g.api_token)


projects = Project.objects.all()
for p in projects:
   github.repos.delete(p.shortname)
   
