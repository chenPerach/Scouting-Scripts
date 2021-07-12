
import json
from firebase_admin import db, credentials
from pathlib import Path
from file_helper import *


BRANCH = "2021isjo"
MATCHES_REQUEST_URL = "https://www.thebluealliance.com/api/v3/district/2021isr/teams"

'''
 the token is securly stored in a json file in this directory
 and needs to be loaded
'''
match_h = matches_helper(filepath=Path(Path.cwd(),"matches.json"))
team_h = teams_helper(Path(Path.cwd(),"teams.json"))
TBA_h = TBA_helper(token_path=Path(Path.cwd(),"TBA_token.json"))
firebase_h = firebase_helper(db_url=Path(Path.cwd(),"firebase_rtdb_url.json"),token_path=Path(Path.cwd(),"firebase_auth_key.json"))


if __name__ == "__main__":
    # request_data = json.loads(requests.get(MATCHES_REQUEST_URL,
    #                           headers={'X-TBA-Auth-Key': TBA_AUTH_TOKEN}).text)
    data = TBA_h.fetch_teams(MATCHES_REQUEST_URL)
    team_h.load_teams()
    my_data = []
    for team in data:
        my_data.append({
            "nickname": team["nickname"],
            "number": team["number"]
        })
    team_h.write_teams(my_data)

    firebase_h.post_data(my_data,f"{BRANCH}/teams")
