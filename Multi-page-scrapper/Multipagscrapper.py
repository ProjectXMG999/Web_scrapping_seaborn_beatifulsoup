import requests
from bs4 import BeautifulSoup
import sqlite3
import time

# Set the URL of the page to start scraping
start_url = 'https://www.example.com'

# Set the duration of the scraping process (in seconds)
duration = 60

# Set the interval between requests (in seconds)
interval = 10

# Set up the SQLite connection
conn = sqlite3.connect('scraped_data.db')
c = conn.cursor()

# Create a table to store the scraped data
c.execute("CREATE TABLE IF NOT EXISTS links (id INTEGER PRIMARY KEY, url TEXT UNIQUE, scraped INTEGER DEFAULT 0)")

# Add the start URL to the list of URLs to scrape
urls_to_scrape = [(start_url,)]

# Run the scraping process for the specified duration
start_time = time.time()
while time.time() < start_time + duration and urls_to_scrape:
    # Get the next URL to scrape
    url, = urls_to_scrape.pop(0)
    
    # Send a GET request to the URL and handle errors
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Error scraping {url}: {e}')
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
    urls_to_add = [(link,) for link in unique_links]
    c.executemany("INSERT OR IGNORE INTO links (url) VALUES (?)", urls_to_add)
    conn.commit()

    # Mark the current URL as scraped
    c.execute("UPDATE links SET scraped = 1 WHERE url = ?", (url,))
    conn.commit()

    # Add any new URLs to the list of URLs to scrape
    urls_to_scrape += [(link,) for link in unique_links if not c.execute("SELECT 1 FROM links WHERE url = ?", (link,)).fetchone()]

    # Wait for the specified interval before sending the next request
    time.sleep(interval)

# Close the SQLite connection
c.close()
conn.close()
