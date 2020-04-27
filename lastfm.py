from bs4 import BeautifulSoup
import requests
import os
import sqlite3
import json

# This function takes the data from the Top100 table in the database and gets requests from the last fm API
# It returns a dictionary where the key is the id, and the value is a tuple (track, artist, genre[])
def lastfm_info():
    """Inputs a list of tuples (song title and rank). Returns a dictionary with keys being id in the Top100 table, and the values
    are a tuple in form (track, artist, genre[])."""
    headers = {'user-agent': "WilkinsShelton"}
    payload = {'api_key': "b08f231d65c50a751a8f4f7e3cc72f22", 'method': 'track.getInfo', 'autocorrect': 1, 'format': 'json'}
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    conn = sqlite3.connect(path + 'WilkinsSheltonRecords.db')
    cur = conn.cursor()
    print("Requesting info from Lastfm API...")
    cur.execute('SELECT * FROM Top100')
    info = cur.fetchall()

    dict = {}
    for data in info:
        track = data[3]
        artist = data[4]
        payload['track'] = track
        payload["artist"] = artist
        r = requests.get('http://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
        if r.status_code != 200:
            print("Error: Artist %s not found with API" % artist)
        else:
            tags = json.loads(r.text)
            if 'track' not in tags.keys():
                stuff = (data[0], data[3], data[4], [])
                dict[data[0]] = stuff
                continue
            table = tags['track']
            names = table['toptags']
            morenames = names['tag']
            genres = []
            for genre in morenames:
                genres.append(genre['name'])
            stuff = (data[0], track, artist, genres)
            dict[data[0]] = stuff
    with open('genres.json', 'w+') as f:
        json.dump(dict, f)

# This function uses the data from the api and stores 20 at a time
def genre_table():
    print("Inserting 20 entries into Genre table...")
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    conn = sqlite3.connect(path + 'WilkinsSheltonRecords.db')
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM Genres')
    index = cur.fetchone()[0]
    stop = index + 20
    with open('genres.json', 'r') as f:
        data = json.load(f)
    if stop > len(data):
        stop = len(data)
        print("Last call needed")
    while index < stop:
        song = data[str(index)]
        if song[3] == []:
            index += 1
            cur.execute('INSERT INTO Genres (id, genre) VALUES (?,?)', (song[0], "none"))
            continue
        cur.execute('INSERT INTO Genres (id, genre) VALUES (?,?)', (song[0], song[3][0]))
        index += 1
    conn.commit()
    cur.close()

path = os.path.dirname(os.path.abspath(__file__)) + os.sep
conn = sqlite3.connect(path + 'WilkinsSheltonRecords.db')
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM Genres')
if cur.fetchone()[0] == 0:
    lastfm_info()
genre_table()
