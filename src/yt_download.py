from http.cookiejar import Cookie
from yt_dlp import YoutubeDL
import os

opts = {
    'format': 'bestaudio/best',
    'outtmpl': '/downloads/%(id)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
    'quiet': True,
    'no_warnings': True,
    'noprogress': True,
    'ignoreerrors': True,
}


def cookie_converter(s: str):
    return [obj.split("=", maxsplit=1) for obj in s.split("; ")]


def yt_download(data, auth=False):
    try:
        with YoutubeDL(opts) as ydl:
            if auth:
                for x in cookie_converter(os.getenv("COOKIE")):
                    ydl.cookiejar.set_cookie(Cookie(
                        name=x[0], value=x[1], domain='.youtube.com',
                        version=0, port=None, path='/', secure=True, expires=None, discard=False,
                        comment=None, comment_url=None, rest={'HttpOnly': None},
                        domain_initial_dot=True, port_specified=False, domain_specified=True, path_specified=False))

            print(f'Downloading {data["name"]} by {data["artist"]}')
            ydl.download([f'https://music.youtube.com/watch?v={data["video_id"]}'])
    except Exception as e:
        raise e