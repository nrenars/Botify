import spotipy
from spotipy.oauth2 import SpotifyOAuth
from os import getenv
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = getenv("CLIENT_ID")
CLIENT_SECRET = getenv("CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="http://127.0.0.1:8080",
    scope="user-modify-playback-state user-read-playback-state"
))

track_uri = "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b?si=81322eb1e6ff48ee"
sp.add_to_queue(track_uri)
print("Dziesma pievienota rindai!")

# URI spotify:track:0FIDCNYYjNvPVimz5icugS
# URL https://open.spotify.com/track/0FIDCNYYjNvPVimz5icugS?si=cd6eca9b71f4419b
# ID 0FIDCNYYjNvPVimz5icugS