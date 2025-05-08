from bs4 import BeautifulSoup
from WebScrapingFundamentals.src.HTTPRequest import HTTPRequest


class HTMLContentParser:
    """Parses HTML content and extracts elements using CSS selectors."""
    def __init__(self, url, auth_token=None, user_agent=None):
        self.url = url
        self.http_request = HTTPRequest(url, auth_token, user_agent)
        response = self.http_request.http_method("GET")

        self.soup = BeautifulSoup(response, "lxml") if response else None

    def get_element(self, selector):
        """Extracts the first matching element using a CSS selector."""
        if not self.soup:
            return None
        return self.soup.select_one(selector)

    def get_elements(self, selector):
        """Extracts all matching elements using a CSS selector."""
        if not self.soup:
            return []
        return self.soup.select(selector)

    def get_text(self, selector):
        """Extracts the text content of an element using a CSS selector."""
        element = self.get_element(selector)
        return element.get_text(strip=True) if element else None

    def get_attribute(self, selector, attribute):
        """Extracts a specific attribute from an element using a CSS selector."""
        element = self.get_element(selector)
        return element[attribute] if element and element.has_attr(attribute) else None

    def get_links(self, selector="a"):
        """Extracts all links (<a> tags) from a specified section of the page."""
        elements = self.get_elements(selector)
        return [elem.get("href") for elem in elements if elem.get("href")]

    def get_all_text(self):
        """Extracts all visible text from the page, ignoring scripts and styles."""
        if not self.soup:
            return None
        for tag in self.soup(["script", "style"]):
            tag.extract()
        return self.soup.get_text(separator="\n", strip=True)
