from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


def initialize_browser():
    """
        Initializing the browser with options, in headless mode,
        with custom user agent and without loading images for optimization
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/122.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.youtube.com/watch?v=VQRLujxTm3c")
    return driver


def scroll_to_load_comments(driver, scroll_pause=1, max_scrolls=2):
    """
        This function scrolls the page down to load some comments.
    """
    driver.execute_script("window.scrollTo(0, 800);")
    time.sleep(scroll_pause)

    for _ in range(max_scrolls):
        driver.execute_script("window.scrollBy(0, 1600);")
        time.sleep(scroll_pause)

        # Try to wait for at least one new comment
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-comment-thread-renderer"))
            )
        except:
            break


def extract_comments(driver):
    """
        Locates the comment blocks and extracts the data.
    """
    time.sleep(3)
    scroll_to_load_comments(driver)

    comment_blocks = driver.find_elements(By.CSS_SELECTOR, "ytd-comment-thread-renderer")

    comments_data = []
    for block in comment_blocks:
        try:
            author_elem = block.find_element(By.CSS_SELECTOR, "#author-text span")
            author = author_elem.get_attribute("textContent").strip()

            time_posted = block.find_element(By.CSS_SELECTOR, "#published-time-text a").text
            comment_text = block.find_element(By.CSS_SELECTOR, "#content-text span").text
            like_count_element = block.find_element(By.CSS_SELECTOR, "#vote-count-middle")
            likes = like_count_element.text.strip()
            likes = likes if likes else "0"

            comments_data.append({
                "author": author,
                "time_posted": time_posted,
                "comment_text": comment_text,
                "likes": likes
            })
        except Exception as e:
            print(f"Skipping one comment due to error: {e}")

    return comments_data


def write_to_csv(comments_data, csv_path):
    """
        This function writes the comments data to a CSV file, using pandas.
    """
    df = pd.DataFrame(comments_data)
    df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"\nSaved {len(comments_data)} comments to {csv_path}")



if __name__ == "__main__":
    csv_path = "datasets/comments.csv"
    
    driver = initialize_browser()
    comments = extract_comments(driver)
    driver.quit()

    write_to_csv(comments, csv_path)
