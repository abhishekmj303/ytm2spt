from typing import Any
from spotify import Spotify
from youtube import YoutubeMusic
from urllib import request
import base64
import argparse
from app_logger import setup_logger


def url_to_id(url: str, site: str) -> str:
    if site == "yt":
        for char in ["list=", "list\\="]:
            if char in url:
                return url.split(char)[1].split("&")[0]
        else:
            raise ValueError("Not a valid Youtube Playlist URL")
    
    elif site == "sp":
        if "playlist/" in url:
            return url.split("playlist/")[1].split("?")[0]
        elif "spotify:playlist:" in url:
            return url.removeprefix("spotify:playlist:")
        else:
            raise ValueError("Not a valid Spotify Playlist URL")


def get_youtube_playlist_id(youtube_arg: str) -> str:
    for site in ["youtube.com", "youtu.be"]:
        if site in youtube_arg:
            return url_to_id(youtube_arg, "yt")
    return youtube_arg


def get_spotify_playlist_id(spotify_arg: str, spotify_playlist_name: str) -> str:
    if spotify_arg:
        for site in ["spotify.com", "spotify:"]:
            if site in spotify_arg:
                return url_to_id(spotify_arg, "sp")
        return spotify_arg
    
    elif spotify_playlist_name:
        if not create_new:
            user_playlists = sp.get_user_playlists()
            for playlist in user_playlists:
                if playlist["name"] == spotify_playlist_name:
                    return playlist["id"]
        return sp.create_playlist(spotify_playlist_name)
    
    else:
        if not dryrun:
            return sp.create_playlist(yt.get_playlist_title())


def set_yt_thumbnail_as_sp_cover():
    thumbnail_url = yt.get_playlist_thumbnail()

    request.urlretrieve(thumbnail_url, "thumbnail.jpg")

    with open("thumbnail.jpg", "rb") as img:
        encoded_img = base64.b64encode(img.read())
        sp.set_playlist_cover(encoded_img)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-yt",
        "--youtube-url-or-id",
        type=str,
        default=None,
        required=True,
        help="Youtube Playlist URL or ID",
    )
    # parser.add_argument(
    #     "-o",
    #     "--output",
    #     type=str,
    #     default="~/Music/JSON",
    #     required=False,
    #     help="Destination location of JSON files",
    # )
    sp_group = parser.add_mutually_exclusive_group(required=False)
    sp_group.add_argument(
        "-sp",
        "--spotify-url-or-id",
        type=str,
        default=None,
        help="Spotify Playlist URL or ID",
    )
    sp_group.add_argument(
        "-spname",
        "--spotify-playlist-name",
        type=str,
        default=None,
        help="Spotify Playlist Name \
            (Default: Youtube Playlist Name)",
    )
    run_group = parser.add_mutually_exclusive_group(required=False)
    run_group.add_argument(
        "-n",
        "--create-new",
        action="store_true",
        required=False,
        default=False,
        help="Create a new playlist",
    )
    run_group.add_argument(
        "-d",
        "--dryrun",
        action="store_true",
        required=False,
        default=False,
        help="Do not add to Spotify",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=None,
        required=False,
        help="Limit the number of songs to fetch",
    )

    args = parser.parse_args()
    youtube = args.youtube_url_or_id
    spotify = args.spotify_url_or_id
    spotify_playlist_name = args.spotify_playlist_name
    dryrun = args.dryrun
    create_new = args.create_new
    limit = args.limit

    return youtube, spotify, spotify_playlist_name, dryrun, create_new, limit


if __name__ == "__main__":
    youtube_arg, spotify_arg, spotify_playlist_name, dryrun, create_new, limit = get_args()
    yt = YoutubeMusic()
    sp = Spotify()
    ytm2spt_logger = setup_logger(__name__)

    youtube_id = get_youtube_playlist_id(youtube_arg)
    ytm2spt_logger.info(f"Youtube Playlist ID: {youtube_id}")
    yt.set_playlist_id(youtube_id)
    ytm2spt_logger.info(f"Youtube Playlist Name: {yt.get_playlist_title()}")
    
    if dryrun:
        ytm2spt_logger.info("Dryrun mode enabled. No songs will be added to Spotify.")
    else:
        spotify_id = get_spotify_playlist_id(spotify_arg, spotify_playlist_name)
        ytm2spt_logger.info(f"Spotify Playlist ID: {spotify_id}")
        sp.set_playlist_id(spotify_id)
        ytm2spt_logger.info(f"Spotify Playlist Name: {sp.get_playlist_name()}")

        set_yt_thumbnail_as_sp_cover()
        ytm2spt_logger.info("Set playlist cover from youtube thumbnail")

        if not create_new:
            sp.set_playlist_description()
            ytm2spt_logger.info("Update playlist description")

    songs = yt.get_songs_from_playlist(limit)
    ytm2spt_logger.info(f"Got {len(songs)} songs from Youtube Playlist")
    total_songs_added = 0

    for song in songs:
        song_uri = sp.get_song_uri(song.artist, song.title)

        if not song_uri:
            ytm2spt_logger.error(f"{song.artist} - {song.title} was not found!")
            continue
        
        if dryrun:
            continue
        
        was_added = sp.add_song_to_playlist(song_uri)

        if was_added:
            ytm2spt_logger.info(
                f'{song.artist} - {song.title} was added to playlist.')
            total_songs_added += 1
    
    if not dryrun:
        

        ytm2spt_logger.info(f'Added {total_songs_added} songs out of {len(songs)}')
