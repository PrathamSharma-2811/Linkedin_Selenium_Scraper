
# LinkedIn Post Scraper

A Selenium-based script to scrape LinkedIn posts based on keywords or hashtags. It extracts URLs and post content and saves them to a CSV file.

## Features
- Scrapes LinkedIn posts based on user input (keywords or hashtags).
- Automatically switches between keyword and hashtag search.
- Scrolls through the LinkedIn search results and extracts post URLs and content.
- Saves the scraped data into a CSV file.

## Requirements
- Python 3.x
- Selenium
- BeautifulSoup4
- ChromeDriver (installed via `webdriver_manager`)


## How It Works
1. **Login**: The script prompts you to enter your LinkedIn email and password to log in.
2. **Search**: Input either a keyword or hashtag. For hashtags, include `#` (e.g., `#AI`).
3. **Scraping**: The script scrolls through search results, extracting post URLs and content.
4. **Output**: The scraped data is saved as `scraped_data.csv`.

