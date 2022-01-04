import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Press the green button in the gutter to run the script.
import secret

def authen():
    auth_manager = SpotifyClientCredentials(client_id=secret.CLIENT_ID, client_secret=secret.CLIEN_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp

def getListAudioFeature(sp, listId, timestr):
    audiofeatureList = sp.audio_features(listId)
    print(audiofeatureList)
    tracksList = sp.tracks(listId)
    print(tracksList)
    resuslt = list(map(lambda x, y: x | y, audiofeatureList, tracksList['tracks']))
    with open('data-'+ timestr +'.json', 'w+', encoding='utf-8') as f:
        json.dump(resuslt, f, ensure_ascii=False, indent=4)
    print(resuslt)

def getListTracks(sp, playlistId):
    limit = 50
    offset = 0
    tracks = sp.playlist_tracks(playlist_id=playlistId, limit=limit, offset=offset)["items"]
    count = 0
    while (tracks):
        for track in tracks:
            count = count + 1
            with open('data.json', 'w+', encoding='utf-8') as f:
                json.dump(track, f, ensure_ascii=False, indent=4)
        offset += limit
        tracks = sp.playlist_tracks(playlist_id=playlistId, limit=limit, offset=offset)["items"]
    # while tracks['next']:
    #     tracks = sp.next(tracks)
    #     count = count + 1
    #     print(tracks['items'])
    print(count)

def getPlaylist(sp):
    playlists = sp.user_playlists('spotify')
    count = 0
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            count = count + 1
            # print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'], playlist['name']))
            print(playlist['id'])
            getListTracks(sp, playlist['id'])
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    print(count)

# if __name__ == '__main__':
    # playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f"
    # playlist_URI = playlist_link.split("/")[-1].split("?")[0]

    # sp = authen()
    # getPlaylist(sp)
    # getListTracks(sp, playlist_URI)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/