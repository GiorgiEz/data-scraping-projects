# News Aggregator

## Overview
This News Aggregator is a Python-based web scraping tool that collects and displays news articles from two major sources: **BBC News** and **The New York Times**. The program fetches headlines, summaries, categories, and URLs, allowing users to interact with the news through a command-line menu.

## Features
- **Scrape Latest News**: Extracts articles from BBC and NYT.
- **Filter by Category**: Users can view articles belonging to a specific category (e.g., Politics, Sports, etc.).
- **Search by Keyword**: Find articles containing specific keywords in the headline or summary.
- **Interactive Command-Line Menu**: Users can navigate and interact with the news data easily.

## How It Works
1. **Fetch News**: The script scrapes BBC News and NYT using `BeautifulSoup`.
2. **Store Articles**: Extracted articles are stored in a list (`news_data`).
3. **User Interaction**: Users can choose options from the command-line menu:
   - View all news articles
   - Filter news by category
   - Search for news by keyword
   - Exit the program

## Requirements
- Python 3.x
- `requests` (for making HTTP requests)
- `BeautifulSoup4` (for parsing HTML)

Install dependencies using:
```sh
pip install -r requirements.txt
```

## Usage
Run the script:
```sh
python news_aggregator.py
```
Follow the menu prompts to filter or search news articles.
