import json
import requests

#constants
API_KEY = "188d3cd487e493f17365888e2d6adf9c"
SECRET = "565f4aa831b8cf35e4693f448aa81bc4"

def get_artist(artist_name):
    r = requests.get("http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist=%s&api_key=%s&format=json" % (artist_name, API_KEY))
    artist_json_dict = r.json()['artist']
    return artist_json_dict


def get_track(track_name, artist_name):
    r = requests.get("http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key="+API_KEY+"&artist="+artist_name+"&track="+track_name+"&format=json")
    track_json_dict = r.json()['track']
    return track_json_dict
