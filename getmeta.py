from yt_dlp import YoutubeDL
import time


def main(url):
    with YoutubeDL() as ydl:
        res = ydl.extract_info(url, download=False)
    return res
