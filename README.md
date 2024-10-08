# dbb_ical_extractor
Python script that extracts an ICal for your basketball teams Spielplan at DBB

## Usage

* Go to your [teams Spielplan](https://www.basketball-bund.net/static/#/liga/44714/spielplan) at basketball-bund.net
* Open a match from your team and gather the required information:
    * Right-click and click "Inspect" to bring up your browsers dev console (this is how Firefox calls it)
    * Open the "Network" Tab
    * Reload the page and look for the `matchinfo` file. Its type should be `json`
    * Open the Response and check the JSON structure
        * Note down either the `homeTeam.teamPermanentId` or `guestTeam.teamPermanentId` depending on your team
* Enter the id as `TEAM_ID` into the script
* Enter a substring that is part of your teams "Spielstätte" as `TEAM_LOCATION` into the script
* Enter a short name as `TEAM_SHORTNAME` into the script
* Install requirements using `pip install -r requirements.txt`
* Run the script using `python main.py`

## License

MIT License
