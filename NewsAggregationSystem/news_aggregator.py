from bs4 import BeautifulSoup
import requests



def request_content(url):
    """ Handles the requests and creates the BeautifulSoup object """
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        print("Request was Successful")
    else:
        soup = None
        print("Request was not Successful")

    return soup

def scrape_bbc_news(soup, url):
    """
    Scrape news data from BBC-NEWS News site
    Gets the articles based on BBC-NEWS News site and extract headlines, article summaries,
    links and categories of each article.
    """
    articles = soup.find_all("a", href=True)  # Ensures we get only links

    for article in articles:
        headline_tag = article.find("h2")
        article_summary = article.find("p")

        if headline_tag and article_summary:
            link = article["href"]  # get href link
            category = str(link).split("/")[1]  # extract category from the url

            # if the link doesn't contain the category, or maybe if its about some kind of ad, then we skip it
            if category == "":
                continue

            if not link.startswith("http"):
                link = f"{url}{link}"

            news_data.append(
                {
                    "headline": headline_tag.get_text(strip=True),
                    "url": link,
                    "summary": article_summary.get_text(strip=True),
                    "category": category,
                    "source": "bbc-news"
                }
            )

def scrape_nytimes_news(soup, url):
    """
    Scrape news data from NYTimes News site
    Gets the articles based on NYTimes News site and extract headlines, article summaries,
    links and categories of each article.
    """
    articles = soup.find("main", id="site-content").find_all("a", href=True)  # Ensures we get only links

    for article in articles[:-6]:
        p_tags = article.find_all("p")

        if not p_tags:
            continue

        headline_tag = p_tags[0]
        article_summary = p_tags[1] if len(p_tags) > 1 else ""

        if headline_tag and article_summary:
            link = article["href"]  # get href link
            category = str(link).split("/")[-2]  # extract category from the url

            # if the link doesn't contain the category, or maybe if its about some kind of ad, then we skip it
            if category == "":
                continue

            if not link.startswith("http"):
                link = f"{url}{link}"

            news_data.append(
                {
                    "headline": headline_tag.get_text(strip=True),
                    "url": link,
                    "summary": article_summary.get_text(strip=True),
                    "category": category,
                    "source": "nytimes"
                }
            )

def filter_articles_by_category(category):
    """Filter and display articles by category."""
    filtered = [item for item in news_data if item['category'].lower() == category.lower()]
    if not filtered:
        print(f"No articles found in the category: {category}")
    for item in filtered:
        print(f"Headline: {item['headline']}")
        print(f"Summary: {item['summary']}")
        print(f"Source: {item['source']}")
        print(f"URL: {item['url']}")
        print("-" * 50)

def search_articles_by_keyword(keyword):
    """Search articles by keyword in headline or summary."""
    found = [item for item in news_data if keyword.lower() in item['headline'].lower() or keyword.lower() in item['summary'].lower()]
    if not found:
        print(f"No articles found containing keyword: {keyword}")
    for item in found:
        print(f"Headline: {item['headline']}")
        print(f"Summary: {item['summary']}")
        print(f"Source: {item['source']}")
        print(f"URL: {item['url']}")
        print("-" * 50)

def display_menu():
    """Display command-line menu options."""
    print("\nNews Aggregator Menu:")
    print("1. View all news")
    print("2. Filter news by category")
    print("3. Search news by keyword")
    print("4. Exit")

def handle_user_choice():
    """Handle user input and call corresponding functions."""
    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ")
        if choice == '1':
            for item in news_data:
                print(f"Headline: {item['headline']}")
                print(f"Summary: {item['summary']}")
                print(f"Category: {item['category']}")
                print(f"Source: {item['source']}")
                print(f"URL: {item['url']}")
                print("-" * 50)
        elif choice == '2':
            category = input("Enter category to filter by: ")
            filter_articles_by_category(category)
        elif choice == '3':
            keyword = input("Enter keyword to search: ")
            search_articles_by_keyword(keyword)
        elif choice == '4':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


def news_aggregator():
    """Main function to fetch and display news."""
    bbc_news_url = "https://www.bbc.com"
    nytimes_url = "https://www.nytimes.com/"

    bbc_soup = request_content(bbc_news_url)
    nytimes_soup = request_content(nytimes_url)

    if bbc_soup:
        scrape_bbc_news(bbc_soup, bbc_news_url)
    if nytimes_soup:
        scrape_nytimes_news(nytimes_soup, nytimes_url)

    handle_user_choice()



if __name__ == '__main__':
    news_data = []
    news_aggregator()
