import platform
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
import os
from .app_logger import setup_logger
from .utils import fuzzy_match_artist, artist_names_from_tracks
from typing import Union
from datetime import datetime


def generate_description() -> str:
    isodate = datetime.now().strftime("%b %d, %Y") # example: Jun 30, 2021
    github = "github.com/abhishekmj303/ytm2spt"
    description = f"Youtube Playlist Imported on {isodate} by {github}"
    return description


class Spotify:
    def __init__(self):
        self.user_id = os.environ["SPOTIFY_USER_ID"]
        open_browser = True
        if platform.system() == "Linux" and not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")):
            open_browser = False
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.environ['SPOTIFY_CLIENT_ID'],
            client_secret=os.environ['SPOTIFY_CLIENT_SECRET'],
            redirect_uri=os.environ['SPOTIFY_REDIRECT_URI'],
            scope='playlist-read-collaborative playlist-modify-private playlist-modify-public playlist-read-private ugc-image-upload',
            open_browser=open_browser,
            cache_path=".spotipy_cache",
        ))
        self.playlist_id = ""
        self.spotify_logger = setup_logger(__name__)
        # print(self.spotify.token)
    
    def set_playlist_id(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.spotify_logger.debug(f"Set Playlist ID: {self.playlist_id}")
    
    def get_user_playlists(self) -> 'list':
        playlists = self.spotify.user_playlists(self.user_id)["items"]
        self.spotify_logger.debug(f"Got User's Playlists: {playlists}")
        return playlists

    def create_playlist(self, playlist_name: str, description: str = "") -> str:
        playlist = self.spotify.user_playlist_create(self.user_id, playlist_name, description)
        self.spotify_logger.debug(f"Created Playlist: {playlist}")
        return playlist['id']
    
    def set_playlist_description(self, description: str = "", playlist_id: str = "") -> None:
        if not playlist_id:
            playlist_id = self.playlist_id
        if not description:
            description = generate_description()
        self.spotify.playlist_change_details(playlist_id, description=description)
        self.spotify_logger.debug(f"Set Playlist {playlist_id} Description {description}")
    
    def get_playlist_name(self, playlist_id: str = "") -> str:
        if not playlist_id:
            playlist_id = self.playlist_id
        playlist_name = self.spotify.playlist(playlist_id)["name"]
        self.spotify_logger.debug(f"Got Playlist Name: {playlist_name}")
        return playlist_name
    
    def get_playlist_items(self, playlist_id: str = "", limit: int = 100) -> 'dict':
        if not playlist_id:
            playlist_id = self.playlist_id
        result = self.spotify.playlist_tracks(playlist_id, limit=limit)["items"]
        track_ids = [t["track"]["id"] for t in result]
        self.spotify_logger.debug(f"Got Playlist Items: {track_ids}")
        return track_ids
    
    def empty_playlist(self, playlist_id: str = "") -> None:
        if not playlist_id:
            playlist_id = self.playlist_id
        tracks = self.get_playlist_items(playlist_id)
        track_ids = [id for id in tracks]

        if not track_ids:
            self.spotify_logger.debug(f"Playlist {playlist_id} is already empty")
            return

        self.spotify.playlist_remove_all_occurrences_of_items(playlist_id, track_ids)
        self.spotify_logger.debug(f"Emptied Playlist {playlist_id}")

    def get_song_uri(self, artist: str, song_name: str) -> Union['str', None]:
        try:
            results = self.spotify.search(f'{song_name} {artist}', type='track', limit=10)
        except SpotifyException as e:
            self.spotify_logger.error(f"Error searching for song: {e}")
            return None

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
        try:
            self.spotify.playlist_add_items(playlist_id, [song_uri])
            self.spotify_logger.debug(f"Added Song {song_uri} to Playlist {playlist_id}")
            return True
        except SpotifyException as e:
            self.spotify_logger.error(f"Error adding song to playlist: {e}")
            return False
    
    def set_playlist_cover(self, encoded_img: str, playlist_id: str = "") -> bool:
        if not playlist_id:
            playlist_id = self.playlist_id
        try:
            self.spotify.playlist_upload_cover_image(playlist_id, encoded_img)
            self.spotify_logger.debug(f"Set Playlist Cover: {encoded_img}")
            return True
        except SpotifyException as e:
            self.spotify_logger.error(f"Error setting playlist cover: {e}")
            return False

    def _num_playlist_songs(self, playlist_id: str = "") -> Union['int', None]:
        if not playlist_id:
            playlist_id = self.playlist_id
        results = self.spotify.playlist_items(playlist_id, limit=1)
        return results.get("total")
