import json
from firebase_admin import db, credentials
from pathlib import Path
from file_helper import *


BRANCH = "2020isde1"
MATCHES_REQUEST_URL = "https://www.thebluealliance.com/api/v3/event/2020isde1/matches/simple"

'''
 the token is securly stored in a json file in this directory
 and needs to be loaded
'''
match_h = matches_helper(filepath=Path(Path.cwd(),"matches.json"))
TBA_h = TBA_helper(token_path=Path(Path.cwd(),"TBA_token.json"))
firebase_h = firebase_helper(db_url=Path(Path.cwd(),"firebase_rtdb_url.json"),token_path=Path(Path.cwd(),"firebase_auth_key.json"))

if __name__ == "__main__":
    match_h.give_times()
    matches = match_h.load_matches()

    firebase_h.post_data(data=matches,path=f"{BRANCH}/matches")
    