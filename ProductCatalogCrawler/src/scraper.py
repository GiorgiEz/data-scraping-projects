from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time, random, csv, json, logging, undetected_chromedriver as uc
from bs4 import BeautifulSoup

from ProductCatalogCrawler.src.data_cleaning_and_analysis import DataCleaningAndAnalysis

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler("scraping.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# List of rotating user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:91.0) Gecko/20100101 Firefox/91.0"
]


def configure_driver():
    user_agent = random.choice(USER_AGENTS)
    logger.info(f"Using User-Agent: {user_agent}")

    options = uc.ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")

    # Disable image and CSS loading
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2
    }
    options.add_experimental_option("prefs", prefs)

    # Appear more like a real user
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless=new")

    # Launch browser
    driver = uc.Chrome(options=options)
    return driver


def scrape_all_pages(driver, base_url):
    driver.get(base_url)
    time.sleep(3)  # Let initial page load

    page_number = 1
    page_amount_to_scrape = 6  # Change as needed

    while page_number < page_amount_to_scrape:
        logger.info(f"Scraping Page {page_number}")
        scrape_current_page(driver)

        try:
            # Check if "Next" button is disabled
            driver.find_element(By.CSS_SELECTOR, "span.s-pagination-next.s-pagination-disabled")
            logger.info("Last page reached.")
            break
        except NoSuchElementException:
            pass

        try:
            max_retries = 5

            for attempt in range(1, max_retries + 1):
                try:
                    logger.info(f"Attempt {attempt}: Trying to click 'Next'...")

                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH,
                        "//a[contains(@class,'s-pagination-next') and not(contains(@class, 's-pagination-disabled'))]"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                    time.sleep(1)

                    actions = ActionChains(driver)
                    actions.move_to_element(next_button).pause(0.5).click().perform()

                    page_number += 1
                    wait_time = random.randint(3, 5)
                    logger.info(f"Successfully navigated to Page {page_number}. Waiting {wait_time}s.")
                    time.sleep(wait_time)
                    break

                except (NoSuchElementException, ElementClickInterceptedException, TimeoutException) as e:
                    wait = 2 ** (attempt - 1)  # exponential backoff: 1, 2, 4, 8, 16
                    logger.warning(f"Retry {attempt}: Click failed due to: {e}. Retrying in {wait}s...")
                    time.sleep(wait)

        except TimeoutException:
            logger.error("Max retries exceeded. Exiting pagination loop.")
            break


def scrape_current_page(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all product containers
    products = soup.find_all("div", {"data-component-type": "s-search-result"})

    for product in products:
        try:
            asin = product.get("data-asin")
            title_el = product.find("h2")
            title = title_el.text.strip() if title_el else "N/A"
            link_el = product.find("a", class_="a-link-normal") if title_el else "N/A"
            link = "https://www.amazon.com" + link_el.get("href") if link_el else "N/A"

            image_el = product.find("img", class_="s-image")
            image = image_el.get("src") if image_el else "N/A"

            rating_el = product.find("span", class_="a-icon-alt")
            rating = rating_el.text.strip() if rating_el else "N/A"

            review_count_el = product.select_one("span.a-size-base.s-underline-text")
            review_count = review_count_el.text.strip() if review_count_el else "N/A"

            price_el = product.select_one("span.a-price > span.a-offscreen")
            price = price_el.text.strip() if price_el else "N/A"

            delivery_el = product.find("span", string=lambda text: text and "Delivery" in text)
            delivery = delivery_el.parent.text.strip() if delivery_el else "N/A"

            data.append({
                "asin": asin,
                "title": title,
                "link": link,
                "image": image,
                "rating": rating,
                "review_count": review_count,
                "price": price,
                "delivery": delivery
            })
        except Exception as e:
            logger.error(f"Error parsing product: {e}")


def write_to_csv():
    with open('../datasets/products.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['asin', 'title', 'link', 'image', 'rating', 'review_count', 'price', 'delivery']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    logger.info("Data written to products.csv")


def write_to_json():
    with open('../datasets/products.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)
    logger.info("Data written to products.json")



if __name__ == "__main__":
    url = ("https://www.amazon.com/s?i=software-intl-ship&srs=16225008011&rh=n%3A16225008011&"
           "s=popularity-rank&fs=true&ref=lp_16225008011_sar")

    data = []
    driver = configure_driver()

    try:
        scrape_all_pages(driver, url)
        write_to_csv()
        write_to_json()
    finally:
        driver.quit()
        logger.info("Browser closed and script completed.")

    data_cleaning_and_analysis = DataCleaningAndAnalysis()
    data_cleaning_and_analysis.main()
