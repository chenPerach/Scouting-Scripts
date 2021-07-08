import pathlib
import requests
import json
import firebase_admin
from firebase_admin import db, credentials
from pathlib import Path

DATA_BASE_URL = "https://scouting-off-season-default-rtdb.europe-west1.firebasedatabase.app/"
MATCHES_REQUEST_URL = "https://www.thebluealliance.com/api/v3/district/2021isr/teams"

'''
 the token is securly stored in a json file in this directory
 and needs to be loaded
'''
token = {}
with open("TBA_token.json", "r") as f:
    token = json.load(f)
TBA_AUTH_TOKEN = token["token"]

if __name__ == "__main__":
    request_data = json.loads(requests.get(MATCHES_REQUEST_URL,
                              headers={'X-TBA-Auth-Key': TBA_AUTH_TOKEN}).text)
    my_data = []
    for team in request_data:
        my_data.append({
            "nickname": team["nickname"],
            "number": team["team_number"]
        })
    with open("teams.json","w") as f:
        json.dump(my_data,f)
