from ytmusicapi import OAuthCredentials, YTMusic
from dataclasses import dataclass
import re
import requests
from .app_logger import setup_logger
from typing import Optional

@dataclass
class Song:
    artist: str
    title: str


def clean_song_info(song: Song) -> Song:
    artist, title = song.artist, song.title
    title = re.sub(r'\(.*', '', title)          # Remove everything after '(' including '('
    title = re.sub(r'ft.*', '', title)          # Remove everything after 'ft' including 'ft'
    title = re.sub(r',.*', '', title)           # Remove everything after ',' including ','
    artist = re.sub(r'\sx\s.*', '', artist)     # Remove everything after ' x ' including ' x '
    artist = re.sub(r'\(.*', '', artist)        # Remove everything after '(' including '('
    artist = re.sub(r'ft.*', '', artist)        # Remove everything after 'ft' including 'ft'
    artist = re.sub(r',.*', '', artist)         # Remove everything after ',' including ','
    return Song(artist.strip(), title.strip())  # Remove whitespaces from start and end


class YoutubeMusic:
    def __init__(self, oauth_json: Optional[str] = None, client_id: str = "", client_secret: str = ""):
        self.playlist_id = ""
        self.playlist = {}
        self.songs = []
        self.yt_logger = setup_logger(__name__)
        if client_id and client_secret:
            print("Use OAuth")
            self.ytmusic = YTMusic(oauth_json, oauth_credentials=OAuthCredentials(client_id=client_id, client_secret=client_secret))
        else:
            print("Use browser")
            self.ytmusic = YTMusic(oauth_json)

    def __fetch_playlist(self) -> dict:
        result = self.ytmusic.get_playlist(self.playlist_id, limit=None)
        return result

    def __fetch_liked_songs(self) -> dict:
        return self.ytmusic.get_liked_songs(limit=None)
    
    def set_playlist_id(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.playlist = self.__fetch_playlist()
        self.songs = []

    def set_liked_songs(self):
        self.playlist_id = "LM"
        self.playlist = self.__fetch_liked_songs()
        self.songs = []

    def get_songs_from_playlist(self, limit: Optional[int] = None):
        if limit:
            tracks = self.playlist["tracks"][:limit]
        else:
            tracks = self.playlist["tracks"]
        for track in tracks:
            yt_title = track["title"]
            yt_artist = track["artists"][0]["name"]
            song = clean_song_info(Song(yt_artist, yt_title))
            self.songs.append(song)
        return self.songs

    def get_playlist_title(self):       
        return self.playlist["title"]
    
    def get_playlist_thumbnail(self):
        for thumbnails in reversed(self.playlist["thumbnails"]):
            res = requests.head(thumbnails["url"])
            if int(res.headers['content-length']) < 200*1024:
                return thumbnails["url"]
        self.yt_logger.info("No Thumbnail found which can be used as Playlist Cover")


if __name__ == "__main__":
    pass
