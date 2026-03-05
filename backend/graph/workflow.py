from langgraph.graph import StateGraph, END
from graph.state import ResearchState, Finding
from agents.planner import PlannerAgent
from agents.researcher import ResearcherAgent
from agents.analyst import AnalystAgent
from agents.synthesizer import SynthesizerAgent
from agents.critic import CriticAgent


def create_research_workflow():
    """Create the LangGraph workflow"""
    
    # Initialize agents
    planner = PlannerAgent()
    researcher = ResearcherAgent()
    analyst = AnalystAgent()
    synthesizer = SynthesizerAgent()
    critic = CriticAgent()
    
    # Define node functions
    def plan_node(state: ResearchState) -> ResearchState:
        state["current_phase"] = "Planning"
        state["progress_log"].append("🎯 Planning research strategy...")
        
        plan = planner.plan(state["question"])
        state["sub_questions"] = plan.get("sub_questions", [])
        state["research_plan"] = plan
        
        state["progress_log"].append(f"✓ Created {len(state['sub_questions'])} sub-questions")
        return state
    
    def research_node(state: ResearchState) -> ResearchState:
        state["current_phase"] = "Researching"
        state["progress_log"].append("🔍 Conducting research...")
        depth = state.get("depth", "advanced")
        
        all_sources = []
        for sub_q in state["sub_questions"]:
            state["progress_log"].append(f"  → Researching: {sub_q}")
            sources = researcher.research(sub_q, depth=depth)
            all_sources.extend(sources)
            state["progress_log"].append(f"    Found {len(sources)} sources")
        
        state["sources"] = all_sources
        state["progress_log"].append(f"✓ Collected {len(all_sources)} total sources")
        return state
    
    def analyze_node(state: ResearchState) -> ResearchState:
        state["current_phase"] = "Analyzing"
        state["progress_log"].append("📊 Analyzing findings...")
        
        analysis = analyst.analyze(state["sub_questions"], state["sources"])
        state["analysis"] = analysis
        
        # Convert finding dicts to Finding objects
        findings = []
        for f in analysis.get("findings", []):
            if isinstance(f, dict):
                findings.append(Finding(**f))
            else:
                findings.append(f)
        state["findings"] = findings
        
        state["progress_log"].append(f"✓ Identified {len(findings)} key findings")
        return state
    
    def synthesize_node(state: ResearchState) -> ResearchState:
        state["current_phase"] = "Synthesizing"
        state["progress_log"].append("📝 Writing report...")
        
        findings = [Finding(**f) if isinstance(f, dict) else f for f in state.get("findings", [])]
        
        report = synthesizer.synthesize(
            state["question"],
            findings,
            state["analysis"],
            state["sources"]
        )
        state["report"] = report
        
        state["progress_log"].append("✓ Report generated")
        return state
    
    def critique_node(state: ResearchState) -> ResearchState:
        state["current_phase"] = "Reviewing"
        state["progress_log"].append("🔎 Quality check...")
        
        critique = critic.critique(state["report"], state["sources"])
        state["critique"] = critique
        
        state["progress_log"].append(f"✓ Quality score: {critique.get('quality_score', 0):.2f}")
        state["current_phase"] = "Complete"
        return state
    
    # Build graph
    workflow = StateGraph(ResearchState)
    
    workflow.add_node("planner", plan_node)
    workflow.add_node("researcher", research_node)
    workflow.add_node("analyst", analyze_node)
    workflow.add_node("synthesizer", synthesize_node)
    workflow.add_node("critic", critique_node)
    
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "analyst")
    workflow.add_edge("analyst", "synthesizer")
    workflow.add_edge("synthesizer", "critic")
    workflow.add_edge("critic", END)
    
    return workflow.compile()
