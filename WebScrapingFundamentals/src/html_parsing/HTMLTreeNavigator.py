from bs4 import BeautifulSoup



class HTMLTreeNavigator:
    def __init__(self, html):
        """Initializes the navigator with an HTML document."""
        self.soup = BeautifulSoup(html, "lxml")

    def get_parent(self, element):
        """Returns the parent of the given element."""
        return element.parent if element else None

    def get_children(self, element):
        """Returns a list of direct children of the given element."""
        return list(element.children) if element else []

    def get_descendants(self, element):
        """Returns a list of all descendant elements."""
        return list(element.descendants) if element else []

    def get_next_sibling(self, element):
        """Returns the next sibling of the given element."""
        return element.next_sibling if element else None

    def get_previous_sibling(self, element):
        """Returns the previous sibling of the given element."""
        return element.previous_sibling if element else None

    def find_element(self, tag, class_=None, id_=None):
        """Finds the first matching element by tag, class, or id."""
        return self.soup.find(tag, class_=class_, id=id_)

    def find_all_elements(self, tag, class_=None, id_=None):
        """Finds all matching elements by tag, class, or id."""
        return self.soup.find_all(tag, class_=class_, id=id_)

    def get_text(self, element):
        """Extracts and returns the text from an element."""
        return element.get_text(strip=True) if element else ""

    def print_structure(self, element, level=0):
        """Recursively prints the structure of the given element."""
        if element:
            print("  " * level + str(element.name))
            for child in element.find_all(recursive=False):
                self.print_structure(child, level + 1)
