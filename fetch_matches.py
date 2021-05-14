import pathlib
import requests
import json
import firebase_admin
from firebase_admin import db, credentials
from pathlib import Path

DATA_BASE_URL = "https://scouting-off-season-default-rtdb.europe-west1.firebasedatabase.app/"
MATCHES_REQUEST_URL = "https://www.thebluealliance.com/api/v3/event/2020isde1/matches/simple"
token = {}
with open("TBA_token.json","r") as f:
    token = json.load(f)
TBA_AUTH_TOKEN = token["token"]
if __name__ == "__main__":
    request_data = json.loads(requests.get(MATCHES_REQUEST_URL,
                              headers={'X-TBA-Auth-Key': TBA_AUTH_TOKEN}).text)

    with open('data.json', 'w') as f:
        json.dump(request_data, f)

    my_data = []

    for match in request_data:
        my_data.append({
            "time": match["predicted_time"],
            "comp_level": match["comp_level"],
            "match_number": match["match_number"],
            "alliances": {
                "red": {
                    "score": match["alliances"]["red"]["score"],
                    "team_keys": [i for i in match["alliances"]["red"]["team_keys"]]
                },
                "blue": {
                    "score": match["alliances"]["blue"]["score"],
                    "team_keys": [i for i in match["alliances"]["blue"]["team_keys"]]
                },
            }
        })

    with open('my_data.json', 'w') as f:
        json.dump(my_data, f)
    
    path = Path(Path.cwd(),"firebase_auth_key.json")
    cred = credentials.Certificate(path)
    firebase_admin.initialize_app(cred,{'databaseURL':DATA_BASE_URL})

    ref = db.reference("/")
    ref.child("matches").set(my_data)
