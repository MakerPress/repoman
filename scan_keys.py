from github2.client import Github


github = Github(username="MakerPress", api_token="92d4ac4e85f5bd69ed27ba1eadd75af4")


for r in github.repos.list():
   print r.name

