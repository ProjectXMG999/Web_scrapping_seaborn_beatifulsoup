import requests
from bs4 import BeautifulSoup
import sqlite3
import time

# Set the URL of the page to scrape
url = 'https://pl.wikipedia.org/wiki/Cukrownik_czarnobrody'

# Set the duration of the scraping process (in seconds)
duration = 60

# Set the interval between requests (in seconds)
interval = 10

# Connect to the SQLite database
conn = sqlite3.connect('links.db')

# Create a table to store the scraped data
conn.execute('''CREATE TABLE IF NOT EXISTS links 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT UNIQUE)''')

# Run the scraping process for the specified duration
start_time = time.time()
while time.time() < start_time + duration:
    # Send a GET request to the URL and handle errors
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e)
        continue

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all links on the page and extract the URLs
    links = [link.get('href') for link in soup.find_all('a')]

    # Clean the URLs to remove any unwanted characters or query parameters
    clean_links = []
    for link in links:
        if link is not None:
            clean_link = link.strip().replace('\n', '').replace('\r', '')
            if len(clean_link) > 0 and clean_link[0] != '#':
                clean_links.append(clean_link)

    # Remove any duplicates from the list of clean URLs
    unique_links = set(clean_links)

    # Write the unique URLs to the SQLite database
    for link in unique_links:
        try:
            conn.execute("INSERT INTO links (url) VALUES (?)", (link,))
        except sqlite3.IntegrityError:
            # Ignore duplicate URLs
            pass
    conn.commit()

    # Wait for the specified interval before sending the next request
    time.sleep(interval)

# Close the SQLite connection
conn.close()
