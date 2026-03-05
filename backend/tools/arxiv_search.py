import arxiv
from typing import List, Dict


class ArxivSearchTool:
    def search(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search arXiv for academic papers"""
        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            results = []
            for paper in search.results():
                results.append({
                    "title": paper.title,
                    "url": paper.entry_id,
                    "summary": paper.summary[:500] + "...",
                    "authors": [author.name for author in paper.authors],
                    "published": paper.published.strftime("%Y-%m-%d"),
                    "pdf_url": paper.pdf_url
                })
            
            return results
        except Exception as e:
            print(f"arXiv search error: {e}")
            return []
