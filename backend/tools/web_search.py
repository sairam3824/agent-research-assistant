import os
from typing import List, Dict
from tavily import TavilyClient
from config import SEARCH_DEPTH


class WebSearchTool:
    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY not found in environment")
        self.client = TavilyClient(api_key=api_key)
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search the web using Tavily API"""
        try:
            response = self.client.search(
                query=query,
                max_results=max_results,
                search_depth=SEARCH_DEPTH
            )
            return response.get("results", [])
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def get_search_context(self, query: str) -> str:
        """Get aggregated context from search results"""
        try:
            response = self.client.get_search_context(query=query)
            return response
        except Exception as e:
            print(f"Context error: {e}")
            return ""
