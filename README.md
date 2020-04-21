# SI206FinalProject

## Purpose
In today's world of viral videos and overnight superstars, everyone is looking for their way to fame. Some may join TikTok and hope their videos get seen by millions, some may think of a billion dollar idea and start a company, and some may hope their sports film gets seen by top scouts & universities. Here at Wilkins Shelton Records, we specialize in helping the big record labels find the next stars, and even consult new artists on what genres will be most successful in the coming years.

## How It Works
Our world renowned web scraping algorithm gets updated data from Billboard's Year End Top 100 (any year(s) from 2006-2019) and stores the best hits in our secret database. From there, we use the Genius API to extract even more information about the top hits, like genre, record label, release date, etc. After calculating frequencies of genre and record label in the top 100 of each year, we see if we can find any sorts of trends that might help our clients better prepare for the next year.

To predict the best genre of next year, each spot in the Top 100 is given a point value, 100 - rank. Every time a genre appears in a spot, its score is increaed. For example, if rank 45 is a pop song, the pop genre gets 100 - 45 = 55 points. After calculating frequencies, divide the frequency by total number of songs, to get a percentage of genres. Once all point totals are summed, multiply each genre by their percentage. The highest point total should be the best genre next year. We can do the same for record labels. 

If we want to go more in depth we can even look at release timing to help predict when the best time to release a song is, historically.

## Visuals
We want to show a year-to-year change in frequencies, point totals, and projections for the next year. Also, we will show the yearly breakdown of genres in the Top 100, as well as which was the most popular.

If time allows, we will also show a correlation plot in terms of release months and rank on the Top 100.

## How to Run it
Fork this repo (or download the python file and the database). Run the python file and input via terminal as necessary.