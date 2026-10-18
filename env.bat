@echo off

@REM Remove the  < and > characters when setting the actual values.
set SPOTIFY_CLIENT_ID=<your_client_id>
set SPOTIFY_CLIENT_SECRET=<your_client_secret>
set SPOTIFY_REDIRECT_URI=http://localhost:8888/callback

setx SPOTIFY_CLIENT_ID %SPOTIFY_CLIENT_ID%
setx SPOTIFY_CLIENT_SECRET %SPOTIFY_CLIENT_SECRET%
setx SPOTIFY_REDIRECT_URI %SPOTIFY_REDIRECT_URI%
