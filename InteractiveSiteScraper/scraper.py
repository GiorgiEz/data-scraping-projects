from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
import time, csv


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument('--headless')  # headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def handle_privacy_popup(driver):
    try:
        # Wait for the pop-up container
        wait = WebDriverWait(driver, 10)
        got_it_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(text(), 'Got it')]"
        )))
        got_it_button.click()
        print("Privacy pop-up handled.")
    except Exception as e:
        print("No pop-up appeared or failed to click: ", e)


def perform_search(driver, search_term):
    try:
        wait = WebDriverWait(driver, 10)

        # Find and fill the search input
        search_input = wait.until(EC.presence_of_element_located((By.ID, "SearchText")))
        search_input.clear()
        search_input.send_keys(search_term)

        # Find and click the submit button
        submit_button = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, "button.RedSearchBar_RedSearchBar__submit__7hkcj"
        )))
        submit_button.click()
        print(f"Searched for '{search_term}'.")

        # Wait for search results to load
        time.sleep(5)
    except Exception as e:
        print("Search failed:", e)


def apply_free_filter(driver):
    try:
        wait = WebDriverWait(driver, 10)

        # Locate the checkbox by its label text "Free"
        free_label = wait.until(EC.presence_of_element_located((
            By.XPATH, "//label[.//span[text()='Free']]"
        )))

        checkbox = free_label.find_element(By.TAG_NAME, "input")

        # Click only if not already selected
        if not checkbox.is_selected():
            free_label.click()
            print("Free filter checkbox clicked.")

            # Wait for content to update after applying the filter
            time.sleep(5)
        else:
            print("Free filter already applied.")

    except Exception as e:
        print("Could not apply 'Free' filter:", e)

def select_checkbox_by_label(driver, label_text):
    try:
        wait = WebDriverWait(driver, 10)
        # Find the label that contains the span with the exact text
        label = wait.until(EC.presence_of_element_located((
            By.XPATH, f"//label[.//span[text()='{label_text}']]"
        )))
        checkbox = label.find_element(By.TAG_NAME, "input")

        if not checkbox.is_selected():
            label.click()
            print(f"Checkbox '{label_text}' selected.")
            time.sleep(3)  # Optional: allow time for page to refresh
        else:
            print(f"Checkbox '{label_text}' already selected.")
    except Exception as e:
        print(f"Failed to select checkbox '{label_text}':", e)


def scraper(driver):
    # Explicit wait before trying to scrape
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'SnowSearchProductFeed_List__grid')]"))
    )
    container = driver.find_element(By.XPATH, "//div[contains(@class, 'SnowSearchProductFeed_List__grid')]")
    products = container.find_elements(By.XPATH, ".//div[contains(@class, 'red-snippet_RedSnippet__container')]")

    print(f"Found {len(products)} products.")

    scraped_data = []

    for idx, product in enumerate(products, 1):
        try:
            current_price = product.find_element(By.XPATH,
                                                 ".//div[contains(@class, 'red-snippet_RedSnippet__priceNew')]").text
        except:
            current_price = None

        # Extract the block that might contain either rating or sold amount or both
        try:
            trust_items = product.find_elements(By.XPATH,
                                                ".//div[contains(@class, 'red-snippet_RedSnippet__trustItem')]//span")
            rating = None
            sold_amount = None
            for item in trust_items:
                text = item.text.strip().lower()
                if 'sold' in text:
                    sold_amount = item.text
                elif text.replace('.', '', 1).isdigit():
                    rating = item.text
        except:
            rating = None
            sold_amount = None

        try:
            description = product.find_element(By.XPATH,
                                               ".//div[contains(@class, 'red-snippet_RedSnippet__title')]").text
        except:
            description = None

        scraped_data.append({
            "current_price": current_price,
            "rating": rating,
            "sold_amount": sold_amount,
            "description": description
        })

        print(f"[{idx}] {scraped_data[-1]}")

    return scraped_data


def go_to_next_page(driver):
    # Stop if "Clear filters" button appears (i.e., no more results)
    try:
        driver.find_element(By.XPATH, "//button[.//span[text()='Clear filters']]")
        print("Reached last page (Clear filters button found).")
        return False
    except:
        pass  # Button not found, so continue

    try:
        wait = WebDriverWait(driver, 10)
        next_button = wait.until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[2]/div/div[6]/div/div/div[2]/div/div[3]/div/a[5]"
        )))
        href = next_button.get_attribute("href")
        if href:
            next_url = urljoin(driver.current_url, href)
            print(f"Navigating to next page: {next_url}")
            driver.get(next_url)

            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[contains(@class, 'SnowSearchProductFeed_List__grid')]"))
                )
            except Exception as e:
                print("Warning: Product container didn't load in time:", e)
                return False

            return True
        else:
            print("Next button href not found.")
            return False
    except Exception as e:
        print("Next page button not found or failed to navigate:", e)
        return False


def save_to_csv(data, filename="aliexpress_products.csv"):
    if not data:
        print("No data to save.")
        return

    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"Data saved to {filename}")


if __name__ == "__main__":
    url = "https://aliexpress.com"
    driver = setup_driver()
    driver.get(url)

    try:
        perform_search(driver, "computer")
        handle_privacy_popup(driver)
        apply_free_filter(driver)
        select_checkbox_by_label(driver, "Pink")

        all_data = []

        while True:
            page_data = scraper(driver)
            all_data.extend(page_data)

            if not go_to_next_page(driver):
                break

        save_to_csv(all_data)

    finally:
        driver.quit()
