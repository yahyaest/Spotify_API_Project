import json
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError
import oauth
from twilio.rest import Client
from oauth import account_sid, auth_token, my_cell, my_twilio

#Create our spotifyObject
username = 'd5gqzzfewfdefoiyrwa6yvgq7'
scope = 'playlist-modify-public playlist-read-private'

token = util.prompt_for_user_token(username, scope, oauth.client_id, oauth.client_secret, oauth.redirect_uri)

spotifyObject = spotipy.Spotify(auth=token)

#Get user informations
user = spotifyObject.current_user()
display_name = user['display_name']

#Get user playlists
while True:
    print()
    print(">>> Welcome to Spotify " + display_name + "!")

    print()
    print("0 - To add a track : Search for an artist")
    print("1 - exit")
    choice = input("Your choice: ")

    #Search for the artist
    if choice == "0":
        print()
        searchQuery = input("Ok, what's their name?: ")
        print()

        # Get seach result
        searchResults = spotifyObject.search(searchQuery,1,0,"artist")

        # Artist details
        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        print(str(artist['followers']['total']) + " followers")
        print(artist['genres'][0])
        print()
        artistID = artist['id']

        # Albums and Tracks
        trackIDs = []
        trackNames = []
        z = 0

        # Extract album data
        albumResults = spotifyObject.artist_albums(artistID)
        albumResults = albumResults['items']

        for item in albumResults:
            print("ALBUM " + item['name'])
            albumID = item['id']

            # Extract track data
            trackResults = spotifyObject.album_tracks(albumID)
            trackResults = trackResults['items']

            for item in trackResults:
                print(str(z) + ": " + item['name'])
                trackIDs.append(item['id'])
                trackNames.append(item['name'])
                z+=1
            print()

        # Add the track to a playlist
        while True:
            SongSelection = input("Enter a song number to add it to a playlist (x to exit): ")
            if SongSelection == "x":
                break
            #Get user playlists
            playlists = spotifyObject.user_playlists(username)

            user_playlist_name = list()
            user_playlist_id = list()

            print()
            print("user playlists : ")
            print()

            i = 0
            for playlist in playlists['items']:
                playlist_name = playlists['items'][i]['name']
                playlist_id = playlists['items'][i]['id']
                user_playlist_name.append(playlist_name)
                user_playlist_id.append(playlist_id)
                print(i , '-', playlist_name)
                i = i + 1

            playlist_tag = input("Choose a playlist to add a track to it: ")

            while int(playlist_tag) >= len(user_playlist_id):
                playlist_tag = input("Chose a playlist to add a track to it: ")

            username = 'd5gqzzfewfdefoiyrwa6yvgq7'
            playlist_id = user_playlist_id[int(playlist_tag)]
            track_ids = [trackIDs[int(SongSelection)]]

            playlist_name = user_playlist_name[int(playlist_tag)]
            track_name = trackNames[int(SongSelection)]

            results = spotifyObject.user_playlist_add_tracks(username, playlist_id, track_ids)
            #print(results)
            print(track_name + " by " + artist['name'] + " has been added to this playlist : " + playlist_name)
            #Send added track as an sms my_msg
            client = Client(account_sid, auth_token)
            my_msg = track_name + " by " + artist['name'] + " has been added to this playlist : " + playlist_name
            message = client.messages.create(to=my_cell, from_=my_twilio, body=my_msg)


    #End the program
    if choice == "1":
        break
