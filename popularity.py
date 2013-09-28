import sqlite3
import csv

DATABASE = 'db/popularity.db'


if __name__ == '__main__':
    db = sqlite3.connect(DATABASE)
    with open('itunes_dummy.txt', 'r') as data_file:
        for line in csv.reader(data_file, delimiter="\t"):
            db.execute(
                'insert into popularities (genre, atom_id, rank) values (?, ?, ?)',
                [line[2], line[3], line[4]])
        db.commit()
