import os
import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement



COOKIE_FILE = "medium_cookies.json"
email = ""  # Replace with logged in email
password = ""  # Replace with actual password

def save_cookies(driver, path):
    with open(path, 'w') as f:
        json.dump(driver.get_cookies(), f)

def load_cookies(driver, path):
    try:
        with open(path, 'r') as f:
            cookies = json.load(f)
            for cookie in cookies:
                if 'sameSite' in cookie:
                    del cookie['sameSite']  # Prevent potential error
                driver.add_cookie(cookie)
        return True
    except Exception as e:
        print(f"Failed to load cookies: {e}")
        return False

def is_logged_in(driver):
    """ Checks if article appears on the page, which should only be the case if logged in """
    time.sleep(3)
    articles = driver.find_elements(By.CSS_SELECTOR, "article[data-testid='post-preview']")
    return len(articles) > 0

def start_browser():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    return webdriver.Chrome(service=Service(), options=options)

def safe_relative_text(el: WebElement, xpath: str):
    try:
        return el.find_element(By.XPATH, xpath).text
    except NoSuchElementException:
        return ""

def safe_relative_attr(el: WebElement, xpath: str, attr: str):
    try:
        return el.find_element(By.XPATH, xpath).get_attribute(attr)
    except NoSuchElementException:
        return ""

def scraper(driver):
    articles_data = []

    # Find all article elements
    article_elements = driver.find_elements(By.CSS_SELECTOR, "article[data-testid='post-preview']")
    print(f"🔍 Found {len(article_elements)} articles")

    for i, article in enumerate(article_elements, start=1):
        try:
            description = safe_relative_text(article, ".//h3")
            title_element = article.find_element(By.XPATH, ".//h2")
            title = title_element.text.strip()
            anchor = title_element.find_element(By.XPATH, "./ancestor::a[1]")
            link = anchor.get_attribute("href")
            image_url = safe_relative_attr(article, ".//img", "src")

            articles_data.append({
                "title": title,
                "description": description,
                "link": link,
                "image_url": image_url,
            })

            print(f"Scraped article {i}: {title}")
        except Exception as e:
            print(f"⚠Failed to scrape article {i}: {e}")
            continue

    # Save to CSV
    df = pd.DataFrame(articles_data)
    df.to_csv("medium_articles.csv", index=False)
    print(f"\nSaved {len(articles_data)} articles to medium_articles.csv")

def main():
    driver = start_browser()
    driver.get("https://medium.com/")
    time.sleep(2)

    # Try cookies first
    if os.path.exists(COOKIE_FILE) and load_cookies(driver, COOKIE_FILE):
        driver.get("https://medium.com/")
        if is_logged_in(driver):
            print("Logged in using cookies.")
            scraper(driver)
            driver.quit()
            return
        else:
            print("⚠Cookies didn't work or expired. Logging in manually.")

    try:
        # Step 1: Click Sign in
        sign_in_btn = driver.find_element(By.LINK_TEXT, "Sign in")
        sign_in_btn.click()
        time.sleep(3)

        # Step 2: Sign in with Google
        google_sign_in = driver.find_element(By.XPATH, "//a[contains(@href, 'connect/google')]")
        google_sign_in.click()
        time.sleep(5)

        # Step 3: Wait for the email input field to appear and enter it
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_input.clear()
        email_input.send_keys(email)
        print(f"Entered email: {email}")

        # Step 4: Click Next button
        next_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']/parent::button"))
        )
        next_btn.click()
        print("➡Clicked 'Next' after email input.")

        # Step 5: Wait for the password input field to appear
        password_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "Passwd"))
        )
        time.sleep(1)  # Brief pause helps with stability
        password_input.clear()
        password_input.send_keys(password)
        print("Entered password.")

        # Step 6: Click Next button after password
        next_btn_pw = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']/parent::button"))
        )
        next_btn_pw.click()
        print("➡Clicked 'Next' after password input.")

        # Step 7: Wait for the user to complete 2FA authorization
        print("Please complete 2FA manually.")
    except Exception as e:
        print(f"Error during sign-in process: {e}")
        print("Manually navigate and log in if necessary.")

    # Wait for login to complete
    while True:
        if is_logged_in(driver):
            print("Login successful. Saving cookies.")
            save_cookies(driver, COOKIE_FILE)
            scraper(driver)
            break
        print("Waiting for login to complete...")
        time.sleep(5)

    driver.quit()



if __name__ == "__main__":
    main()
