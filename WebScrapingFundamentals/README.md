### **README: Web Scraping Project**

This project consists of multiple classes that handle different aspects of web scraping, from making HTTP requests to parsing HTML and extracting data efficiently.

## Installing Dependencies and Running the project
To install the necessary dependencies in WebScrapingFundamentals directory run the following command
- pip install -r requirements.txt

## Testing the project
To run the project and test the scraper run the main.py file in the WebScrapingFundamentals directory
- python main.py

## **Task 1: HTTPRequest Class**
This class handles HTTP requests with different methods (GET, POST, PUT, DELETE). It manages headers for authentication and user-agent, securely handles HTTPS connections, and implements error handling for different HTTP status codes.

### **Methods:**
- `__init__(url, auth_token=None, user_agent=None)`: Initializes the request with a URL and optional authentication and user-agent headers.
- `_get_headers()`: Generates and returns headers for the request.
- `http_method(method)`: Sends an HTTP request using the specified method and returns the response.

## **Task 2: Parsing and Cleaning Classes**
### **HTMLContentParser Class**
Extracts specific elements using CSS selectors and provides functions to retrieve text, attributes, and elements.

### **Methods:**
- `get_element(selector)`: Finds and returns a single element based on the given CSS selector.
- `get_elements(selector)`: Finds and returns elements based on the given CSS selector.
- `get_text(selector)`: Extracts text content from selected elements.
- `get_attribute(selector)`: Extracts a specific attribute from an element using a CSS selector.
- `get_links(selector)`: Extracts all `<a>` tags from a specified section.
- `get_all_text()`: Extracts all visible text from the page.

### **XPathHTMLParser Class**
Implements XPath queries for complex element selection, similar to `HTMLContentParser` but using XPath syntax.

### **Methods:**
- `get_element(xpath)`: Finds and returns the first matching element for the given XPath expression.
- `get_elements(xpath)`: Finds and returns elements based on the given XPath expression.
- `get_text(xpath)`: Extracts text from elements matching the given XPath expression.
- `get_attribute(xpath, attr)`: Retrieves attribute values from elements found using XPath.
- `get_links(xpath, attr)`: Returns all `<a>` tag links found by the given XPath expression.

### **TextCleaner Class**
Provides a method to clean extracted text by removing whitespace, trimming, and applying regex transformations.

### **Methods:**
- `clean_text(text)`: Cleans text by trimming whitespace and applying regex-based formatting.

### **HTMLTreeNavigator Class**
The `HTMLTreeNavigator` class is designed to navigate and manipulate an HTML tree structure. It provides methods to traverse parent-child relationships, access siblings, search for elements, extract text, and visualize the document structure.

### **Methods:**
- `get_parent(element)`: Finds and returns the parent element of the given element.
- `get_children(element)`: Retrieves all direct child elements of the given element.
- `get_descendants(element)`: Returns all descendant elements of the given element.
- `get_next_sibling(element)`: Finds and returns the next sibling of the given element.
- `get_previous_sibling(element)`: Finds and returns the previous sibling of the given element.
- `find_element(tag, class_=None, id_=None)`: Finds and returns the first matching element by tag, class, or id.
- `find_all_elements(tag, class_=None, id_=None)`: Finds and returns all matching elements by tag, class, or id.
- `get_text(element)`: Extracts and returns the text content from the given element.
- `print_structure(element, level=0)`: Recursively prints the hierarchical structure of the given element.

## **Task 3: ECommerceScraper Class**
This class is used to scrape product data from an e-commerce website. It extracts product details, saves data into JSON and CSV files, downloads images, supports multi-page scraping, and tracks progress using logging.

### **Methods:**
- `__init__(url, number_of_pages=1)`: Initializes the scraper with a base URL and number of pages to scrape.
- `scrape_products()`: Scrapes product data (image, name, price) and saves it into CSV and JSON files.
- `save_to_csv(product_list)`: Saves the extracted product data to a CSV file.
- `save_to_json(product_list)`: Saves the extracted product data to a JSON file.
- `download_image(prod_name)`: Searches for a product in the CSV file, retrieves its image URL, and downloads the image.

## **Logging System**
This project implements a logging system to track errors and successful operations.

### **Logging Features:**
- Logs HTTP request status and errors.
- Tracks successful and failed data extraction.
- Logs downloaded images and failed downloads.
