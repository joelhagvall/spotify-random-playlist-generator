import random

import PySimpleGUI as sg
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# First thing - authenticate with Spotify
client_id = "enter_your_client_id"
client_secret = "enter_your_client_secret"
redirect_uri = "enter_redirect_uri"
if client_id == "enter_your_client_id" or client_secret == "enter_your_client_secret":
    sg.popup("Please enter your client ID and client secret in the code.")
    exit()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope="playlist-modify-private"))

# Retrieves user playlists
playlists = sp.user_playlists(user="enter_your_spotify_username")['items'] # User: username
playlist_ids = [playlist['id'] for playlist in playlists]

# Layout in PySimpleGUI
sg.theme('BlueMono')

layout = [
    [sg.Text("How many tracks do you want to include in your playlist?")],
    [sg.Input(key="-NUM_TRACKS-")],
    [sg.Text("What would you like to name your playlist?")],
    [sg.Input(key="-PLAYLIST_NAME-")],
    [sg.Button("Generate Playlist")]
]

# Window in PySimpleGui
window = sg.Window("Spotify Playlist Generator", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "Generate Playlist":
        # Get the number of tracks from the user input
        num_tracks = int(values["-NUM_TRACKS-"])

        # Selects a random playlist ID
        playlist_id = random.choice(playlist_ids)

        # Retrieves tracks from playlists
        tracks = sp.playlist_tracks(playlist_id)['items'] 
        track_ids = [track['track']['id'] for track in tracks]

        # Selects random track IDs
        random_tracks = random.sample(population=track_ids,k=num_tracks)

        # Get the playlist name from the user input
        playlist_name = values["-PLAYLIST_NAME-"]

        # Creates a new playlist
        new_playlist = sp.user_playlist_create(user="enter_your_spotify_username", name=playlist_name, public=False)   # User: username

        # Adds tracks to new playlist created
        sp.playlist_add_items(new_playlist['id'], random_tracks)

        sg.popup("Random playlist generated! Check your Spotify :)")

window.close()