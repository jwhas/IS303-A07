# A07 Integration Pipeline Analysis

# Dataset Description
For this project, I built a dataset of  quotes by scraping the first three pages of quotes.toscrape.com, which gave me 30 unique records. The database stores three main pieces of info for each quote: text, author, and tags. 

# Pipeline Description
My main() function ties the whole pipeline together by running four steps. Starting with fetch_and_scrape_quotes(), which pings the web pages, verifies we get a 200 HTTP status code, and uses BeautifulSoup to parse the HTML into a list of dictionaries.store_quotes() takes over, using Peewee ORM to load the records into a SQLite database (quotes.db). I set up a uniqueness constraint on the quote text so it automatically ignores any duplicates if the script runs multiple times. analyze_quotes() pulls the DB data into a Pandas DataFrame, splits up the comma-separated tags, and runs a groupby aggregation to count up how often each tag appears. visualize_quotes() uses that aggregated data to build and save a horizontal bar chart before popping it up on the screen.

# Findings
When I ran Pandas, it pulled 82 total tags across the 30 quotes. The groupby analysis showed that life was the most common theme by far, showing up 7 times in the sample. I also found that out of the 20 unique authors we scraped, Albert Einstein was the most popular with 6 quotes in the dataset. I generated a bar chart (quotes_chart.png) that maps out the frequency of the top 10 themes.

# Ethical Considerations
I wanted to make sure my scraping was ethical, so I specifically used quotes.toscrape.com because I dont have ennough experience to know what to scrape and what not to scrape. I was just a little scared. I also added a time.sleep(1) (thanks to Gemini) pause between each page request to rate-limit the scraper and avoid spamming their server. I only pulled historically important quotes too so I wouldnt accudentially take some important information. 

# Limitations
The biggest limitation here is definitely the sample size. Since I only scraped three pages, the dataset caps out at 30 quotes, and it isn't really enough data to draw  conclusions about broader trends. If I had more time to expand the project, I would update the scraper to loop through the site's entire pagination to sfit through the whole database. It would also be interesting to run a text-based sentiment  on the actual quote text rather than just relying on the tags the website provided.