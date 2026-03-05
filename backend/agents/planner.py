from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any
import json
from config import PLANNER_MODEL, PLANNER_TEMPERATURE


class PlannerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model=PLANNER_MODEL, temperature=PLANNER_TEMPERATURE)
        
    def plan(self, question: str) -> Dict[str, Any]:
        """Break down research question into sub-questions and create strategy"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a research planning expert. Given a research question, break it down into 3-5 focused sub-questions that will help answer the main question comprehensively.
            
For each sub-question, suggest search strategies.

Return a JSON object with:
- sub_questions: list of strings
- search_strategies: dict mapping each sub-question to search terms
- research_depth: "basic" or "advanced"
- estimated_sources: number of sources needed"""),
            ("user", "Research question: {question}")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({"question": question})
        
        try:
            # Parse JSON from response
            content = response.content
            # Extract JSON if wrapped in markdown
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            plan = json.loads(content.strip())
            return plan
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            # Fallback if JSON parsing fails
            print(f"Warning: Failed to parse planner response: {e}")
            return {
                "sub_questions": [question],
                "search_strategies": {question: [question]},
                "research_depth": "basic",
                "estimated_sources": 5
            }
