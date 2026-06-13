Quotes Data Pipeline

This is my final project for IS 303. It is a Python script that scrapes quotes from a practice website, saves them to a database, and then makes a chart showing the most common themes.

I used requests and BeautifulSoup to pull the text, authors, and tags from quotes.toscrape.com. I made sure to add a 1-second delay between pages so I wasn't spamming the server.

After grabbing the data, the code uses Peewee and SQLite to store it all in a local database called quotes.db. I set it up so it checks for duplicates, that way if you run the script a bunch of times, it doesn't just copy the same quotes over and over.

Finally, it uses Pandas to crunch the numbers and figure out the top 10 most used tags, and then it builds a horizontal bar chart with Matplotlib so you can actually see the breakdown.

If you want to run it yourself, you just need to pip install requests, beautifulsoup4, peewee, pandas, and matplotlib, and then run the main.py file.