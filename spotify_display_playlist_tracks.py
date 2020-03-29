import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import oauth

# shows a user's playlists (need to be authenticated via oauth)

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name']))


if __name__ == '__main__':
    username = 'd5gqzzfewfdefoiyrwa6yvgq7'
    token = util.prompt_for_user_token(username, oauth.scope, oauth.client_id, oauth.client_secret, oauth.redirect_uri)

    if token:
        #Create our spotifyObject
        sp = spotipy.Spotify(auth=token)

        playlists = sp.user_playlists(username)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == username:
                #print(playlist) # to get the playlist json code
                print()
                print(playlist['name'])
                print ('  total tracks', playlist['tracks']['total'])
                results = sp.playlist(playlist['id'],
                    fields="tracks,next")
                tracks = results['tracks']
                show_tracks(tracks)
                while tracks['next']:
                    tracks = sp.next(tracks)
                    show_tracks(tracks)
    else:
        print("Can't get token for", username)
