import json
import requests
from urllib import urlencode

def search(search_term, **params):
    res = requests.get('http://itunes.apple.com/search?term=%s&%s' %
        (search_term, urlencode(params)))
    results = [r for r in res.json().get('results', [])
        if r['wrapperType'] == 'track']
    return results

def lookup(atom_id):
    res = requests.get('http://itunes.apple.com/lookup?id=%s' % atom_id)
    if res.json()['resultCount'] >= 1:
        return res.json()['results'][0]
    return {}
