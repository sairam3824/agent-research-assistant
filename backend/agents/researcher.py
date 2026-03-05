from typing import List
from tools.web_search import WebSearchTool
from tools.page_reader import PageReader
from tools.arxiv_search import ArxivSearchTool
from graph.state import Source
from config import (
    MAX_SEARCH_RESULTS,
    MAX_ARXIV_RESULTS,
)


class ResearcherAgent:
    def __init__(self):
        self.web_search = WebSearchTool()
        self.page_reader = PageReader()
        self.arxiv_search = ArxivSearchTool()
        
    def research(
        self,
        sub_question: str,
        depth: str = "advanced",
        is_academic: bool = False
    ) -> List[Source]:
        """Conduct research for a sub-question"""
        sources = []
        is_advanced = depth == "advanced"
        web_result_limit = MAX_SEARCH_RESULTS if is_advanced else max(1, MAX_SEARCH_RESULTS // 2)
        
        # Web search
        search_results = self.web_search.search(sub_question, max_results=web_result_limit)
        
        for result in search_results:
            # Fetch full content
            page_data = self.page_reader.fetch_and_extract(result.get("url", ""))
            
            # Evaluate credibility
            credibility = self._evaluate_credibility(
                result.get("url", ""),
                page_data.get("content", "")
            )
            
            sources.append(Source(
                url=result.get("url", ""),
                title=result.get("title", page_data.get("title", "Unknown")),
                content=page_data.get("content", result.get("content", "")),
                credibility_score=credibility,
                date=result.get("published_date")
            ))
        
        # Academic search if needed
        if is_advanced and (
            is_academic or any(word in sub_question.lower() for word in ["research", "study", "paper", "academic"])
        ):
            arxiv_results = self.arxiv_search.search(sub_question, max_results=MAX_ARXIV_RESULTS)
            for paper in arxiv_results:
                sources.append(Source(
                    url=paper["url"],
                    title=paper["title"],
                    content=paper["summary"],
                    credibility_score=0.9,  # Academic papers get high credibility
                    date=paper["published"]
                ))
        
        return sources
    
    def _evaluate_credibility(self, url: str, content: str) -> float:
        """Simple credibility scoring based on domain and content quality"""
        score = 0.5  # Base score
        
        # Domain authority
        trusted_domains = [".edu", ".gov", ".org", "arxiv.org", "nature.com", "science.org"]
        if any(domain in url for domain in trusted_domains):
            score += 0.3
        
        # Content quality indicators
        if len(content) > 1000:
            score += 0.1
        if any(word in content.lower() for word in ["research", "study", "data", "analysis"]):
            score += 0.1
        
        return min(score, 1.0)
