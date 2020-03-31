import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import oauth

#Create our spotifyObject
username = 'd5gqzzfewfdefoiyrwa6yvgq7'
scope = 'playlist-modify-public'

token = util.prompt_for_user_token(username, scope, oauth.client_id, oauth.client_secret, oauth.redirect_uri)

spotifyObject = spotipy.Spotify(auth=token)

#Get user playlists
playlists = spotifyObject.user_playlists(username)

user_playlist_name = list()
user_playlist_id = list()

print("\nuser playlists :\n")

i = 0
for playlist in playlists['items']:
    #print(json.dumps(playlist, sort_keys=True, indent=4))
    #print(playlists)
    playlist_name = playlists['items'][i]['name']
    playlist_id = playlists['items'][i]['id']
    user_playlist_name.append(playlist_name)
    user_playlist_id.append(playlist_id)
    print(i , '-', playlist_name)
    i = i + 1

# Add tracks to a playlist
playlist_tag = input("Chose a playlist to add a track to it: ")
#assert playlist_tag is int

while int(playlist_tag) >= len(user_playlist_id):
    playlist_tag = input("Chose a playlist to add a track to it: ")

username = 'd5gqzzfewfdefoiyrwa6yvgq7'
playlist_id = user_playlist_id[int(playlist_tag)]

playlist_name = user_playlist_name[int(playlist_tag)]

if len(sys.argv) > 1:
    track_ids = sys.argv[1:]
else:
    print("Usage: %s username playlist_id track_id ..." % (sys.argv[0],))
    sys.exit()

scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope, oauth.client_id, oauth.client_secret, oauth.redirect_uri)

if token:
    spotifyObject.trace = False
    results = spotifyObject.user_playlist_add_tracks(username, playlist_id, track_ids)
    print(results)
else:
    print("Can't get token for", username)
