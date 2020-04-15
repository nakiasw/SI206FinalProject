from bs4 import BeautifulSoup
import requests
import os
import sqlite3

#Create a function to pull song titles and their ranking from the billboard website
def titles_and_rankings(url):
    """Inputs a website that'll return the title of each song and their ranking in a list of tuples."""
    r = requests.get(url) #might have to add https:// 
    data = r.text
    soup = BeautifulSoup(data, 'lxml')

    body = soup.find('body')
    main = body.find('main')
    article = main.find('article')
    div1 = article.find('div', class_ = 'longform__body js-fitvids-content')
    div2 = div1.find('div', class_ = 'container') 
    div3 = div2.find('div', class_ = 'longform__body-primary')

    para = div3.find_all('p') #find_all returns a list of all p tags

    l = []
    for p in para:
        p = str(p)
        if '<strong>' in p: #have to figure out how to git rid of some of the a tags

            p.replace('<p><strong>','').replace('</strong></p>', '')
            l.append(p)    #list of the rankings in strings that still inlcudes the <p><strong>


    return len(l)

    
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
print(titles_and_rankings('https://www.billboard.com/articles/events/year-in-music-2018/8489483/best-songs-2018-staff-picks'))