from datetime import datetime
import logging
import time
import os

from utils import get_fs_stats
from database import Database
from yt_download import yt_download
from yt_request import fetch_history

db = Database()
log = logging.getLogger("YTMusicHistoryDownloader")
log.setLevel(logging.DEBUG)
logging.Formatter.default_time_format = '%d/%m/%y %H:%M:%S'
logging.basicConfig(format='%(asctime)s %(levelname)s -> %(message)s')


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
        'name':     name,
        'video_id': video_id,
        'album':    album,
        'artist':   artist,
    }


def download():
    data = fetch_history()
    data_groups_length = [len(group['musicShelfRenderer']['contents']) for group in data]
    log.info(f"Received {data_groups_length} ({sum(data_groups_length)}) songs")

    auth_required_queue = []
    downloaded_count, auth_count, errors_count = 0, 0, 0
    i = 0
    for group in data:
        for element in group['musicShelfRenderer']['contents']:
            data = data_from_element(element)

            if db.add_song(data['name'], data['video_id'], data['album'], data['artist']):
                try:
                    # Download song if it hasn't been added to db yet
                    yt_download(data)
                except Exception as e:
                    log.warning(f"Failure on {data['video_id']} {data['name']}: {e}, adding to auth_queue")
                    auth_required_queue.append(data)
                else:
                    downloaded_count += 1

            if i == 0:
                db.add_view(data['video_id'], datetime.now().strftime('%d/%m/%Y'))

        i += 1

    for data in auth_required_queue:
        try:
            yt_download(data, auth=True)
        except Exception as e:
            errors_count += 1
            log.error(f"Failure on {data['video_id']} {data['name']}: {e}, skipping")
        else:
            auth_count += 1

    log.info(f"Downloaded {downloaded_count} songs, {auth_count} auth required, {errors_count} errors")


if __name__ == '__main__':
    if os.getenv("COOKIE") is None or len(os.getenv("COOKIE")) < 8:
        log.error("Please set the COOKIE environment variable to your YouTube Music cookie")
        exit(1)

    if os.getenv("AUTHORIZATION") is None or len(os.getenv("AUTHORIZATION")) < 8:
        log.error("Please set the AUTHORIZATION environment variable to your YouTube Music authorization")
        exit(1)

    print("YTMusic History Downloader started")
    while True:
        start = datetime.now()
        download()
        log.info(f"Downloaded in {datetime.now() - start}")

        download_folder_size, download_folder_filecount, database_size = get_fs_stats()
        log.info(f"Download folder size ({download_folder_filecount}): {download_folder_size / 1024 / 1024:.2f} MB")
        log.info(f"Database size: {database_size / 1024 / 1024:.2f} MB")
        song_count, view_count = db.get_stats()
        log.info(f"Database song count: {song_count}, view count: {view_count}")

        log.debug(f"Sleeping for {os.getenv('INTERVAL', 24)} hours")
        time.sleep(60 * 60 * int(os.getenv('INTERVAL', 24)))
