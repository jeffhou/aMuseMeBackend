import json
import requests
import grequests

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


def get_similar(*artists):
    similar_artists = {}
    urls = ("http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist=%s&api_key=%s&format=json&limit=3" % (artist, API_KEY) for artist in artists)
    rs = grequests.map((grequests.get(url) for url in urls))
    for r in rs:
        r_json = r.json()
        artist = r_json['similarartists']['@attr']['artist']
        for similar in r_json['similarartists']['artist']:
            if similar['name'] not in similar_artists:
                similar_artists[similar['name']] = []
            similar_artists[similar['name']].append(artist)
    return sorted(
        similar_artists.iteritems(), key=lambda s: len(similar_artists[s[0]]),
        reverse=True)
