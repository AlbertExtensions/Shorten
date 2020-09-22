"""Shorten link and copy to clipboard"""
import time

from albertv0 import *
import json
import requests
from os import path


__iid__ = "PythonInterface/v0.2"
__prettyname__ = "Shorten"
__version__ = "0.1"
__trigger__ = "short "
__author__ = "Bharat kalluri"
__dependencies__ = ["requests"]

isgd_url = "https://is.gd/create.php?format=simple&url={}"

icon_path = "{}/icons/{}.svg".format(path.dirname(__file__), "link")


def get_short_url(input_url):
    # TODO: Handle errors
    api_resp = requests.get(isgd_url.format(input_url))
    return api_resp.content.decode()


def handleQuery(query):
    results = []

    if query.isTriggered and query.string.strip():

        # avoid rate limiting
        time.sleep(0.3)
        if not query.isValid:
            return

        item = Item(
            id=__prettyname__,
            icon=icon_path,
            completion=query.rawString,
            text=__prettyname__,
            actions=[]
        )

        if len(query.string) >=4:
            return Item(
                    id=__prettyname__,
                    icon=icon_path,
                    text="Click to copy shortened url to clipboard",
                    subtext="Link shortened by is.gd",
                    actions=[ClipAction("Copy URL to clipboard", get_short_url(query.string))])
        else:
            item.subtext = "Search in Stackoverflow!"
            return item
    return results
