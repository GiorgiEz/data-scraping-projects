# YouTube Comments Scraper

This project uses **Selenium** with **Python** to scrape YouTube comments from a specified video. It initializes a headless browser, scrolls to load comments, and extracts key information like author, post time, comment text, and likes. The collected data is then saved into a CSV file.

---

## Features

* Headless browser scraping for better performance
* Scroll automation to load dynamic comment content
* Robust parsing of author, time, comment, and like count
* Saves output to a CSV file using `pandas`

---

## Requirements

* Python 3.12+
* Google Chrome installed
* ChromeDriver matching your Chrome version

Install dependencies using the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Project Structure

```
youtube_scraper/
├── datasets/
│   └── comments.csv          # Output file with scraped data
├── requirements.txt          # List of required Python packages
├── social_meadia_scraper.py  # Main script for scraping
└── README.md                 # Project description
```

---

## Usage

1. Make sure you have ChromeDriver installed and in your system PATH.
2. Run the scraper:

```bash
python social_meadia_scraper.py
```

3. The output will be saved to `datasets/comments.csv`

---
