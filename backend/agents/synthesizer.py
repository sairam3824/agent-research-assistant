from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any, List
from graph.state import Source, Finding
from config import SYNTHESIZER_MODEL, SYNTHESIZER_TEMPERATURE


class SynthesizerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model=SYNTHESIZER_MODEL, temperature=SYNTHESIZER_TEMPERATURE)
        
    def synthesize(
        self,
        question: str,
        findings: List[Finding],
        analysis: Dict[str, Any],
        sources: List[Source]
    ) -> str:
        """Compile findings into structured research report"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a research report writer. Create a comprehensive, well-structured research report.

Format:
# Research Report: [Question]

## Executive Summary
[3-4 sentence overview]

## Key Findings
[Numbered findings with citations]

## Analysis & Discussion
[Detailed analysis with cross-references]

## Knowledge Gaps & Open Questions
[Areas needing more research]

## Methodology
[What was searched, sources consulted]

## References
[Numbered list of all sources]

Use [1], [2] format for citations."""),
            ("user", """Question: {question}

Findings:
{findings}

Analysis:
{analysis}

Sources:
{sources}

Generate the report.""")
        ])
        
        findings_text = "\n".join([
            f"{i+1}. {f.claim} (confidence: {f.confidence:.2f})"
            for i, f in enumerate(findings)
        ])
        
        sources_text = "\n".join([
            f"[{i+1}] {s.title} - {s.url} (credibility: {s.credibility_score:.2f})"
            for i, s in enumerate(sources)
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "question": question,
            "findings": findings_text,
            "analysis": str(analysis),
            "sources": sources_text
        })
        
        return response.content
