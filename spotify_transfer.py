import spotipy
import youtube_search as ytsearch
import create_playlist as ytplaylist
import insert_playlist as ytinsert
from spotipy.oauth2 import SpotifyClientCredentials


file = r'ids.txt'
scope = 'playlist-read-private'

with open(file, 'r') as credentials_file:
    client_id = credentials_file.readline()
    client_secret = credentials_file.readline()
    client_id = client_id[:-1]
    client_secret = client_secret[:-1]

print('[Prompt for the token]')
username = str(input('Gib me your username: '))
try:
    token = spotipy.util.prompt_for_user_token(username,
                                                scope,
                                                client_id,
                                                client_secret,
                                                'https://google.com/')
    print('[!] Access Authorized')
except:
    print('ERRO!')

# This method will call all the funcions from the youtube_search module
# so the program can get the video id from the music name
def get_music(music_name):
    youtube = ytsearch.youtube_search()
    search_response = ytsearch.search_musics(youtube, music_name)
    music_id = ytsearch.get_music_id(search_response)
    print("Music ID:", music_id)
    return music_id

# This method will receive a list with all the musics in a playlist
# and will pass each value(name) to get_music method and will return a lists
# with all the music id from the playlist
def get_music_from_list_and_search(music_list):
    musics_id_list = []
    for i in range(len(music_list)):
        print('music name: ', music_list[i])
        music_id = get_music(music_list[i])
        musics_id_list.append(music_id)
    print(musics_id_list)
    return musics_id_list

# This method will ask the user which playlist will be transfered to youtube
# and returns a list with the number of the playlist
def ask_playlist():
    list = []
    numbers = input("Choose the playlists: ")
    list = numbers.split(' ')
    return list

def show_tracks(tracks):
    playlist_musics = []
    for i, item in enumerate(tracks['items']):
        track = item['track']
        playlist_musics.append(track['artists'][0]['name'] + " - " + track['name'])

    print("Playlist musics:", playlist_musics)
    print("Searching ...\n\n")
    musics_id_list = get_music_from_list_and_search(playlist_musics)
    return musics_id_list

def read_playlist(token, username):
    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(username)
    i = 0
    for playlist in playlists['items']:
       print('\n {0} - '.format(i), playlist['name'])
       print('\ttotal tracks', playlist['tracks']['total'])
       i += 1

    playlists_to_transfer = ask_playlist()
    print()
    for l in range(len(playlists_to_transfer)):
        sp_playlist_name = playlists['items'][int(playlists_to_transfer[l])]['name']
        print('\n', sp_playlist_name)
        results = sp.playlist(playlists['items'][int(playlists_to_transfer[l])]['id'], fields="tracks,next")
        tracks = results['tracks']
        musics_id_list = show_tracks(tracks)
        # HERE STARTS TO SEND THE VIDEOS TO YOUTUBE
        yt_playlist_id = ytplaylist.create_playlist(sp_playlist_name)
        ytinsert.send_to_ytplaylist(ytinsert.youtube, yt_playlist_id, musics_id_list)

        # while tracks['next']:
        #     print("comeco do while")
        #     tracks = sp.next(tracks)
        #     show_tracks(tracks)
        #     print("fim do while")


if __name__ == "__main__":
    read_playlist(token, username)
else:
    print("You need to run spotify_transfer.py")
