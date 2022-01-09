import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Press the green button in the gutter to run the script.
import secret
import pika

def authen():
    auth_manager = SpotifyClientCredentials(client_id=secret.CLIENT_ID, client_secret=secret.CLIEN_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp

def getListAudioFeature(sp, listId, timestr, channel):
    audiofeatureList = sp.audio_features(listId)
    tracksList = sp.tracks(listId)
    tracksList = tracksList['tracks']
    artistIDList = map(lambda a : a['artists'][0]['id'], tracksList)
    artistList = sp.artists(artistIDList)["artists"]
    genreList = map(lambda a : {"genres": a["genres"]}, artistList)
    results = list(map(lambda x, y: x | y, audiofeatureList, tracksList))
    results = list(map(lambda x, y: x | y, genreList, results))
    for r in results:
        r.update({'time': timestr})
    # with open('./newdata/data-'+ timestr +'.json', 'w+', encoding='utf-8') as f:
    #     json.dump(results, f, ensure_ascii=False, indent=4)
    return results

# if __name__ == '__main__':
    # playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f"
    # playlist_URI = playlist_link.split("/")[-1].split("?")[0]

    # sp = authen()
    # getPlaylist(sp)
    # getListTracks(sp, playlist_URI)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/