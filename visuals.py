import matplotlib.pyplot as plt

#Pie Chart
def pie():
    genres = 'Country', 'Hip-Hop', 'Rap', 'Blues' #change this list to whatever the top 4 genres are in that year from database
    amount = [5, 15, 10, 2] #change the numbers also to whatevers in database

    fig1, ax1 = plt.subplots()
    ax1.pie(amount, labels=genres, autopct='%1.1f%%', shadow=True, startangle=90) #the autopct automatically makes the percentages 
    ax1.legend(title = "List of Genres in the Year " + '2019')
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()

def pie1(table):
    """Total amount of each genre in a specifc year from the table given"""
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    conn = sqlite3.connect(path + 'WilkinsSheltonRecords.db')
    cur = conn.cursor()
    cur.execute('SELECT genres FROM ___') #input the needed information of the new table that is created, should I make the variable name genres for the pie chart? 
    genres = cur.fetchall()
    conn.commit()
    cur.close() #do I need this or can I get rid of it?

    genres = 'Country', 'Hip-Hop', 'Rap', 'Blues' #change this list to whatever the top 4 genres are in that year from database
    amount = [5, 15, 10, 2] #change the numbers also to whatevers in database

    fig1, ax1 = plt.subplots()
    ax1.pie(amount, labels=genres, autopct='%1.1f%%', shadow=True, startangle=90) #the autopct automatically makes the percentages 
    ax1.legend(title = "List of Genres in the Year " + year)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()
    

#Bar Graph
def bar():
    genres = ['Country', 'Hip-Hop', 'Rap', 'Blues']
    genre_count = [12,20,15,1]

    plt.bar(genres, genre_count, color = 'purple')
    plt.title("Popular Genre in the Year " + '2019' )
    plt.xlabel('Genre')
    plt.ylabel('Count')
    plt.show()

def bar1(genre, year1, year2, year3):
    """Shows the growth of each genre through the years, including a prediction of the next most popular genre based on the history."""
    #geninfo and count function is whatever the actual name of those functions
    y1 = geninfo(year1)
    y2 = geninfo(year2)
    y3 = geninfo(year3)

    count1 = count(y1) #whatever function that counts the amount of times a genre occurs in that table (or whatever the input function is)
    count2 = count(y2)
    count3 = count(y3)

    years = [year1, year2, year3]        #need to make sure this and the information below is correct 
    genre_count = [count1,count2,count3]

    plt.bar(years, genre_count, color = 'purple')
    plt.title(genre + 'Occurances')
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.show ()

    pass 


###############################################################################################################################################
print(pie())
print(bar())