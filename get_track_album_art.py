import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import oauth


username = 'd5gqzzfewfdefoiyrwa6yvgq7'
token = util.prompt_for_user_token(username, oauth.scope, oauth.client_id, oauth.client_secret, oauth.redirect_uri)


#Create our spotifyObject
spotifyObject = spotipy.Spotify(auth=token)

#Get user informations
user = spotifyObject.current_user()
#print(json.dumps(user, sort_keys=True, indent=4))
display_name = user['display_name']
followers = user['followers']['total']

#Get user playlists
while True:
    print()
    print(">>> Welcome to Spotify " + display_name + "!")
    print(">>> You have " + str(followers) + " followers.")
    print()
    print("0 - Search for an artist")
    print("1 - exit")
    choice = input("Your choice: ")

    #Search for the artist
    if choice == "0":
        print()
        searchQuery = input("Ok, what's their name?: ")
        print()

        # Get seach result
        searchResults = spotifyObject.search(searchQuery,1,0,"artist")
        #print(json.dumps(searchResults, sort_keys=True, indent=4))

        # Artist details
        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        print(str(artist['followers']['total']) + " followers")
        print(artist['genres'][0])
        print()
        webbrowser.open(artist['images'][0]['url'])
        artistID = artist['id']

        # Albums and Tracks
        trackURIs = []
        trackArt = []
        z = 0

        # Extract album data
        albumResults = spotifyObject.artist_albums(artistID)
        #print(json.dumps(albumResult, sort_keys=True, indent=4))
        # OR a btterr version is to automate the json dumps methode by creting a json file
        #f = open("album_search.json", "w+")
        #f.write(json.dumps(albumResults, sort_keys=True, indent=4))
        #f.close()
        albumResults = albumResults['items']

        for item in albumResults:
            print("ALBUM " + item['name'])
            albumID = item['id']
            albumArt = item['images'][0]['url']

            # Extract track data
            trackResults = spotifyObject.album_tracks(albumID)
            #f = open("track_search.json", "w+")
            #f.write(json.dumps(trackResults, sort_keys=True, indent=4))
            #f.close()
            trackResults = trackResults['items']

            for item in trackResults:
                print(str(z) + ": " + item['name'])
                trackURIs.append(item['uri'])
                trackArt.append(albumArt)
                z+=1
            print()

        # See album art
        while True:
            SongSelection = input("Enter a song number to see the album art associated with it (x to exit): ")
            if SongSelection == "x":
                break
            webbrowser.open(trackArt[int(SongSelection)])

    #End the program
    if choice == "1":
        break
