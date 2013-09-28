from flask import Flask, render_template, request, g, Response
from werkzeug.contrib.cache import SimpleCache
from helpers import json_response
from random import random
import os
import lastfm
import json
import itunes
import sqlite3

app = Flask(__name__, static_url_path='', static_folder='public')

cache = SimpleCache()

DATABASE = 'db/popularity.db'


def connect_db():
    return sqlite3.connect(DATABASE)


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


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
    itunes_songs = [dict((k, song[k]) for k in song_fields)
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
        return json_response(artist)
    else:
        return json_response({})


@app.route('/api/random')
def get_random():
    genre = request.args.get('genre')
    if genre:
        song = query_db(
            'select * from popularities where genre=? order by random() limit 1',
            args=[genre], one=True)
    else:
        song = query_db(
            'select * from popularities order by random() limit 1',
            one=True)

    lookup = itunes.lookup(song['atom_id'])
    fields = ['trackName', 'previewUrl', 'artworkUrl100', 'collectionName']
    for field in fields:
        song[field] = lookup[field]
    return json_response(song)


@app.route('/api/genres')
def get_genres():
    genres = [item['genre']
              for item in query_db('select distinct genre from popularities')]
    return json_response(genres)


if __name__ == '__main__':
    app.run(debug=os.environ.get('DEBUG', True),
            port=int(os.environ.get('PORT', 5000)))
