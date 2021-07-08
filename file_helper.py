import json
from pathlib import Path
import datetime
from typing import List
import firebase_admin
import requests
from firebase_admin import db, credentials




class teams_helper:
    def __init__(self,path : Path):
        self.path = path
    
    def write_teams(self,teams: list) -> None:
        with open(self.path,"w") as f:
            json.dump(teams,f)

    def load_teams(self) -> list:
        teams = []
        with open(self.path,"r") as f:
            teams = json.load(f)
        return teams

class firebase_helper:
    def __init__(self,db_url : str,token_path : Path):
        cred = credentials.Certificate(token_path)
        firebase_admin.initialize_app(cred,{"databaseURL":db_url})
    
    def post_data(self,data,path):
        ref = db.reference("/")
        ref.child(path=path).set(data)

class TBA_helper:
    def __init__(self,token_path : Path):
        token = {}
        with open(token_path,"r") as f:
            token = json.load(f)
        self.token = token["token"]

    
    def fetch_matches(self,request : str) -> list:
        '''
            this function returns a sorted list of matches from the given request string
            example request string: "https://www.thebluealliance.com/api/v3/event/2020isde1/matches/simple"
        '''
        data = json.loads(requests.get(request,
                              headers={'X-TBA-Auth-Key':self.token}).text)
        matches = []
        for match in data:
            matches.append({
                "time": match["time"],
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
        matches.sort(key=lambda e:e["time"])
        return matches
    
    def fetch_teams(self,request:str) -> list:
        '''
        this function returns a list of teams from a given request string
        example request string:
        https://www.thebluealliance.com/api/v3/district/2021isr/teams
        '''
        request_data = json.loads(requests.get(request,
                            headers={'X-TBA-Auth-Key': self.token}).text)
        my_data = []
        for team in request_data:
            my_data.append({
                "nickname": team["nickname"],
                "number": team["team_number"]
            })
        return my_data
        
class matches_helper:
    def __init__(self,filepath : Path):
        self.path = filepath

    """
    this function loads the matches from file and sorts them by time
    then the function puts writes these matches back to the file
    """
    def sort_matches(self):
        """
        loads matches from the given file, 
        sorts them by time and writes them back to the given file
        """
        data = []
        with open(self.path,"r") as f:
            data = json.load(f)

        data.sort(key=lambda e:e["time"])
        with open(self.path,"w") as f:
            json.dump(data,f)
    def write_matches(self,matches :list):
        with open(self.path,"w") as f:
            json.dump(matches,f)
    def load_matches(self)->list:
        return json.load(open(self.path,"r"))
    def give_times(self):
        """
        laods matches from file, gives the a compotition time for 30 minutes from now and writes them back
        """
        matches = []
        with open(self.path,"r") as f:
            matches = json.load(f)
        startingTime = datetime.datetime.now()
        starting_delta = datetime.timedelta(minutes=30)
        difference_delta = datetime.timedelta(minutes=5)
        startingTime += starting_delta
        for match in matches:
            match["time"] = int(startingTime.timestamp())
            startingTime+=difference_delta

        with open(self.path,"w") as f:
            json.dump(matches,f)