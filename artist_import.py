import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import oauth
import json

#This code uses Spotify API to get the albums and the tracks related to them of the artist breaking benjamin

# breaking benjamin spotify uri
breaking_benjamin_uri = 'spotify:artist:5BtHciL0e0zOP7prIHn3pP'

#Create a spotify object from class Spotify
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(oauth.client_id, oauth.client_secret))

#create variable that get the artist albums
results = spotify.artist_albums(breaking_benjamin_uri, album_type='album')
#print(json.dumps(results, sort_keys=True, indent=4))

#Print the introduction phrase
print('Here is Breaking Benjamin Albums and Tracks')

albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print('\n', album['name'], '\n')
    album_uri = album['uri']
    #create variable that get the album tracks
    track_results = spotify.album_tracks(album_uri)
    #print(json.dumps(track_results, sort_keys=True, indent=4))
    tracks = track_results['items']
    i = 0
    for track in tracks:
        print('     ', i + 1,  '-', tracks[i]['name'])
        i = i + 1
