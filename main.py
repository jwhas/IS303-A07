"""
A07: Quotes Collection System

Inputs:     
- Scrape quotes.toscrape.com 

Processes:  
- Extract quotes, authors, and tags using BeautifulSoup
- Store in a SQLite database using Peewee ORM
- Query data into a Pandas DataFrame 
- Analyze top tags via groupby aggregations
- Visualize findings using Matplotlib

Outputs:    
- Printed summary statistics, quotes.db database file, and quotes_chart.png
"""

import requests
from bs4 import BeautifulSoup
from peewee import SqliteDatabase, Model, CharField, TextField
import pandas as pd
import matplotlib.pyplot as plt
import time

# Database Setup
db = SqliteDatabase("quotes.db")
class QuoteModel(Model):
    text = TextField(unique=True)
    author = CharField()
    tags = CharField(null=True)  

    class Meta:
        database = db

# Scraping
def fetch_and_scrape_quotes(num_pages=3):
    """
    Loops through pages of quotes.toscrape.com, extracts elements,
    and returns a list of dictionaries. Enforces rate-limiting.
    """
    base_url = "https://quotes.toscrape.com/page/{}/"
    scraped_quotes = []

    for page in range(1, num_pages + 1):
        url = base_url.format(page)
        print(f"Fetching: {url}")
        
        response = requests.get(url)
        
        # Check HTTP status code before parsing
        if response.status_code != 200:
            print(f"Failed to retrieve page {page}. Status code: {response.status_code}")
            continue
            
        soup = BeautifulSoup(response.text, "html.parser")
        quote_elements = soup.find_all("div", class_="quote")

        for elem in quote_elements:
            text = elem.find("span", class_="text").text.strip()
            author = elem.find("small", class_="author").text.strip()
            

            tag_elements = elem.find_all("a", class_="tag")
            tags_list = [tag.text.strip() for tag in tag_elements]
            tags_str = ",".join(tags_list) if tags_list else None

            scraped_quotes.append({
                "text": text,
                "author": author,
                "tags": tags_str
            })


        time.sleep(1)

    return scraped_quotes

# Database Storage
def store_quotes(quotes_list):
    """
    Safely inserts scraped quotes into the database. 
    Skips over quotes that already exist to prevent database inflation.
    """
    inserted_count = 0
    skipped_count = 0

    for q in quotes_list:
        if not QuoteModel.select().where(QuoteModel.text == q["text"]).exists():
            QuoteModel.create(
                text=q["text"],
                author=q["author"],
                tags=q["tags"]
            )
            inserted_count += 1
        else:
            skipped_count += 1

    print(f"Storage Complete: {inserted_count} new records inserted, {skipped_count} duplicates skipped.")

# Data Query & Analysis
def analyze_quotes():
    """
    Queries the database, transforms records into a Pandas DataFrame,
    performs data cleaning/parsing on tags, and computes a groupby aggregation.
    """
    # Pull data from database
    query = QuoteModel.select()
    df = pd.DataFrame(list(query.dicts()))

    if df.empty:
        print("Database is empty. No analysis can be performed.")
        return None

    all_tags = []
    for tags_entry in df["tags"].dropna():
        all_tags.extend([t.strip() for t in tags_entry.split(",")])
    
    tags_df = pd.DataFrame(all_tags, columns=["Tag"])
    
    tag_counts = tags_df.groupby("Tag").size().reset_index(name="Count")
    top_tags = tag_counts.sort_values(by="Count", ascending=False).head(10)

    print("\n================== PIPELINE ANALYSIS METRICS ==================")
    print(f"Line 1: Total unique quotes stored in database: {len(df)}")
    print(f"Line 2: Total unique authors represented: {df['author'].nunique()}")
    print(f"Line 3: Most impactful author in sample: {df['author'].value_counts().idxmax()} ({df['author'].value_counts().max()} quotes)")
    print(f"Line 4: Total number of descriptive tags found: {len(all_tags)}")
    print(f"Line 5: Most popular theme used: '{top_tags.iloc[0]['Tag']}' appearing {top_tags.iloc[0]['Count']} times.")
    print("===============================================================\n")

    return top_tags

# 5. Visualization
def visualize_quotes(top_tags_df):
    """
    Generates a horizontal bar chart displaying the top 10 tags,
    saves the image to disk, and displays it.
    """
    if top_tags_df is None or top_tags_df.empty:
        return

    plot_df = top_tags_df.sort_values(by="Count", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(plot_df["Tag"], plot_df["Count"], color="skyblue", edgecolor="gray")
    
    # Chart formating
    plt.title("Top 10 Most Frequent Quote Tags / Themes", fontsize=14, fontweight="bold")
    plt.xlabel("Frequency Count", fontsize=11)
    plt.ylabel("Tag Name", fontsize=11)
    plt.tight_layout()

    plt.savefig("quotes_chart.png", dpi=300)
    print("Table saved successfully as 'quotes_chart.png'.")
    plt.show()

# Pipeline 
def main():
    # Connect and establish tables
    db.connect()
    db.create_tables([QuoteModel])
    
    # 1. Fetching
    raw_data = fetch_and_scrape_quotes(num_pages=3)
    
    # 2. Storing
    store_quotes(raw_data)
    
    # 3. Analyzing
    analysis_results = analyze_quotes()
    
    # 4. Visualizing
    visualize_quotes(analysis_results)
    
    db.close()

if __name__ == "__main__":
    main()