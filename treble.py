import sys
import spotipy
import spotipy.util as util
try:
	import configparser
except:
	import ConfigParser


config = configparser.ConfigParser()

def show_tracks(results):
    for i, item in enumerate(results['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'], track['name']))

def configure():
    global SPOTIFY_CLIENT_ID
    global SPOTIPY_CLIENT_SECRET
    global SPOTIPY_REDIRECT_URI
    config.read('config.ini')
    SPOTIFY_CLIENT_ID = config['AUTH']['SPOTIPY_CLIENT_ID']
    SPOTIPY_CLIENT_SECRET = config['AUTH']['SPOTIPY_CLIENT_SECRET']
    SPOTIPY_REDIRECT_URI = config['AUTH']['SPOTIPY_REDIRECT_URI']

def main():
    configure()
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Whoops, need your username!")
        print("usage: python user_playlists_contents.py [username]")
        sys.exit()

    token = util.prompt_for_user_token(username)

    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == username:
                print()
                print(playlist['name'])
                print('  total tracks', playlist['tracks']['total'])
                results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
                tracks = results['tracks']
                show_tracks(tracks)
                while tracks['next']:
                    tracks = sp.next(tracks)
                    show_tracks(tracks)
    else:
        print("Can't get token for", username)

if __name__ == '__main__':
    main()
