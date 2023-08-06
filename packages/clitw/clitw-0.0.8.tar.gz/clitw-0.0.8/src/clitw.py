import json
import os
import webbrowser
from typing import Any

import fire
import tweepy

BASE_URL = "https://api.twitter.com/"
ROOT_PATH = os.environ["HOME"] + "/clitw"
TOKEN_FILE = ROOT_PATH + "/oauth_token.json"
CONSUMER_FILE = ROOT_PATH + "/consumer_token.json"


def make_auth() -> Any:
    with open(CONSUMER_FILE, mode="+r") as f:
        consumer = json.load(f)
    return tweepy.OAuthHandler(**consumer)


def authenicate_oauth(auth: Any) -> str:
    try:
        redirect_url = auth.get_authorization_url()
    except Exception as e:
        raise tweepy.TweepError(e)

    if webbrowser.open_new_tab(redirect_url):
        return input("Verifier: ")
    else:
        raise ValueError()


def load_access_token() -> Any:
    auth = make_auth()
    if os.path.isfile(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            token = json.load(f)
    else:
        verifier = authenicate_oauth(auth)
        try:
            key, secret = auth.get_access_token(verifier)
        except Exception as e:
            raise tweepy.TweepError(e)

        token = {"key": key, "secret": secret}
        with open(TOKEN_FILE, mode="w") as f:
            json.dump(token, f)
    auth.set_access_token(**token)
    return auth


def make_api() -> Any:
    auth = load_access_token()
    return tweepy.API(auth)


class Twitter:
    def __init__(self) -> None:
        if not os.path.isdir(ROOT_PATH):
            os.makedirs(ROOT_PATH)
        self.api = make_api()

    def tw(self) -> None:
        flag = "n"
        text = ""
        while flag != "y":
            text = input("Text: ")
            print(text)
            flag = input("Tweet? (y or n): ")
        try:
            self.api.update_status(text)
        except Exception as e:
            raise tweepy.TweepError(e)
        print("success")


def main() -> None:
    fire.Fire(Twitter)
