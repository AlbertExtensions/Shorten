"""Shorten link and copy to clipboard"""
import time
import traceback
from os import path
import subprocess

import requests
from albert import *

__title__ = "Shorten"
__version__ = "0.4.0"
__triggers__ = "short "
__author__ = "Bharat kalluri"
__exec_deps__ = ["xclip"]
__py_deps__ = ["requests", "traceback"]
__homepage__ = "https://github.com/AlbertExtensions/Shorten"

isgd_url = "https://is.gd/create.php?format=simple&url={}"

icon_path = "{}/icons/{}.svg".format(path.dirname(__file__), "link")


def get_short_url(input_url: str):
    api_resp = requests.get(isgd_url.format(input_url))
    return api_resp.content.decode()


def copy_to_clipboard(s: str):
    subprocess.run(f"echo {s} | xclip -rmlastnl -selection clipboard", shell=True)


def handleQuery(query):
    results = []

    try:

        if query.isTriggered and query.string.strip():
            if len(query.string) >= 4:
                results.append(
                    Item(
                        id=__title__,
                        icon=icon_path,
                        text="Click to copy shortened url to clipboard",
                        subtext="Link shortened by is.gd",
                        completion=__triggers__,
                        actions=[
                            FuncAction(
                                "Copy URL to clipboard",
                                lambda url=query.string: copy_to_clipboard(get_short_url(url)),
                            )
                        ],
                    )
                )
            else:
                results.append(
                    Item(
                        id=__title__,
                        icon=icon_path,
                        completion=__triggers__,
                        text="Paste the URL that you want to shorten",
                        actions=[],
                    )
                )

    except Exception:  # user to report error
        results.insert(
            0,
            Item(
                id=__title__,
                icon=icon_path,
                text="Something went wrong! Press [ENTER] to copy error and report it",
                actions=[
                    ClipAction(
                        f"Copy error - report it to {__homepage__[8:]}",
                        f"{traceback.format_exc()}",
                    )
                ],
            ),
        )

    return results
