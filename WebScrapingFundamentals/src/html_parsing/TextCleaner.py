import re
import html
from bs4 import BeautifulSoup



class TextCleaner:
    @staticmethod
    def clean_text(text):
        if not text:
            return ""

        # 1. Remove HTML tags
        text = BeautifulSoup(text, "lxml").text

        # 2. Decode HTML entities (&amp; → &)
        text = html.unescape(text)

        # 3. Normalize whitespace (removes multiple spaces and trims)
        text = re.sub(r'\s+', ' ', text).strip()

        # 4. Normalize Unicode (remove special characters)
        text = text.encode('utf-8').decode('ascii', 'ignore')

        return text
