from datetime import datetime
import time
import sys
import os

from database import Database
from yt_download import yt_download
from yt_request import fetch_history

db = Database()


def data_from_element(element):
    col = element['musicResponsiveListItemRenderer']['flexColumns']
    x = 'musicResponsiveListItemFlexColumnRenderer'

    name = col[0][x]['text']['runs'][0]['text']
    video_id = col[0][x]['text']['runs'][0]['navigationEndpoint']['watchEndpoint']['videoId']

    album = None
    if 'runs' in col[2][x]['text']:
        album = col[2][x]['text']['runs'][0]['text']
    if album is not None and album == name:
        album = None

    artist = ''.join([obj['text'] for obj in col[1][x]['text']['runs']]).split("•")[0].strip()

    return {
        'name': name,
        'video_id': video_id,
        'album': album,
        'artist': artist,
    }


def download():
    data = fetch_history()

    auth_required_queue = []
    i = 0
    for group in data:
        for element in group['musicShelfRenderer']['contents']:
            data = data_from_element(element)
            print(data)

            if db.add_song(data['name'], data['video_id'], data['album'], data['artist']):
                try:
                    # Download song if it hasn't been added to db yet
                    yt_download(data)
                except Exception as e:
                    print(f"Failure on {data['video_id']} {data['name']}: {e}, adding to auth_queue", file=sys.stderr)
                    auth_required_queue.append(data)

            if i == 0:
                db.add_view(data['video_id'], datetime.now().strftime('%d/%m/%Y'))

        i += 1

    for data in auth_required_queue:
        try:
            yt_download(data, auth=True)
        except Exception as e:
            print(f"Failure on {data['video_id']} {data['name']}: {e}, skipping", file=sys.stderr)
            pass


if __name__ == '__main__':
    if os.getenv("COOKIE") is None or len(os.getenv("COOKIE")) < 8:
        print("Please set the COOKIE environment variable to your YouTube Music cookie", file=sys.stderr)
        exit(1)

    if os.getenv("AUTHORIZATION") is None or len(os.getenv("AUTHORIZATION")) < 8:
        print("Please set the AUTHORIZATION environment variable to your YouTube Music authorization", file=sys.stderr)
        exit(1)

    print("YTMusic History Downloader started")
    while True:
        start = datetime.now()
        download()
        print(f"Downloaded in {datetime.now() - start}")
        time.sleep(60 * 60 * int(os.getenv('INTERVAL', 24)))
