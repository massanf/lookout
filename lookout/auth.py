import urllib
import json
import os
import requests
import webbrowser
from oauthlib.oauth2 import WebApplicationClient
import pathlib

DEFAULT_CONFIG = {"hangthreshold": 120, "link": {}}
SCRIPT_LOCATION = pathlib.Path(os.path.realpath(os.path.dirname(__file__)))
CONFIG_LOCATION = SCRIPT_LOCATION / 'config.json'


def main():
    if not os.path.exists(CONFIG_LOCATION):
        with open(CONFIG_LOCATION, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=4,
                      sort_keys=True, separators=(',', ': '))

    CLIENT_ID = "4837413857745.4837415034865"
    REQUEST_SCOPE = "incoming-webhook"
    CLIENT_SECRET = "94bd2a56603cfc13ab47dc851064f2eb"
    REDIRECT_URL = "https://sleepy-shelf-95701.herokuapp.com/slack"

    oauth = WebApplicationClient(CLIENT_ID)
    url, headers, body = oauth.prepare_authorization_request('https://slack.com/oauth/authorize', scope=REQUEST_SCOPE, redirect_url=REDIRECT_URL)

    webbrowser.open(url)
    print("Please follow the authentication process in your browser.")
    CODE = input("Please paste your code here: ")

    request_data = {
        "client_id": CLIENT_ID,
        "code": CODE,
        "client_secret": CLIENT_SECRET,
        "scope": REQUEST_SCOPE,
        "redirect_url": REDIRECT_URL
    }

    url, headers, body = oauth.prepare_token_request('https://slack.com/api/oauth.access', code=CODE, client_secret=CLIENT_SECRET)
    req = urllib.request.Request(url, body.encode(), headers=headers)
    payload = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))

    if payload["ok"]:
        team_name = payload["team_name"],
        channel = payload["incoming_webhook"]["channel"],
        url = payload["incoming_webhook"]["url"]

        with open(CONFIG_LOCATION, 'r') as f:
            config = json.load(f)
            config["link"] = {
                "team_name": team_name,
                "channel": channel,
                "url": url
            }

        with open(CONFIG_LOCATION, 'w') as f:
            json.dump(config, f, ensure_ascii=False, indent=4,
                      sort_keys=True, separators=(',', ': '))

        print(f"Now set to {channel[0]} at {team_name[0]}!")

    else:
        errormsg = payload["error"]
        print(f"An error occured during authentication. Please try again. ({errormsg})")


if __name__ == "__main__":
    main()