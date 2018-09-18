import os
import fnmatch
import sqlite3

db = sqlite3.connect("music.sqlite")
db.execute("CREATE TABLE IF NOT EXISTS artists (_id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE)")
db.execute("CREATE TABLE IF NOT EXISTS albums (_id INTEGER PRIMARY KEY, name TEXT, year INTEGER, "
           "place INTEGER, id_artist INTEGER NOT NULL,"
           "UNIQUE(name, year, place, id_artist), FOREIGN KEY (id_artist) REFERENCES artists(_id))")
db.execute("CREATE TABLE IF NOT EXISTS songs (_id INTEGER PRIMARY KEY, title TEXT, track INTEGER, "
           "id_albums INTEGER NOT NULL, UNIQUE (title, track, id_albums), "
           "FOREIGN KEY (id_albums) REFERENCES albums(_id))")


def read_music(path, extension):

    for paths, dirs, files in os.walk(path):
        album_data = (os.path.split(paths))[1].split(" - ")
        if len(album_data) > 3:
            # Reading data from paths
            place_ranking = album_data[0]
            print(int(place_ranking[1:]))
            year = album_data[1]
            artist = album_data[2]
            album_title = album_data[3]
            # Insert values to artists table
            db.execute("INSERT OR IGNORE INTO artists (name) VALUES (?)", (album_data[2],))
            cursor = db.cursor()
            cursor.execute("SELECT _id FROM artists WHERE name = (?)", (artist,))
            # Insert values to albums table
            db.execute("INSERT OR IGNORE INTO albums (name, year, place, id_artist) VALUES (?, ?, ?, ?)",
                       (album_title, year, int(place_ranking[1:]), int(cursor.fetchone()[0])))

        for song in fnmatch.filter(files, "*.{}".format(extension)):

            track_number = song.split(" - ")[-2]
            track = song.split(" - ")[-1][:-4]
            cursor.execute("SELECT _id FROM albums WHERE name = (?)", (album_title,))
            db.execute("INSERT OR IGNORE INTO songs (title, track, id_albums) VALUES (?, ?, ?)",
                       (track, track_number, int(cursor.fetchone()[0])))
            
            db.commit()


read_music("E:\mp3\The Rolling Stone 500 Greatest Albums of All Time 100 - 149", "mp3")
