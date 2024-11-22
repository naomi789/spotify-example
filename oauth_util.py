from authlib.integrations.requests_client import OAuth2Session

from keys import spotify_client_id, spotify_client_secret # Keep these in a separate file
# All the possible scopes are listed here:
# https://developer.spotify.com/documentation/general/guides/authorization/scopes/
scope = "playlist-read-private"

# Get user to authorize the client: You may need to add the redirect URL from your app dashboard
client = OAuth2Session(spotify_client_id, spotify_client_secret, scope=scope, redirect_uri="http://sayamindu.pythonanywhere.com/spotify")
authorization_endpoint = "https://accounts.spotify.com/authorize"
uri, state = client.create_authorization_url(authorization_endpoint)
print("Please go to this URL in your web browser and follow the prompts:{}".format(uri))

# Get the authorization response back
authorization_response = input("Once you are redirected by your browser, copy the URL from your browser's address bar and enter it here:")

# Get the token
token_endpoint = "https://accounts.spotify.com/api/token"
token = client.fetch_token(token_endpoint, authorization_response=authorization_response)

# Get data with the token
api_endpoint = "https://api.spotify.com/v1"
resp = client.get(api_endpoint + "/me/playlists")
print(resp.text) # JSON data that you can do things with
