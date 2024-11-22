import json

from flask import Flask, redirect, session, url_for
from authlib.integrations.flask_client import OAuth

from keys import secret_key, spotify_client_id, spotify_client_secret

app = Flask(__name__)
app.secret_key = secret_key

oauth = OAuth(app)
oauth.register(
   name="spotify",
   client_id=spotify_client_id,
   client_secret=spotify_client_secret,
   authorize_url="https://accounts.spotify.com/authorize",
   access_token_url="https://accounts.spotify.com/api/token",
   api_base_url="https://api.spotify.com/v1/",
   client_kwargs={
       'scope': 'playlist-read-private user-top-read'
   }
)

@app.route("/login")
def login():
   redirect_uri = url_for('authorize', _external=True)
   print(redirect_uri)
   return oauth.spotify.authorize_redirect(redirect_uri)


@app.route("/spotify-authorize")
def authorize():
   token = oauth.spotify.authorize_access_token()
   session["spotify-token"] = token
   return token


@app.route("/")
def index():
   try:
       token = session["spotify-token"]
   except KeyError:
       return redirect(url_for("login"))
   data = oauth.spotify.get("me/top/tracks?limit=5", token=token).text
   return json.loads(data)

if __name__ == "__main__":
    app.run(debug=True)