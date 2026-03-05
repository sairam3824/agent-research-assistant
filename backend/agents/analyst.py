from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Dict, Any
from graph.state import Source, Finding
import json
from config import ANALYST_MODEL, ANALYST_TEMPERATURE


class AnalystAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model=ANALYST_MODEL, temperature=ANALYST_TEMPERATURE)
        
    def analyze(self, sub_questions: List[str], sources: List[Source]) -> Dict[str, Any]:
        """Cross-reference findings and identify patterns"""
        
        # Extract findings for each sub-question
        findings = []
        for sub_q in sub_questions:
            relevant_sources = self._filter_relevant_sources(sub_q, sources)
            finding = self._extract_finding(sub_q, relevant_sources)
            if finding:
                findings.append(finding)
        
        # Identify contradictions and gaps
        analysis = self._cross_reference(findings, sources)
        
        return {
            "findings": [f.dict() for f in findings],
            "agreements": analysis.get("agreements", []),
            "contradictions": analysis.get("contradictions", []),
            "knowledge_gaps": analysis.get("knowledge_gaps", []),
            "confidence_summary": analysis.get("confidence_summary", "")
        }
    
    def _filter_relevant_sources(self, sub_question: str, sources: List[Source]) -> List[Source]:
        """Filter sources relevant to a sub-question"""
        # Simple keyword matching - could be enhanced with embeddings
        keywords = sub_question.lower().split()
        relevant = []
        
        for source in sources:
            content_lower = (source.title + " " + source.content).lower()
            if any(keyword in content_lower for keyword in keywords):
                relevant.append(source)
        
        return relevant[:5]  # Top 5 most relevant
    
    def _extract_finding(self, sub_question: str, sources: List[Source]) -> Finding | None:
        """Extract key finding from sources"""
        if not sources:
            return None
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Analyze the provided sources and extract the key finding that answers the sub-question.
            
Return a JSON object with:
- claim: the main finding (1-2 sentences)
- confidence: float 0-1 based on source agreement and quality
- supporting_evidence: brief summary of evidence"""),
            ("user", """Sub-question: {sub_question}

Sources:
{sources}

Extract the key finding.""")
        ])
        
        sources_text = "\n\n".join([
            f"[{i+1}] {s.title} ({s.url})\nCredibility: {s.credibility_score}\n{s.content[:500]}..."
            for i, s in enumerate(sources)
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "sub_question": sub_question,
            "sources": sources_text
        })
        
        try:
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            
            data = json.loads(content.strip())
            
            return Finding(
                claim=data.get("claim", ""),
                sources=[s.url for s in sources],
                confidence=data.get("confidence", 0.5),
                sub_question=sub_question
            )
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"Warning: Failed to extract finding for '{sub_question}': {e}")
            return Finding(
                claim="Unable to extract clear finding",
                sources=[s.url for s in sources],
                confidence=0.3,
                sub_question=sub_question
            )
    
    def _cross_reference(self, findings: List[Finding], sources: List[Source]) -> Dict[str, Any]:
        """Identify patterns across findings"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Analyze these research findings and identify:
1. Key agreements across sources
2. Any contradictions or conflicting information
3. Knowledge gaps that need more research
4. Overall confidence assessment

Return JSON with: agreements (list), contradictions (list), knowledge_gaps (list), confidence_summary (string)"""),
            ("user", "Findings:\n{findings}")
        ])
        
        findings_text = "\n".join([
            f"- {f.claim} (confidence: {f.confidence})"
            for f in findings
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({"findings": findings_text})
        
        try:
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            return json.loads(content.strip())
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"Warning: Failed to parse cross-reference analysis: {e}")
            return {
                "agreements": [],
                "contradictions": [],
                "knowledge_gaps": [],
                "confidence_summary": "Analysis incomplete"
            }
