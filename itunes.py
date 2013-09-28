import json
import requests

def search(search_term):
    res = requests.get('http://itunes.apple.com/search?term=%s' % search_term)
    return res.json().get('results', [])

def lookup(artist_id):
    res = requests.get('http://itunes.apple.com/lookup?id=%s' % artist_id)
    if res.json()['resultCount'] >= 1:
        return res.json()['results'][0]
    return {}
