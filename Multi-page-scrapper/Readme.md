### this script is improved by sobe features:
- The script now starts by scraping a single URL (start_url), and then follows links on that page to find other pages to scrape. This avoids the need to manually specify a list of URLs to scrape.
- The script now keeps track of which URLs have already been scraped in the SQLite database, and only scrapes URLs that have not yet been scraped. This avoids scraping the same page multiple times, and ensures that the script can be safely run multiple times without generating duplicates.
- The scraped column in the links table is used to mark URLs that have been scraped. The value is 0 for URLs that have not been scraped, and 1 for URLs that have been scraped. This allows the script to easily check which URLs have already been
