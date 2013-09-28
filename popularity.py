import sqlite3
import csv
import json

DATABASE = 'db/popularity.db'
MAX_GENRE = 400


if __name__ == '__main__':
    db = sqlite3.connect(DATABASE)
    genre_counts = {}
    with open('genre_translations.json', 'r') as genre_translations:
        f_json = json.loads(genre_translations.read())
        equivalence = f_json['equivalences']
        english_names = f_json['english_names']

    with open('iTunes Data/song_popularity_per_genre', 'r') as data_file:
        for line in csv.reader(data_file, delimiter="\t"):
            if (line[2] in equivalence
                    and genre_counts.get(equivalence[line[2]], 0) < MAX_GENRE):
                if equivalence[line[2]] not in genre_counts:
                    genre_counts[equivalence[line[2]]] = 0
                genre_counts[equivalence[line[2]]] += 1

                db.execute(
                    'insert into popularities (genre, atom_id, rank) \
                    values (?, ?, ?)',
                    [equivalence[line[2]], line[3], line[4]])
        print genre_counts
        db.commit()
