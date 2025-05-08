from lxml import etree
from bs4 import BeautifulSoup
import requests


class XPathHTMLParser:
    """Parses HTML content and extracts elements using XPath."""

    def __init__(self, url):
        self.url = url
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        self.soup = BeautifulSoup(response.text, "lxml")
        self.dom = etree.HTML(str(self.soup))  # Convert to lxml etree

    def get_element(self, xpath):
        """Returns the first matching element for the given XPath expression."""
        result = self.dom.xpath(xpath)
        return result[0] if result else None

    def get_elements(self, xpath):
        """Returns all matching elements for the given XPath expression."""
        return self.dom.xpath(xpath)

    def get_text(self, xpath):
        """Returns text content of the first matching element."""
        element = self.get_element(xpath)
        return element.text.strip() if element is not None else None

    def get_attribute(self, xpath, attribute):
        """Returns the specified attribute of an element found by XPath."""
        element = self.get_element(xpath)
        return element.get(attribute) if element is not None and attribute in element.attrib else None

    def get_links(self, xpath="//a/@href"):
        """Returns all href links found by the given XPath expression."""
        return self.dom.xpath(xpath)
