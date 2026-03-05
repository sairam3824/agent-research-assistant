from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any
import json
from config import CRITIC_MODEL, CRITIC_TEMPERATURE


class CriticAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model=CRITIC_MODEL, temperature=CRITIC_TEMPERATURE)
        
    def critique(self, report: str, sources: list) -> Dict[str, Any]:
        """Review report quality and suggest improvements"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a research quality reviewer. Evaluate this research report for:
1. Logical consistency
2. Citation completeness (all claims cited?)
3. Source diversity and potential bias
4. Areas needing deeper investigation

Return JSON with:
- quality_score: float 0-1
- strengths: list of strings
- weaknesses: list of strings
- suggestions: list of improvement suggestions
- bias_assessment: string"""),
            ("user", """Report:
{report}

Number of sources: {num_sources}

Evaluate the report.""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "report": report,
            "num_sources": len(sources)
        })
        
        try:
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            return json.loads(content.strip())
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"Warning: Failed to parse critique: {e}")
            return {
                "quality_score": 0.7,
                "strengths": ["Report generated"],
                "weaknesses": ["Unable to fully evaluate"],
                "suggestions": [],
                "bias_assessment": "Not assessed"
            }
