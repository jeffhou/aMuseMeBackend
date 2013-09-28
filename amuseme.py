from flask import Flask, render_template, request, jsonify
from werkzeug.contrib.cache import SimpleCache
import os
import lastfm
import json
import itunes

app = Flask(__name__, static_url_path='', static_folder='public')

cache = SimpleCache()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/picker')
def picker():
    return app.send_static_file('picker.html')

@app.route('/detail/<artist_id>')
def detail(artist_id):
    # TODO: make this async?
    itunes_data = itunes.lookup(artist_id)
    lastfm_data = lastfm.get_artist(itunes_data['artistName'])

    song_fields = ['trackName', 'previewUrl', 'artworkUrl100', 'collectionName']
    itunes_songs = itunes.search(itunes_data['artistName'])[:3]
    itunes_songs = [dict((k, song[k]) for k in song_fields )
        for song in itunes_songs]

    return render_template('detail.html', **{
        'name': itunes_data['artistName'],
        'picture': lastfm_data['image'][2]['#text'],
        'on_tour': True,
        'other_songs': itunes_songs,
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
