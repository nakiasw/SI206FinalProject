from bs4 import BeautifulSoup
import requests
import os
import sqlite3

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
    
def genius_info(billb_list):
    """Inputs a list of tuples (song title and rank). For each song title, using the Genius API website, return the artist, genre, 
    release date, and record label as a dictionary, where the song title is the key, and the values is the information previously said."""
    pass

#Create a database with the information from genius_info
def genius_table():
    pass

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
    yearLow = input("Please enter a lower bound year between 2006 and 2019: ")
    yearHi = input("Please enter an upper bound year or the same year between 2006 and 2019: ")
    info = titles_and_rankings(int(yearLow), int(yearHi))
    billboardData(info)

if __name__ == "__main__":
    main()
