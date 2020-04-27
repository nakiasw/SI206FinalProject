from bs4 import BeautifulSoup
import requests
import os
import sqlite3
import json

#Create a function to pull song titles and their ranking from the billboard website
# returns a list of tuples in format (rank, title, artist(s))
def titles_and_rankings():
    yearLow = int(input("Please enter a lower bound year between 2006 and 2019: "))
    yearHi = int(input("Please enter an upper bound year between 2006 and 2019: "))
    """Inputs a website that'll return the title of each song and their ranking in a list of tuples."""
    # error check to make sure the input year is between 2006 and 2019
    if yearLow > 2019 or yearLow < 2006 or yearHi > 2019 or yearHi < 2006 or yearLow == yearHi:
        print("Make sure years are between 2006 and 2019, and are not the same")
        exit(1)
    if yearLow > yearHi:
        print("Please provide a valid range")
        exit(1)
    if yearHi - yearLow != 2:
        print("Please provide a 3 year range")
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

# Create a database to store id and genre for each track, call it Genres
def genre_table():
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    conn = sqlite3.connect(path + 'WilkinsSheltonRecords.db')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS Genres')
    cur.execute('CREATE TABLE Genres (id INTEGER, genre TEXT)')
    conn.commit()
    cur.close()

info = titles_and_rankings()
billboardData(info)
genre_table()
