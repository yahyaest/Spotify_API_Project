import json
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError
import oauth
import sqlite3
from twilio.rest import Client
from oauth import account_sid, auth_token, my_cell, my_twilio

conn = sqlite3.connect('Recently_played.sqlite')
cur = conn.cursor()

# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Recently_played;

CREATE TABLE Recently_played (
    id  INTEGER NOT NULL PRIMARY KEY
        AUTOINCREMENT UNIQUE,
    track TEXT  UNIQUE,
    artist TEXT,
    album TEXT
);
''')

username = 'd5gqzzfewfdefoiyrwa6yvgq7'
scope = 'user-read-recently-played'
token = util.prompt_for_user_token(username, scope, oauth.client_id, oauth.client_secret, oauth.redirect_uri)


#Create our spotifyObject
spotifyObject = spotipy.Spotify(auth=token)

# Display lastest 50 played tracks
CurrentUserRecentlyPlayed = spotifyObject.current_user_recently_played(limit=20)
CurrentUserRecentlyPlayed = CurrentUserRecentlyPlayed['items']

i = 1
my_msg = ""
for item in CurrentUserRecentlyPlayed:
    track_name = item['track']['name']
    track_artist = item['track']['artists'][0]['name']
    track_album = item['track']['album']['name']

    print(i, "-", track_name, " by ", track_artist)
    current_msg = str(i) + " - " + track_name + " by " + track_artist
    # print(current_msg)
    my_msg = my_msg + current_msg + "\n"
    i = i + 1

    cur.execute('''INSERT OR IGNORE INTO Recently_played (track, artist, album)
        VALUES ( ?, ?, ? )''', ( track_name, track_artist, track_album) )

conn.commit()

client = Client(account_sid, auth_token)
message = client.messages.create(to=my_cell, from_=my_twilio, body=my_msg)
