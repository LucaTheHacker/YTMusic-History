import os
import sys

import requests

headers = {
    'authority': 'music.youtube.com',
    'accept': '*/*',
    'accept-language': 'it-IT,it;q=0.9',
    'authorization': os.getenv("AUTHORIZATION"),
    'content-type': 'application/json',
    'cookie': os.getenv("COOKIE"),
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'x-origin': 'https://music.youtube.com',
    'x-youtube-bootstrap-logged-in': 'true',
    'x-youtube-client-name': '67',
    'x-youtube-client-version': '1.20230829.05.00'
}


def fetch_history():
    r = requests.post("https://music.youtube.com/youtubei/v1/browse?prettyPrint=false", headers=headers, json={
        "context": {
            "client": {
                "hl": "it",
                "gl": "IT",
                "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36,gzip(gfe)",
                "clientName": "WEB_REMIX",
                "clientVersion": "1.20230829.05.00",
                "platform": "DESKTOP",
                "acceptHeader": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "timeZone": "Europe/Rome"
            },
            "user": {
                "lockedSafetyMode": False
            }
        },
        "browseId": "FEmusic_history"
    })

    if r.status_code != 200:
        print("Error while fetching YTMusic history, please check credentials", file=sys.stderr)
        print(r.text, file=sys.stderr)
        return []

    return r.json()['contents']['singleColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents']
