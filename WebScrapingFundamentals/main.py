from WebScrapingFundamentals.src.HTTPRequest import HTTPRequest
from WebScrapingFundamentals.src.html_parsing.HTMLContentParser import HTMLContentParser
from WebScrapingFundamentals.src.html_parsing.XPathHTMLParser import XPathHTMLParser
from WebScrapingFundamentals.src.html_parsing.TextCleaner import TextCleaner
from WebScrapingFundamentals.src.html_parsing.HTMLTreeNavigator import HTMLTreeNavigator
from WebScrapingFundamentals.src.scraper.ECommerceScraper import ECommerceScraper



def task1():
    """ Testing the HTTPRequest class from the task 1"""
    http_request = HTTPRequest("https://httpbin.org/get", auth_token, user_agent)
    print("GET REQUEST\n", http_request.http_method('GET'))

    http_request = HTTPRequest("https://httpbin.org/post", auth_token, user_agent)
    print("\nPOST REQUEST\n", http_request.http_method("POST", data={"name": "John", "age": 30}))

    http_request = HTTPRequest("https://httpbin.org/put", auth_token, user_agent)
    print("\nPUT REQUEST\n", http_request.http_method("PUT", data={"name": "John", "age": 30}))

    http_request = HTTPRequest("https://httpbin.org/delete", auth_token, user_agent)
    print("\nDELETE REQUEST\n", http_request.http_method("DELETE", data={"name": "John", "age": 30}))

def task2():
    """ Testing task 2"""
    url = "https://quotes.toscrape.com"

    def test_html_content_parsing():
        """ Testing the HTML content parsing by specific css selectors"""
        parser = HTMLContentParser(url)

        # Extract and print the page title
        print("Page Title:", parser.get_text("title"), "\n")

        # Extract the first quote
        print("First Quote:", parser.get_text(".quote .text"), "\n")

        # Extract all author names
        authors = [author.get_text(strip=True) for author in parser.get_elements(".quote .author")]
        print("Authors:", authors, "\n")

        # Extract all tags from quotes
        tags = [tag.get_text(strip=True) for tag in parser.get_elements(".quote .tags .tag")]
        print("Tags:", tags, "\n")

        # Extract next page link
        next_page = parser.get_attribute(".next a", "href")
        print("Next Page Link:", f"{url}{next_page}" if next_page else "No next page", "\n")

        # Extract all text content
        print("All Visible Text:\n", parser.get_all_text(), "\n")

    def test_xpath_html_parser():
        """ Testing the XPath HTML parser by specific css selectors"""
        xpath_parser = XPathHTMLParser(url)

        # Extract Page Title
        print("Page Title:", xpath_parser.get_text("//title"))

        # Extract First Quote
        print("First Quote:", xpath_parser.get_text("//div[@class='quote']/span[@class='text']"))

        # Extract All Authors
        authors = xpath_parser.get_elements("//small[@class='author']")
        print("Authors:", [author.text for author in authors])

        # Extract All Tags
        tags = xpath_parser.get_elements("//div[@class='tags']/a[@class='tag']")
        print("Tags:", [tag.text for tag in tags])

        # Extract Next Page Link
        next_page = xpath_parser.get_attribute("//li[@class='next']/a", "href")
        print("Next Page Link:", f"{url}{next_page}" if next_page else "No next page")

        # Extract All Links
        links = xpath_parser.get_links()
        print("All Links:", links)

    def test_text_cleaner():
        """ Testing the text cleaner """
        raw_text = "  <p>Hello, <b>World</b>!   &nbsp; This is a    test &amp; example. </p>  "
        cleaned_text = TextCleaner.clean_text(raw_text)
        print("\nCleaning Test:", cleaned_text)

    def test_html_tree_navigator():
        """ Testing the HTML tree navigator """
        html_doc = """
        <html>
          <body>
            <div class='container'>
              <p class='text'><p class='text'>Hello World!</p></p>
              <p class='text'>Welcome to Web Scraping</p>
            </div>
          </body>
        </html>
        """

        navigator = HTMLTreeNavigator(html_doc)
        div = navigator.find_element("div", class_="container")
        print("Parent:", navigator.get_parent(div))
        print("\nChildren:", navigator.get_children(div))
        print("\nNext Sibling:", navigator.get_next_sibling(div))
        print("\nText Content:", navigator.get_text(div))
        navigator.print_structure(navigator.soup.body)

    test_html_content_parsing()
    test_xpath_html_parser()
    test_text_cleaner()
    test_html_tree_navigator()

def task3():
    """ Testing the E-Commerce data scraper """
    # Enter number of pages to scrape
    e_commerce_scraper = ECommerceScraper(url="https://scrapeme.live/shop/", number_of_pages=3)
    e_commerce_scraper.scrape_products()
    e_commerce_scraper.download_image("Charizard")



if __name__ == '__main__':
    auth_token = "exampletoken123"
    user_agent = "CustomClient/2.0"

    task1()
    task2()
    task3()
