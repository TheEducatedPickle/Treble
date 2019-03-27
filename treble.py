import sys
import spotipy
import os
import spotipy.util as util
import random
from collections import defaultdict
from PyLyrics import *
scope = 'user-library-read playlist-modify-public playlist-modify-private'

global sp

def list_of_artists():
    artists = set()
    for item in get_user_playlists()['items']:
        for a in sp.user_playlist(sys.argv[1],item['id'])['tracks']['items']:
            track_artist=a['track']['artists'][0]['id']
            artists.add(track_artist)
    return list(artists)

def create_playlist(name):
    curr_user_id=sp.current_user()['id']
    new_playlist=sp.user_playlist_create(curr_user_id,name,public=True)
    return new_playlist

def reorder_playlist(name):
    playlist = playlist_given_name(name)
    length =  len(sp.user_playlist(username,item['id'])['tracks']['items'])-1
    for i in range(1,length):
        random_number=random.randint(1,length)
        while random_number!=i:
            random_number=random.randint(1,length)
        sp.user_playlist_reorder_track(sp.current_user()['id'],playlist['id'],i,random_number,1,snapshot_id=None)

def playlist_from_rec(name):
    playlist = playlist_given_name(name)
    lists = list(list_of_artists())
    lists = lists[:5]
    for item in sp.recommendations(seed_artists=lists,seed_genres=None,seed_tracks=None,limit=100,country=None)['tracks']:
        uris = []
        uris.append(item['uri'])
        sp.user_playlist_add_tracks(sp.current_user()['id'],playlist['id'],uris,position=None)

def recs_by_genre(name, genres=None):
    if genres==None:
        playlist_from_rec(name)
    else:
        playlist = playlist_given_name(name)
        lists = list(list_of_artists())
        lists = lists[:5]
        for item in sp.recommendations(seed_artists=lists,seed_genres=None,seed_tracks=None,limit=100,country=None)['tracks']:
            print(item)
            uris = []
            uris.append(item['uri'])
            sp.user_playlist_add_tracks(sp.current_user()['id'],playlist['id'],uris,position=None)

def playlist_given_name(target):
    for item in get_user_playlists()['items']:
        if item['name']==target:
            return item
    return create_playlist(target)
    
def get_user_playlists():
    playlists =sp.current_user_playlists(limit=50,offset=0)
    return playlists

def create_playlist_from_favorites(name):
    results = sp.current_user_saved_tracks()
    curr_user_id=sp.current_user()['id']
    fav_playlist = playlist_given_name(name)
    for item in results['items']:
        track = item['track']
        tracks = []
        tracks.append(track['uri'])
        temp = sp.user_playlist_add_tracks(curr_user_id,fav_playlist['id'],tracks,position=None)
        #print (track['name'] + ' - ' + track['artists'][0]['name'])

def get_lyrics(): #Creates a dict that maps artist to a list of song and lyric tuple
    artists_and_songs = defaultdict(list)
    for item in sp.current_user_saved_tracks()['items']:
        track = item['track']
        artist = track['artists'][0]['name']
        song = track['name']
        lyrics = None
        try:
            lyrics = PyLyrics.getLyrics(artist,song)
            print("Lyrics were found for", song, "by", artist)
        except:
            print("Lyrics were not found for ", song, " by ", artist)
        artists_and_songs[artist].append((song, lyrics))
        return artists_and_songs #TODO: Return at end of for loop instead when not testing

def get_lyric_map():
    artist_to_song_lyric = get_lyrics()
    reverse_search_map = {}
    for artist, tracks in artist_to_song_lyric.items():
        for tup in tracks:
            if tup[1] is not None:
                reverse_search_map[tup[1]] = (artist, tup[0])
    return artist_to_song_lyric, reverse_search_map

if __name__ == "__main__":
    global sp
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: ",sys.argv[0], "username")
        sys.exit()

    token = util.prompt_for_user_token(username, scope)
    if not token: 
        print ("Can't get token for", username)
    sp = spotipy.Spotify(auth=token)

    #create_playlist_from_favorites(sp,"Favorites")
    artist_to_song_lyric_tuple, reverse_search_map = get_lyric_map()
    print(reverse_search_map)
    #recs_by_genre("Rec")
    