import requests
from lxml import html
import csv



def scraper():
    """
    Scrapes book data from the homepage of 'Books to Scrape' website.

    For each book listed on the page, it extracts:
    - Title of the book
    - Price (including currency symbol)
    - Image source URL
    - Star rating (as a text label like 'Three', 'Five', etc.)
    - Availability status (e.g., 'In stock')

    The data is printed to the console and is saved to csv file.

    This function uses XPath to extract data elements and assumes
    the HTML content has been parsed into an lxml tree structure.
    """
    books_data = []
    books = tree.xpath('//article[@class="product_pod"]')

    for book in books:
        try:
            title = book.xpath('.//h3/a/@title')[0]
            price = book.xpath('.//p[@class="price_color"]/text()')[0]
            image = book.xpath('.//div[@class="image_container"]/a/img/@src')[0]
            rating = book.xpath('.//p[contains(@class, "star-rating")]/@class')[0].split()[-1]
            availability = book.xpath('.//p[contains(@class, "instock")]/text()')
            availability_text = ''.join(availability).strip()

            image_url = f"{url}{image.replace('../', '')}"

            books_data.append({
                "Title": title,
                "Price": price,
                "Rating": rating,
                "Availability": availability_text,
                "Image URL": image_url
            })

            print(f"Title: {title}")
            print(f"Price: {price}")
            print(f"Rating: {rating}")
            print(f"Availability: {availability_text}")
            print(f"Image URL: {image_url}")
            print("-" * 50)

        except Exception as e:
            print(f"Error while scraping a book: {e}")
            continue

    return books_data


def clean_data(input_data, output_file):
    """
    Removes currency symbol from price category, converts rating from string to integers
    and removes unnecessary white spaces from rest of the attributes
    """
    cleaned_data = []
    ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    try:
        for row in input_data:
            cleaned_row = {
                "Title": row["Title"].strip(),
                "Price": row["Price"].strip()[1:] if row["Price"].strip() else "",
                "Rating": ratings[row["Rating"]],
                "Availability": row["Availability"].strip(),
                "Image URL": row["Image URL"].strip()
            }
            cleaned_data.append(cleaned_row)

        export_to_csv(cleaned_data, output_file)

    except Exception as e:
        print(f"Error cleaning data: {e}")


def export_to_csv(data, filename):
    """Exports the book data to a CSV file."""
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["Title", "Price", "Rating", "Availability", "Image URL"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"\nData exported successfully to '{filename}'")
    except Exception as e:
        print(f"Failed to export CSV: {e}")



if __name__ == "__main__":
    url = "https://books.toscrape.com/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        tree = html.fromstring(response.content)

        scraped_data = scraper()
        export_to_csv(scraped_data, "datasets/books.csv")
        clean_data(scraped_data, "datasets/cleaned_books.csv")

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch the page: {e}")
