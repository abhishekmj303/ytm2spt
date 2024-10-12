import argparse
from .transfer import transfer_playlist

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
    parser.add_argument(
        "-ytauth",
        "--youtube-oauth-json",
        type=str,
        default=None,
        required=False,
        help="Youtube OAuth JSON filepath (run 'ytmusicapi oauth')"
    )
    run_group = parser.add_mutually_exclusive_group(required=False)
    run_group.add_argument(
        "-n",
        "--create-new",
        action="store_true",
        required=False,
        default=False,
        help="Force create a new playlist",
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
    youtube_oauth = args.youtube_oauth_json
    spotify = args.spotify_url_or_id
    spotify_playlist_name = args.spotify_playlist_name
    dryrun = args.dryrun
    create_new = args.create_new
    limit = args.limit

    return youtube, spotify, spotify_playlist_name, youtube_oauth, dryrun, create_new, limit


def oauth():
    import os
    import platform
    from ytmusicapi import setup_oauth

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b",
        "--open-browser",
        action="store_true",
        required=False,
        default=None,
        help="open browser for OAuth login (Default: True)",
    )
    parser.add_argument(
        "file",
        nargs="?",
        type=str,
        default="ytmusicapi-oauth.json",
        help="file path to store the json (Default: ytmusic-oauth.json)",
    )

    args = parser.parse_args()
    file = args.file
    open_browser = args.open_browser
    if open_browser is None:
        open_browser = True
        if platform.system() == "Linux" and not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")):
            open_browser = False
    
    print(file)
    setup_oauth(filepath=file, open_browser=open_browser)


def main():
    transfer_playlist(*get_args())


if __name__ == "__main__":
    main()