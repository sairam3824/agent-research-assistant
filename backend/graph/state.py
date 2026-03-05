from typing import TypedDict, List, Dict, Any
from pydantic import BaseModel


class Source(BaseModel):
    url: str
    title: str
    content: str
    credibility_score: float
    date: str | None = None


class Finding(BaseModel):
    claim: str
    sources: List[str]
    confidence: float
    sub_question: str


class ResearchState(TypedDict):
    question: str
    depth: str
    sub_questions: List[str]
    research_plan: Dict[str, Any]
    sources: List[Source]
    findings: List[Finding]
    analysis: Dict[str, Any]
    report: str
    critique: Dict[str, Any]
    current_phase: str
    progress_log: List[str]
