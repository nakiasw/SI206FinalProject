from bs4 import BeautifulSoup
import requests
import os
import sqlite3
import hashlib
import json

#Create a function to pull song titles and their ranking from the billboard website
# returns a list of tuples in format (rank, title, artist(s))
def titles_and_rankings(yearLow, yearHi):
    """Inputs a website that'll return the title of each song and their ranking in a list of tuples."""
    # error check to make sure the input year is between 2006 and 2019
    if yearLow > 2019 or yearLow < 2006 or yearHi > 2019 or yearHi < 2006:
        print("Make sure years are between 2006 and 2019")
        exit(1)
    if yearLow > yearHi:
        print("Please provide a valid range")
        exit(1)
    z = yearLow
    info = []
    while z <= yearHi:
        newurl = "https://www.billboard.com/charts/year-end/" + str(z) + "/hot-100-songs"
        page = requests.get(newurl)
        soup2 = BeautifulSoup(page.content, "html.parser")
        songs = soup2.find_all('div', class_="ye-chart-item__primary-row")
        for song in songs:
            rank = ""
            title = ""
            artist = ""
            for x in range(len(song.contents)):
                if x == 1:
                    rank = int(song.contents[x].text.strip("\n"))
                if x == 5:
                    for y in range(len(song.contents[x].contents)):
                        if y == 1:
                            title = song.contents[x].contents[y].text.strip("\n")
                        if y == 3:
                            artist = song.contents[x].contents[y].text.strip("\n")
            songInfo = (rank, title, artist, z)
            info.append(songInfo)
        z += 1

    return info

# this function takes in the list of tuples (info) and creates a table in the database called "Top 100"
def billboardData(info):
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    conn = sqlite3.connect(path + 'WilkinsSheltonRecords.db')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS Top100')
    cur.execute('CREATE TABLE Top100 (id INTEGER, year INTEGER, rank INTEGER, title TEXT, artist TEXT)')
    x = 0
    for song in info:
        cur.execute('INSERT INTO Top100 (id, year, rank, title, artist) VALUES (?,?,?,?,?)', (x,song[3],song[0],song[1],song[2]))
        x += 1
    conn.commit()
    cur.close()
    return
    
def lastfm_info(info):
    """Inputs a list of tuples (song title and rank). Returns a dictionary with keys being id in the Top100 table, and the values
    are a tuple in form (track, artist, genre[])."""
    headers = {'user-agent': "WilkinsShelton"}
    payload = {'api_key': "b08f231d65c50a751a8f4f7e3cc72f22", 'method': 'track.getInfo', 'autocorrect': 1, 'format': 'json'}
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    conn = sqlite3.connect(path + 'WilkinsSheltonRecords.db')
    cur = conn.cursor()
    print("Requesting info from Lastfm API...")

    dict = {}
    for data in info:
        track = data[1]
        artist = data[2]
        payload['track'] = track
        payload["artist"] = artist
        r = requests.get('http://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
        if r.status_code != 200:
            print("Error: Artist %s not found with API" % artist)
        else:
            tags = json.loads(r.text)
            if 'track' not in tags.keys():
                continue
            table = tags['track']
            names = table['toptags']
            morenames = names['tag']
            genres = []
            for genre in morenames:
                genres.append(genre['name'])
            cur.execute('SELECT id FROM Top100 WHERE title=?', (track,))
            stuff = (track, artist, genres)
            dict[cur.fetchone()[0]] = stuff
    return dict

# Create a database with the information from genius_info
def genius_table(info):
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    conn = sqlite3.connect(path + 'WilkinsSheltonRecords.db')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS Genres')
    cur.execute('CREATE TABLE Genres (id INTEGER, genre TEXT')

    

def record_label_count(name):
    """Returns the count of the record label name inputted."""
    pass

def popular_labels():
    """returns a sorted list of tuples of the record label name and the amount of times it appears on BillBoard."""
    pass

def pop_label_tabel():
    """Creates a table in a database that orders the record label and the amount of times it appeard on BillBoard."""
    pass

#Anything afterwards would be used to create the visuals.



#Space below will be used for testing
def main():
    #yearLow = input("Please enter a lower bound year between 2006 and 2019: ")
    #yearHi = input("Please enter an upper bound year or the same year between 2006 and 2019: ")
    #info = titles_and_rankings(int(yearLow), int(yearHi))
    info = titles_and_rankings(2019, 2019)
    billboardData(info)
    lastfm_info(info)



    #api_key = "b08f231d65c50a751a8f4f7e3cc72f22"
    #api_sec = "acdf9b2e149b02276011b4160fe7a232"
    #api_sig = hashlib.md5("api_keyxxxxxxxxmethodauth.getSessiontokenxxxxxxxmysecret")



if __name__ == "__main__":
    main()
