# playlist(playlist_id, fields=None, market=None)
# current_user_playlists(limit=50, offset=0)
# playlist_cover_image(playlist_id)
# playlist_upload_cover_image(playlist_id, image_b64)
#
# current_user_followed_artists(limit=20, after=None)
#
# current_playback(market=None) : Done
# pause_playback(device_id=None) :Premium required
# next_track(device_id=None)   :Premium required
# previous_track(device_id=None) :Premium required
# currently_playing(market=None) :Done
# current_user_recently_played(limit=50, after=None, before=None) : Done

import json
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError
import oauth
from twilio.rest import Client
from oauth import account_sid, auth_token, my_cell, my_twilio

username = 'd5gqzzfewfdefoiyrwa6yvgq7'
scope = 'user-read-currently-playing'
token = util.prompt_for_user_token(username, scope, oauth.client_id, oauth.client_secret, oauth.redirect_uri)


#Create our spotifyObject
spotifyObject = spotipy.Spotify(auth=token)

# GET Currently Playing Track
CurrentlyPlaying = spotifyObject.currently_playing()
#print(json.dumps(CurrentlyPlaying, sort_keys=True, indent=4))
print("Your are listening to: ", CurrentlyPlaying['item']['name'], " by ", CurrentlyPlaying['item']['artists'][0]['name'])
#Send currently playing track as an sms my_msg
client = Client(account_sid, auth_token)
my_msg = "Your are listening to: " + CurrentlyPlaying['item']['name'] + " by " + CurrentlyPlaying['item']['artists'][0]['name']
message = client.messages.create(to=my_cell, from_=my_twilio, body=my_msg)

# Same as CurrentlyPlaying
# scope = 'user-read-playback-state'
# token = util.prompt_for_user_token(username, scope, oauth.client_id, oauth.client_secret, oauth.redirect_uri)
# spotifyObject = spotipy.Spotify(auth=token)
# CurrentPlayback = spotifyObject.current_playback()
# print(json.dumps(CurrentPlayback, sort_keys=True, indent=4))
