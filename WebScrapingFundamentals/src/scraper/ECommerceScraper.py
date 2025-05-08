import os
import csv
import json
import requests
import logging
from bs4 import BeautifulSoup
from WebScrapingFundamentals.src.HTTPRequest import HTTPRequest


# Configuring the Logging system
logging.basicConfig(
    filename="src/scraper/logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(console_handler)


class ECommerceScraper:
    """ Scraping the multi-page E-commerce website, with functionality to download images by the product name """
    def __init__(self, url="https://scrapeme.live/shop/", number_of_pages=1):
        self.url = url
        self.number_of_pages = number_of_pages
        self.products_csv_path = "src/scraper/datasets/products.csv"
        self.products_json_path = "src/scraper/datasets/products.json"
        self.image_folder = "src/scraper/image_folder"

        os.makedirs(self.image_folder, exist_ok=True)  # Ensure image folder exists

    def scrape_products(self):
        """Scrape product data from multiple pages."""
        product_list = []
        page_number = 1

        while page_number <= self.number_of_pages:
            url = f"{self.url}page/{page_number}/"
            logging.info(f"📌 Scraping page {page_number}: {url}")

            try:
                response = HTTPRequest(url).http_method("GET")
                soup = BeautifulSoup(response, "html.parser") if response else None

                products = (soup.find("div", id="page").find("div", id="content")
                            .find("main").find("ul", class_="products columns-4"))

                if not products:
                    logging.warning(f"⚠️ No products found on page {page_number}.")
                    break

                for product in products.find_all("li"):
                    a = product.find("a")
                    prod_img = a.find("img")['src']
                    prod_name = a.find("h2").text.strip()
                    prod_price = a.find("span", class_="price").find("span").text.strip()

                    product_data = {"Image URL": prod_img, "Name": prod_name, "Price": prod_price}
                    product_list.append(product_data)
                    logging.info(f"✅ Scraped: {prod_name} - {prod_price}")

                self.save_to_csv(product_list)
                self.save_to_json(product_list)

            except Exception as e:
                logging.error(f"❌ Error scraping page {page_number}: {e}")

            page_number += 1

    def save_to_csv(self, product_list):
        """Save product data to a CSV file."""
        try:
            with open(self.products_csv_path, mode="w", newline="", encoding="utf-8") as csv_file:
                fieldnames = ["Image URL", "Name", "Price"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(product_list)

            logging.info(f"✅ Data saved to CSV: {self.products_csv_path}")
        except Exception as e:
            logging.error(f"❌ Failed to save CSV: {e}")

    def save_to_json(self, product_list):
        """Save product data to a JSON file."""
        try:
            with open(self.products_json_path, mode="w", encoding="utf-8") as json_file:
                json.dump(product_list, json_file, indent=4, ensure_ascii=False)

            logging.info(f"✅ Data saved to JSON: {self.products_json_path}")
        except Exception as e:
            logging.error(f"❌ Failed to save JSON: {e}")

    def download_image(self, prod_name):
        """Download product image using name of the product from CSV file."""
        image_filename = os.path.join(self.image_folder, f"{prod_name}.jpg")

        try:
            with open(self.products_csv_path, mode="r", encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    if row["Name"].lower() == prod_name.lower():
                        prod_img = row["Image URL"]
                        break
                else:
                    logging.warning(f"⚠️ Product '{prod_name}' not found in CSV.")
                    return

            img_data = requests.get(prod_img, stream=True, verify=False)  # Disabling SSL verification
            with open(image_filename, "wb") as img_file:
                for chunk in img_data.iter_content(1024):
                    img_file.write(chunk)

            logging.info(f"✅ Downloaded image: {image_filename}")

        except Exception as e:
            logging.error(f"❌ Failed to download image for '{prod_name}': {e}")
