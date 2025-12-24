<h1 align="center">
   YouTube Music To Spotify
</h1>

<p align="center">
   <a href="https://github.com/abhishekmj303/ytm2spt/stargazers"><img src="https://img.shields.io/github/stars/abhishekmj303/ytm2spt?colorA=363a4f&colorB=b7bdf8&style=for-the-badge"></a>
   <a href="https://github.com/abhishekmj303/ytm2spt/releases/latest"><img src="https://img.shields.io/github/v/release/abhishekmj303/ytm2spt?colorA=363a4f&colorB=a6da95&style=for-the-badge"></a>
   <a href="https://github.com/abhishekmj303/ytm2spt/releases"><img src="https://img.shields.io/github/downloads/abhishekmj303/ytm2spt/total?colorA=363a4f&colorB=f5a97f&style=for-the-badge"></a>
</p>

<p align="center">
   An open-source app for effortlessly transferring playlists from YouTube Music to Spotify.
</p>

<p align="center">
   <img src="https://raw.githubusercontent.com/abhishekmj303/ytm2spt/refs/heads/main/media/app_ui.png">
</p>


## Features

- [x] No limit on size of playlist
- [x] Support public playlists
- [x] Support private playlists
- [x] Auto create or update playlist if it already exists
- [x] Use fuzzy search to find the best match
- [x] Copy playlist thumbnail from youtube to spotify
- [ ] Copy playlist description from youtube to spotify
- [x] Limit number of songs to be imported in the playlist
- [x] Dry run mode to test without adding to spotify


## Setup

### Spotify Developer Account

**Why?**

By setting up a Developer account and creating your own credentials (like keys), you are ensuring that the app connects to your account in a safe way without sharing your login details with anyone. It gives you full control over what the app can access and helps keep your Spotify account secure.

1. Create a new app: https://developer.spotify.com/dashboard
2. Set "Redirect URI" to `http://127.0.0.1:8888/callback`
   ![Spotify create new app](https://raw.githubusercontent.com/abhishekmj303/ytm2spt/refs/heads/main/media/spotify_create_app.png)
3. Copy the "Client ID" and "Client Secret" to use later
   ![Spotify settings](https://raw.githubusercontent.com/abhishekmj303/ytm2spt/refs/heads/main/media/spotify_settings.png)
   ![Spotify credentials](https://raw.githubusercontent.com/abhishekmj303/ytm2spt/refs/heads/main/media/spotify_credentials.png)
4. Copy the "User ID" from your Spotify account: https://www.spotify.com/in-en/account/profile/
   ![Spotify username](https://raw.githubusercontent.com/abhishekmj303/ytm2spt/refs/heads/main/media/spotify_username.png)


## Installation

Download the latest version from the following links:

<table>
  <tr>
    <td><a href="https://github.com/abhishekmj303/ytm2spt/releases/latest/download/ytm2spt-linux.tar.gz"><img src="https://img.shields.io/badge/Linux-363a4f?style=for-the-badge&logo=linux&logoColor=white" alt="Linux"></a></td>
    <td><a href="https://github.com/abhishekmj303/ytm2spt/releases/latest/download/ytm2spt-windows.zip"><img src="https://img.shields.io/badge/Windows-363a4f?style=for-the-badge&logo=windows&logoColor=white" alt="Windows"></a></td>
    <td><a href="https://github.com/abhishekmj303/ytm2spt/releases/latest/download/ytm2spt-macos.zip"><img src="https://img.shields.io/badge/Mac OS-363a4f?style=for-the-badge&logo=apple&logoColor=white" alt="MacOS"></a></td>
  </tr>
</table>


> [!NOTE]<br>
> **Windows**: Windows Defender may interrupt the app from running. Click on more info and allow the program to run.
>
> **Linux**: You need to run the app from terminal, if you want the to know the progress of the transfer.

**Using pip or [pipx](https://github.com/pypa/pipx#install-pipx):**

[![PyPI - Version](https://img.shields.io/pypi/v/ytm2spt?colorA=363a4f&colorB=c6a0f6&style=for-the-badge)](https://pypi.org/project/ytm2spt/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/ytm2spt?colorA=363a4f&colorB=f0c6c6&style=for-the-badge)](https://pypi.org/p/ytm2spt/)

If you have Python installed, you can install the app using [pipx](https://pipx.pypa.io/) (recommended) or pip.

```sh
pipx install ytm2spt
```

or

```sh
pip install ytm2spt
```

After installation, you can run the app using the command `ytm2spt`.

> [!CAUTION]<br>
> While syncing into an existing spotify playlist, first all the songs from Stopify playlist will be deleted and then the all the songs from YouTube Music playlist will be copied.


### Spotify Settings

When you run the executable, you will be prompted to enter your Spotify credentials.

![Spotify Settings](media/spotify_ui.png)

### Youtube Settings

To access private playlists, you need to log in to YouTube. You can use either Browser authentication or OAuth authentication. Please choose one method to log in.

#### Browser authentication

1. Refer to [Browser authentication](https://ytmusicapi.readthedocs.io/en/stable/setup/browser.html) to create a `browser.json` file.

2. Enter the path to the generated `browser.json` file in the **JSON File Path** field. 

3. **Client ID** and **Client Secret** must be left empty.  
![Youtube Settings](media/youtube_browser.png)

4. Close the dialog.

#### OAuth authentication

**Warning!** OAuth authentication is currently unavailable due to an [issue](https://github.com/sigma67/ytmusicapi/issues/813) with the ytmusicapi library!

1. Refer to the [YouTube Data API docs](https://developers.google.com/youtube/registering_an_application) and select `TVs and Limited Input devices` to create an `OAuth client ID`. You will need to obtain a `client_id` and `client_secret`.

2. Enter the generated `client_id` and `client_secret`.  
![Youtube Settings](media/youtube_oauth.png)

3. Click the `Get OAuth Token` button. The YouTube OAuth token will be saved to the path specified in `JSON File Path`.

4. When the authentication is completed close the dialog.

[reference](https://ytmusicapi.readthedocs.io/en/stable/setup/oauth.html)

> [!TIP]<br>
> If you find this project useful or interesting, please consider giving it a 🌟star! It helps others discover it too!

---

## GUI

Python3 is required to run the app. You can download it from [python.org](https://www.python.org/downloads/) for Windows.

### Install Dependencies
```sh
pip install .
```

### Run the App
```sh
python ytm2spt.py
```

## CLI

### Setting Environment Variables Linux and Mac

1. Rename the file `.env.sample` to `.env`
2. Edit the file by adding your credentials
3. Run the following command to set your environment variable: `source .env`


### Setting Environment Variables (Windows)

1. Edit `env.bat` file by adding your credentials in these lines
   ```bat
   set SPOTIFY_USER_ID=<your_user_id>
   set SPOTIFY_CLIENT_ID=<your_client_id>
   set SPOTIFY_CLIENT_SECRET=<your_client_secret>
   ```
2. Run the batch file to set your environment variable: 
   ```bat
   env.bat
   ```

>[!NOTE]<br>
> If the environment variables are not set, you may need to restart your terminal or IDE.

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Youtube OAuth (Only for private playlists)

Run the following command to login to your Youtube account and save the credentials to `ytmusicapi-oauth.json`
```sh
ytmusicapi-oauth
```

## Usage

```sh
$ source .env
$ ytm2spt -h
usage: ytm2spt [-h] -yt YOUTUBE_URL_OR_ID
               [-sp SPOTIFY_URL_OR_ID | -spname SPOTIFY_PLAYLIST_NAME]
               [-ytauth YOUTUBE_OAUTH_JSON]
               [-n | -d] [-l LIMIT]

options:
  -h, --help            show this help message and exit
  -yt YOUTUBE_URL_OR_ID, --youtube-url-or-id YOUTUBE_URL_OR_ID
                        Youtube Playlist URL or ID
  -sp SPOTIFY_URL_OR_ID, --spotify-url-or-id SPOTIFY_URL_OR_ID
                        Spotify Playlist URL or ID
  -spname SPOTIFY_PLAYLIST_NAME, --spotify-playlist-name SPOTIFY_PLAYLIST_NAME
                        Spotify Playlist Name (Default: Youtube Playlist Name)
  -ytauth YOUTUBE_OAUTH_JSON, --youtube-oauth-json YOUTUBE_OAUTH_JSON
                        Youtube OAuth JSON filepath (run 'ytmusicapi-oauth')
  -n, --create-new      Force create a new playlist
  -d, --dryrun          Do not add to Spotify
  -l LIMIT, --limit LIMIT
                        Limit the number of songs to fetch
```

```sh
$ ytmusicapi-oauth -h
usage: ytmusicapi-oauth [-h] [-b] [file]

positional arguments:
  file                file path to store the json (Default: ytmusic-oauth.json)

options:
  -h, --help          show this help message and exit
  -b, --open-browser  open browser for OAuth login (Default: True)
```

### Examples

Sample Playlist: Pop Certified ([YouTube Music](https://music.youtube.com/playlist?list=RDCLAK5uy_lBNUteBRencHzKelu5iDHwLF6mYqjL-JU) to [Spotify](https://open.spotify.com/playlist/6DyIxXHMwuEMbsfPTIr9C8))

```sh
# Pass any link containing a youtube playlist ID
# Sets same name as youtube playlist
$ python ytm2spt.py -yt "https://music.youtube.com/playlist?list=RDCLAK5uy_lBNUteBRencHzKelu5iDHwLF6mYqjL-JU"

# Pass just the youtube playlist ID
# Set a custom name for the playlist
$ python ytm2spt.py -yt "CLAK5uy_lBNUteBRencHzKelu5iDHwLF6mYqjL-JU" -spname "Pop Certified"

# Pass link of a private youtube playlist
# Provide the path to the oauth.json file
$ python ytm2spt.py -yt "https://music.youtube.com/playlist?list=PLz96m0PSfi9p8ABcEcUlSMVmz7sN-IEFu" -ytauth "oauth.json"

# Pass an existing spotify playlist URL or ID
# Limit the number of songs to fetch
# Dry run mode
$ python ytm2spt.py -yt "CLAK5uy_lBNUteBRencHzKelu5iDHwLF6mYqjL-JU" -sp "https://open.spotify.com/playlist/6DyIxXHMwuEMbsfPTIr9C8" -l 10 -d

# Pass even the URL of video playing from playlist
# Force create a new playlist
$ python ytm2spt.py -yt "https://www.youtube.com/watch?v=RlPNh_PBZb4&list=RDCLAK5uy_lBNUteBRencHzKelu5iDHwLF6mYqjL-JU" -n
```


## Build an Executable

**Note:** This is only required if you want to build the executable yourself. This is not necessary if you just need to run the app directly using Python.

**Requirements:**
- C Compiler (gcc, clang)
- `patchelf` (Linux only)
- `python3-devel` or similar package in your OS

```sh
pip install -r requirements-dev.txt
nuitka ytm2spt.py
```


> [!NOTE]<br>
> Forked from @edgarh22's [Youtube-to-Spotify-Archiver](https://github.com/edgarh92/Youtube-to-Spotify-Archiver).
