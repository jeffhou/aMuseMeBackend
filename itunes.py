import json
import requests
from urllib import urlencode

def search(search_term, **params):
    res = requests.get('http://itunes.apple.com/search?term=%s&%s' %
        (search_term, urlencode(params)))
    return res.json().get('results', [])

def lookup(atom_id):
    res = requests.get('http://itunes.apple.com/lookup?id=%s' % atom_id)
    if res.json()['resultCount'] >= 1:
        return res.json()['results'][0]
    return {}
