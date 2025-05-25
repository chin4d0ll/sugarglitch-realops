from instagrapi import Client
import json

with open("session.json") as f:
    session = json.load(f)

cl = Client()
cl.login_by_sessionid(session["sessionid"])

# Test
print(cl.account_info().username)
