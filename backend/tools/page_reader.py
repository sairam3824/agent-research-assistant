import requests
from bs4 import BeautifulSoup
from typing import Dict
from config import MAX_CONTENT_LENGTH


class PageReader:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_and_extract(self, url: str) -> Dict[str, str]:
        """Fetch page and extract main content"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()
            
            # Get text
            text = soup.get_text(separator='\n', strip=True)
            
            # Get title
            title = soup.title.string if soup.title else url
            
            # Limit content length
            max_length = MAX_CONTENT_LENGTH
            if len(text) > max_length:
                text = text[:max_length] + "..."
            
            return {
                "url": url,
                "title": title,
                "content": text
            }
        except Exception as e:
            return {
                "url": url,
                "title": "Error fetching page",
                "content": f"Failed to fetch: {str(e)}"
            }
