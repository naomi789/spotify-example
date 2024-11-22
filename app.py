import json
from flask import Flask, request, redirect, g, render_template
import requests
from urllib.parse import quote
from keys import spotify_client_id, spotify_client_secret, secret_key


app = Flask(__name__)

#  Client Keys
CLIENT_ID = spotify_client_id
CLIENT_SECRET = spotify_client_secret

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8080
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
# SCOPE = "playlist-modify-public playlist-modify-private"
SCOPE = "user-top-read"

STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}


@app.route("/")
def index():
    # Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@app.route("/callback/q")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}

    top_tracks_api_endpoint = "{}/me/top/tracks?limit=5".format(SPOTIFY_API_URL)
    top_tracks_response = requests.get(top_tracks_api_endpoint, headers=authorization_header)
    top_tracks = json.loads(top_tracks_response.text)

    top_tracks = top_tracks['items']
    artist_song_names = []
    for track in top_tracks:
        artist = track['artists'][0]['name']
        song_name = track['name']
        print(f'{artist}, {song_name}\n\n\n')
        artist_song_names.append((artist, song_name))

    return render_template("index.html", sorted_array=artist_song_names)


if __name__ == "__main__":
    app.run(debug=True, port=PORT)