from flask import Flask, render_template, request, jsonify
from werkzeug.contrib.cache import SimpleCache
import os
import lastfm
import json

app = Flask(__name__, static_url_path='', static_folder='public')

cache = SimpleCache()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/picker')
def picker():
    return app.send_static_file('picker.html')

@app.route('/detail')
def detail():
    return render_template('detail.html', **{
        'name': 'Cher',
        'picture': 'http://userserve-ak.last.fm/serve/160/285717.jpg',
        'top_tracks': ['Top Track 1', 'Top Track 2', 'Top Track 3'],
        'on_tour': True,
    })

@app.route('/api/artist')
def get_artist():
    artist_name = request.args.get('artist')
    if artist_name:
        artist = cache.get('artist:%s' % artist_name)
        if artist is None:
            artist = lastfm.get_artist(artist_name)
            cache.set('artist:%s' % artist_name, artist, timeout=5*60)
        return jsonify(artist)
    else:
        return jsonify({})

if __name__ == '__main__':
    app.run(debug=os.environ.get('DEBUG', True),
            port=int(os.environ.get('PORT', 5000)))
