
import requests
from datetime import datetime, timedelta
from pathlib import Path

from ical.calendar import Calendar
from ical.calendar_stream import IcsCalendarStream
from ical.event import Event

TEAM_ID = 310224
TEAM_SHORTNAME = "U10"
TEAM_LOCATION = "Bassen"

calendar = Calendar()

season_url = "https://www.basketball-bund.net/rest/competition/id/44714/matchday/1"
season_data = requests.get(season_url).json()['data']

for gameday in season_data['spieltage']:
    gameday_url = f"https://www.basketball-bund.net/rest/competition/id/44714/matchday/{gameday['spieltag']}"
    gameday_data = requests.get(gameday_url).json()['data']
    for match in gameday_data['matches']:
        if not (match['homeTeam']['teamPermanentId'] == TEAM_ID or
                match['guestTeam']['teamPermanentId'] == TEAM_ID):
            continue

        matchinfo_url = f"https://www.basketball-bund.net/rest/match/id/{ match['matchId'] }/matchInfo"
        matchinfo_resp = requests.get(matchinfo_url).json()
        matchinfo_data = matchinfo_resp['data']
        location = matchinfo_data['matchInfo']['spielfeld']
        address = f"{location['bezeichnung']}, {location['strasse']}, {location['plz']} {location['ort']}"
        if TEAM_LOCATION in address:
            versus_short = 'vs.'
        else:
            versus_short = 'at'            
        
        kickoff_str = f"{matchinfo_data['kickoffDate']}T{matchinfo_data['kickoffTime']}"
        start = datetime.strptime(kickoff_str, "%Y-%m-%dT%H:%M")
        end = start + timedelta(hours=2)
        
        if match['homeTeam']['teamPermanentId'] == TEAM_ID:
            opponent_name = matchinfo_data['guestTeam']['teamname']
        else:
            opponent_name = matchinfo_data['homeTeam']['teamname']
        print(f"{start} - {TEAM_SHORTNAME} {versus_short} {opponent_name} @ {address}")
 
        event = Event(
            summary=f"{TEAM_SHORTNAME} {versus_short} {opponent_name}",
            start=start,
            end=end,
            location=address
        )       
        calendar.events.append(event)
     
for event in calendar.timeline:
    print(event.summary)
        
filename = Path(f"spielplan_{TEAM_SHORTNAME}.ics")
with filename.open("w") as ics_file:
    ics_file.write(IcsCalendarStream.calendar_to_ics(calendar))
    