# Amazon Product Catalog Crawler

This project is a Python-based web scraper designed to collect product data from Amazon's Software category. It uses Selenium with undetected-chromedriver to bypass bot detection, and BeautifulSoup for parsing HTML. The project also includes a data cleaning and analysis pipeline.

## Features

* Rotating user agents for stealth scraping
* Undetected Chrome WebDriver setup
* Pagination handling with retries
* Data extraction including ASIN, title, link, image, rating, review count, price, and delivery info
* Cleaned output CSV and JSON
* Data cleaning to handle whitespace, currency, and ratings
* Basic statistical analysis and summary of the dataset

## Requirements

```
selenium
undetected-chromedriver
beautifulsoup4
pandas
```

You can install all dependencies using:

```bash
pip install -r requirements.txt
```

## Project Structure

```
ProductCatalogCrawler/
├── datasets/
│   ├── products.csv
│   ├── products.json
│   └── cleaned_products.csv
└── src/
    ├── scraping.log
    ├── scraper.py
    └── data_cleaning_and_analysis.py
├── requirements.txt
├── README.md
```

## Usage

To start scraping and analyzing data, run:

```bash
python scraper.py
```

This will:

1. Scrape Amazon product listings.
2. Save raw data to `products.csv` and `products.json`.
3. Clean the data.
4. Output `cleaned_products.csv`.
5. Print basic statistics and insights to the console.

## Output

* `products.csv` - Raw scraped data
* `products.json` - Same data in JSON format
* `cleaned_products.csv` - Cleaned and structured dataset
* Console output - Summary statistics like average price, highest/lowest priced products, rating distribution, etc.

