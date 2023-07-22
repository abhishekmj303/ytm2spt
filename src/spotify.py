from spotipy import util
import requests 
import os
from app_logger import setup_logger
from urllib.parse import quote
from utils import fuzzy_match_artist, artist_names_from_tracks
from typing import Literal, Any
from datetime import datetime


def generate_description() -> str:
    isodate = datetime.now().strftime("%b %d, %Y") # example: Jun 30, 2021
    github = "github.com/abhishekmj303/ytm2spt"
    description = f"Youtube Playlist Imported on {isodate} by {github}"
    return description


class SpotifyClientManager:
    def __init__(self):
        self.scope = 'playlist-read-collaborative playlist-modify-private playlist-modify-public playlist-read-private ugc-image-upload'
        self.user_id = os.getenv('SPOTIFY_USER_ID')
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')

    @property
    def token(self):
        '''
        Return the access token
        '''
        return util.prompt_for_user_token(
            self.user_id,
            scope=self.scope,
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri
        )


class Spotify:
    def __init__(self):
        self.spotify = SpotifyClientManager()
        self.playlist_id = ""
        self.spotify_logger = setup_logger(__name__)
        # print(self.spotify.token)
    
    def set_playlist_id(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.spotify_logger.debug(f"Set Playlist ID: {self.playlist_id}")
    
    def get_user_playlists(self) -> 'list':
        url = f"https://api.spotify.com/v1/users/{self.spotify.user_id}/playlists"
        response = requests.get(
            url,
            headers={
                "Authorization": f"Bearer {self.spotify.token}",
                "Content-Type": "application/json"
            }
        )
        playlists = response.json()["items"]
        self.spotify_logger.debug(f"Got User's Playlists: {playlists}")
        return playlists

    def create_playlist(self, playlist_name: str, description: str = "") -> str:
        if not description:
            description = generate_description()
        request_body = {
            "name": playlist_name,
            "description": description,
            "public": False
        }

        query = f"https://api.spotify.com/v1/users/{self.spotify.user_id}/playlists"

        response = requests.post(
            query,
            json=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.spotify.token}"
            }
        )

        playlist = response.json()
        self.spotify_logger.debug(f"Created Playlist: {playlist}")
        return playlist['id']
    
    def set_playlist_description(self, description: str = "", playlist_id: str = "") -> bool:
        if not playlist_id:
            playlist_id = self.playlist_id
        if not description:
            description = generate_description()
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        response = requests.put(
            url,
            json={"description": description},
            headers={
                "Authorization": f"Bearer {self.spotify.token}",
                "Content-Type": "application/json"
            }
        )
        self.spotify_logger.debug(f"Set Playlist {playlist_id} Description {description}: {response.status_code}")
        return response.ok
    
    def get_playlist_name(self, playlist_id: str = "") -> str:
        if not playlist_id:
            playlist_id = self.playlist_id
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        response = requests.get(
            url,
            headers={
                "Authorization": f"Bearer {self.spotify.token}",
                "Content-Type": "application/json"
            }
        )
        playlist_name = response.json()["name"]
        self.spotify_logger.debug(f"Got Playlist Name: {playlist_name}")
        return playlist_name
    
    def get_playlist_items(self, playlist_id: str = "", limit: int = 100) -> 'dict':
        if not playlist_id:
            playlist_id = self.playlist_id
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?fields=total%2Climit%2Citems%28track.id%29&limit={limit}"
        response = requests.get(
            url,
            headers={
                "Authorization": f"Bearer {self.spotify.token}",
                "Content-Type": "application/json"
            }
        )
        result = response.json()["items"]
        track_ids = [t["track"]["id"] for t in result]
        self.spotify_logger.debug(f"Got Playlist Items: {track_ids}")
        return track_ids
    
    def empty_playlist(self, playlist_id: str = "") -> bool:
        if not playlist_id:
            playlist_id = self.playlist_id
        track_ids = self.get_playlist_items(playlist_id)
        track_uris = [{"uri": "spotify:track:"+id} for id in track_ids]

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        response = requests.delete(
            url,
            json={"tracks": track_uris},
            headers={
                "Authorization": f"Bearer {self.spotify.token}",
                "Content-Type": "application/json"
            }
        )
        self.spotify_logger.debug(f"Emptied Playlist {playlist_id}: {response.status_code}")
        return response.ok

    def get_song_uri(self, artist: str, song_name: str) -> 'str':
        track_request = quote(f'{song_name} {artist}')  # TODO: intercept None types as nulls and exit search. 
        query = f'https://api.spotify.com/v1/search?q={track_request}&type=track&limit=10'
        self.spotify_logger.debug(f'Query arguments: {query}')

        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.spotify.token}"
            }
        )

        if not response.ok:
            self.spotify_logger.debug(f"Response Code: {response.status_code}")
            return None

        results = response.json()

        tracks_found = results['tracks']['items']

        artist_names = artist_names_from_tracks(tracks_found)
        track_name = f'{artist}'
        fuzzy_match_artist(
            artist_names=artist_names,
            track_input=track_name)

        if not tracks_found:
            track_uri = None
        else:
            track_uri = tracks_found[0]['uri']
        self.spotify_logger.debug(f"Got Track URI: {track_uri}")
        return track_uri

    def add_song_to_playlist(self, song_uri: str, playlist_id: str = "") -> bool:
        if not playlist_id:
            playlist_id = self.playlist_id
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        response = requests.post(
            url,
            json={"uris": [song_uri]},
            headers={
                "Authorization": f"Bearer {self.spotify.token}",
                "Content-Type": "application/json"
            }
        )
        self.spotify_logger.debug(f"Added Song {song_uri} to Playlist {playlist_id}: {response.status_code}")
        return response.ok
    
    def set_playlist_cover(self, encoded_img: str, playlist_id: str = "") -> bool:
        if not playlist_id:
            playlist_id = self.playlist_id
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/images"
        response = requests.put(
            url,
            data=encoded_img,
            headers={
                "Authorization": f"Bearer {self.spotify.token}",
                "Content-Type": "image/jpeg"
            }
        )
        self.spotify_logger.debug(f"Set Playlist Cover: {response.status_code}")
        return response.ok

    def _num_playlist_songs(self, playlist_id: str = "") -> Any | Literal[False] | None:
        if not playlist_id:
            playlist_id = self.playlist_id
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.spotify.token}"
            }
        )

        if not response.ok:
            self.spotify_logger.error("Bad API Response")
            return response.ok

        results = response.json()
        if 'total' in results:
            return results['total']
        return None
