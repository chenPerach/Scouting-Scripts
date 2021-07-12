
import json
from firebase_admin import db, credentials
from pathlib import Path
from file_helper import *


BRANCH = "2021isjo"
MATCHES_REQUEST_URL = "https://www.thebluealliance.com/api/v3/event/2021isjo/matches/simple"

'''
 the token is securly stored in a json file in this directory
 and needs to be loaded
'''
match_h = matches_helper(filepath=Path(Path.cwd(),"matches.json"))
TBA_h = TBA_helper(token_path=Path(Path.cwd(),"TBA_token.json"))
firebase_h = firebase_helper(db_url=Path(Path.cwd(),"firebase_rtdb_url.json"),token_path=Path(Path.cwd(),"firebase_auth_key.json"))

if __name__ == "__main__":
    matches = TBA_h.fetch_matches(request=MATCHES_REQUEST_URL)

    match_h.write_matches(matches=matches)
    match_h.sort_matches()

    firebase_h.post_data(data=match_h.load_matches(),path=f"{BRANCH}/matches")
