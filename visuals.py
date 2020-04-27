import matplotlib.pyplot as plt
import os
import sqlite3
import string
import numpy

# This function goes thru the Genre table in our database and returns a dictionary of frequencies for each genre for each year
def calc_freq():
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    conn = sqlite3.connect(path + 'WilkinsSheltonRecords.db')
    cur = conn.cursor()
    cur.execute('SELECT id FROM Genres')
    ids = cur.fetchall()
    dict = {}
    for id in ids:
        id = str(id[0])
        cur.execute('SELECT Top100.year FROM Top100 JOIN Genres ON Top100.id = Genres.id WHERE Genres.id=?', (id,))
        year = cur.fetchone()[0]
        cur.execute('SELECT genre FROM Genres WHERE id=?', (id,))
        genre = cur.fetchone()[0]
        genre = genre.translate(string.punctuation)
        genre = genre.lower()
        if year not in dict.keys():
            dict[year] = {}
        genres = dict[year]
        if genre == 'hip-hop' or genre == 'hip hop' or genre == 'hiphop' or genre == 'emo rap' or genre == 'rap' or genre == 'cloud rap' or genre == 'trap':
            genre = 'hip hop'
        if genre == 'pop rock' or genre == 'indie rock' or genre == 'alternative':
            genre = 'rock'
        if genre == 'indie pop' or genre == 'electropop' or genre == 'indie':
            genre = 'pop'
        if genre == 'dance' or genre == 'party':
            genre = 'electronic'
        if genre == 'not country' or genre == 'racist country':
            genre = 'country'
        genres[genre] = genres.get(genre, 0) + 1
    f = open('data.txt', 'w+')
    for year in dict:
        f.write("Year: %s\n" % year)
        for genre in dict[year]:
            f.write("%s: %d\n" % (genre, dict[year][genre]))
        f.write("\n")
    f.close()
    return dict

# This function takes the raw data from the first function and refines it to only show the top 4 genres of each year
def finalize_data(dict):
    newdict = {}
    for year in dict:
        newdict[year] = newdict.get(year, {})
        genres = dict[year]
        count = 0
        for genre in sorted(genres.items(), key=lambda x: x[1], reverse=True):
            if count < 5 and genre[0] != 'none':
                newdict[year][genre[0]] = genre[1]
            count += 1
    return newdict
    
#Pie Chart
def pie(data, year):
    genres = []
    amount = []
    for genre in data[year]:
        genres.append(genre)
        amount.append(data[year][genre])

    fig1, ax1 = plt.subplots()
    ax1.pie(amount, labels=genres, autopct='%1.1f%%', shadow=True, startangle=90) #the autopct automatically makes the percentages 
    ax1.legend(title = "Top 4 Genres in " + str(year))
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()

def pie1(data):
    yearRange = []
    newdict = {}
    for year in data.keys():
        yearRange.append(year)
        for genre in data[year]:
            newdict[genre] = newdict.get(genre, 0) + 1
    genres = []
    amount = []
    for genre in newdict.keys():
        genres.append(genre)
        amount.append(newdict[genre])

    fig1, ax1 = plt.subplots()
    ax1.pie(amount, labels=genres, autopct='%1.1f%%', shadow=True, startangle=90) #the autopct automatically makes the percentages 
    ax1.legend(title = "Top Genres between " + str(yearRange[0]) + ' - ' + str(yearRange[-1]))
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()

def bar1(data):
    """Shows the growth of each genre through the years, including a prediction of the next most popular genre based on the history."""
    years = []
    allgenres = []
    genre_count = []
    for year in data.keys():
        years.append(year)
        for genre in data[year]:
            allgenres.append(genre)
    for year in data.keys():
        count = []
        for genre in allgenres:
            if genre not in data[year]:
                count.append(0)
            else:
                count.append(data[year][genre])
        genre_count.append(count)
    
    widthB = 0.25
    newlist = []
    i = 0
    while i < 3:
        indv = []
        for count in genre_count:
            indv.append(count[i])
        newlist.append(indv)
        i += 1
    bars1 = newlist[0]
    bars2 = newlist[1]
    bars3 = newlist[2]

    r1 = numpy.arange(len(bars1))
    r2 = [x + widthB for x in r1]
    r3 = [x + widthB for x in r2]

    plt.bar(r1, bars1, color='r', width=widthB, edgecolor='white', label=allgenres[0])
    plt.bar(r2, bars2, color='g', width=widthB, edgecolor='white', label=allgenres[1])
    plt.bar(r3, bars3, color='b', width=widthB, edgecolor='white', label=allgenres[2])
    

    plt.title('Genres in Billboard Top 100 between ' + str(years[0]) + " - " + str(years[-1]))
    plt.xlabel('Year')
    plt.xticks([r + widthB for r in range(len(bars1))], [years[0], years[1], years[2]])
    plt.ylabel('Count')
    plt.legend()
    plt.show()


###############################################################################################################################################
data = calc_freq()
newdata = finalize_data(data)
for year in newdata.keys():
    pie(newdata, year)
pie1(newdata)
bar1(newdata)