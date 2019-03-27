import sys
import spotipy
import os
import spotipy.util as util
import random
scope = 'user-library-read playlist-modify-public playlist-modify-private'

def list_of_artists(sp):
    artists = set()
    for item in get_user_playlists(sp)['items']:
        for a in sp.user_playlist(sys.argv[1],item['id'])['tracks']['items']:
            track_artist=a['track']['artists'][0]['id']
            artists.add(track_artist)
    return list(artists)

def create_playlist(sp,name):
        curr_user_id=sp.current_user()['id']
        new_playlist=sp.user_playlist_create(curr_user_id,name,public=True)
        return new_playlist

def reorder_playlist(sp,name):
        playlist = playlist_given_name(sp,name)
        length =  len(sp.user_playlist(username,item['id'])['tracks']['items'])-1
        for i in range(1,length):
            random_number=random.randint(1,length)
            while random_number!=i:
                random_number=random.randint(1,length)
            sp.user_playlist_reorder_track(sp.current_user()['id'],playlist['id'],i,random_number,1,snapshot_id=None)

def playlist_from_rec(sp,name):
    playlist = playlist_given_name(sp,name)
    lists = list(list_of_artists(sp))
    lists = lists[:5]
    for item in sp.recommendations(seed_artists=lists,seed_genres=None,seed_tracks=None,limit=100,country=None)['tracks']:
        uris = []
        uris.append(item['uri'])
        sp.user_playlist_add_tracks(sp.current_user()['id'],playlist['id'],uris,position=None)

def recs_by_genre(sp, name, genres=None):
    if genres==None:
        playlist_from_rec(sp, name)
    else:
        playlist = playlist_given_name(sp,name)
        lists = list(list_of_artists(sp))
        lists = lists[:5]
        for item in sp.recommendations(seed_artists=lists,seed_genres=None,seed_tracks=None,limit=100,country=None)['tracks']:
            print(item)
            uris = []
            uris.append(item['uri'])
            sp.user_playlist_add_tracks(sp.current_user()['id'],playlist['id'],uris,position=None)

def playlist_given_name(sp, target):
    for item in get_user_playlists(sp)['items']:
        if item['name']==target:
            return item
    return create_playlist(sp,target)
    
def get_user_playlists(sp):
    playlists =sp.current_user_playlists(limit=50,offset=0)
    return playlists

def create_playlist_from_favorites(sp,name):
        results = sp.current_user_saved_tracks()
        curr_user_id=sp.current_user()['id']
        fav_playlist = playlist_given_name(sp,name)
        for item in results['items']:
            track = item['track']
            tracks = []
            tracks.append(track['uri'])
            temp = sp.user_playlist_add_tracks(curr_user_id,fav_playlist['id'],tracks,position=None)
            #print(track['artists'])
            #print (track['name'] + ' - ' + track['artists'][0]['name'])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: ",sys.argv[0], "username")
        sys.exit()

    token = util.prompt_for_user_token(username, scope)
    if not token: 
        print ("Can't get token for", username)
    sp = spotipy.Spotify(auth=token)

    create_playlist_from_favorites(sp,"Favorites")
    recs_by_genre(sp,"Rec")
    #print(sp.recommendation_genre_seeds())
    #for item in get_user_playlists(token)['items']:
        #print(item['name'])
        #print()
        #for a in sp.user_playlist(username,item['id'])['tracks']['items']:
            #print()
            #track_name = a['track']['name']
            #track_artist=a['track']['artists'][0]['name']
            #print(a['track']['name'])
            #print(a['track']['artists'][0].keys())
            #print(a['track']['artists'][0]['name'])
            #print(sp.audio_features(a['track']['id'])[0])
        #print(len(sp.user_playlist(username,item['id'])['tracks']['items']))
        #print()
    #create_playlist_from_favorites(token)
    