import spotipy
import spotipy.util as util
import oauth

print('\nYour saved tracks :\n')
scope = 'user-library-read'

username = 'd5gqzzfewfdefoiyrwa6yvgq7'

token = util.prompt_for_user_token(username, scope, oauth.client_id, oauth.client_secret, oauth.redirect_uri)

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks(limit=50)
    i = 0
    for item in results['items']:
        i = i + 1
        track = item['track']
        print(i, '-', track['name'] + ' - ' + track['artists'][0]['name'])
else:
    print("Can't get token for", username)
