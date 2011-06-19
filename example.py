# Add django app dir to path
import sys
sys.path.append("/home/odewahn/django/selfpub")


# Set up Django to run as a regular Python script
# See http://www.b-list.org/weblog/2007/sep/22/standalone-django-scripts/
from django.core.management import setup_environ
import settings
setup_environ(settings)

# Now do what I'd normally do in the Django shell
from selfpub.repoman.models import Person, Project, Collaborator, RepoServer
from github2.client import Github


# First fetch github login info from Django
g = RepoServer.objects.all()[0]


github = Github(username=g.github_account, api_token=g.api_token)
repos = github.repos.list()
for r in repos:
   print r.name
