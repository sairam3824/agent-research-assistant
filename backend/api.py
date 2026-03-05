from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse
import sys
from pathlib import Path
from typing import Any
import re

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from graph.workflow import create_research_workflow
from graph.state import ResearchState
from config import CORS_ORIGINS, validate_config
from utils.rate_limiter import rate_limiter
from utils.logger import logger
import asyncio
import json
import hashlib
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Research Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fail fast if required environment variables are missing.
validate_config()


class ResearchRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    depth: str = "advanced"


# Create reports directory
REPORTS_DIR = Path(__file__).resolve().parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


@app.post("/api/research")
async def research_stream(request: ResearchRequest, req: Request):
    """Stream research progress via SSE"""
    request_depth = request.depth if request.depth in {"basic", "advanced"} else "advanced"
    
    # Rate limiting
    client_id = req.client.host if req.client else "unknown"
    if not rate_limiter.is_allowed(client_id):
        wait_time = rate_limiter.get_wait_time(client_id)
        logger.warning(f"Rate limit exceeded for {client_id}")
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Please wait {wait_time:.0f} seconds."
        )
    
    logger.info(f"Starting research for question: {request.question[:100]}...")
    
    async def event_generator():
        workflow = create_research_workflow()
        
        initial_state: ResearchState = {
            "question": request.question,
            "depth": request_depth,
            "sub_questions": [],
            "research_plan": {},
            "sources": [],
            "findings": [],
            "analysis": {},
            "report": "",
            "critique": {},
            "current_phase": "Starting",
            "progress_log": []
        }
        
        try:
            # Run workflow
            for state in workflow.stream(initial_state):
                # Send progress updates
                for node_name, node_state in state.items():
                    yield {
                        "event": "progress",
                        "data": json.dumps({
                            "phase": node_state.get("current_phase", ""),
                            "logs": node_state.get("progress_log", [])
                        })
                    }
                    
                    # Send final report when complete
                    if node_state.get("current_phase") == "Complete":
                        # Serialize sources properly
                        sources_data = []
                        for s in node_state.get("sources", []):
                            if hasattr(s, 'model_dump'):
                                sources_data.append(s.model_dump())
                            elif hasattr(s, 'dict'):
                                sources_data.append(s.dict())
                            else:
                                sources_data.append(s)
                        
                        # Serialize findings properly
                        findings_data = []
                        for f in node_state.get("findings", []):
                            if hasattr(f, 'model_dump'):
                                findings_data.append(f.model_dump())
                            elif hasattr(f, 'dict'):
                                findings_data.append(f.dict())
                            else:
                                findings_data.append(f)
                        
                        report_data = {
                            "report": node_state.get("report", ""),
                            "critique": node_state.get("critique", {}),
                            "sources": sources_data,
                            "findings": findings_data
                        }
                        
                        # Save report to file
                        report_id = hashlib.md5(
                            f"{request.question}{datetime.now().isoformat()}".encode()
                        ).hexdigest()[:12]
                        
                        report_file = REPORTS_DIR / f"{report_id}.json"
                        with open(report_file, 'w') as f:
                            json.dump({
                                "id": report_id,
                                "question": request.question,
                                "timestamp": datetime.now().isoformat(),
                                **report_data
                            }, f, indent=2)
                        
                        logger.info(f"Report saved: {report_id}")
                        
                        # Add report ID to response
                        report_data["report_id"] = report_id
                        
                        yield {
                            "event": "complete",
                            "data": json.dumps(report_data)
                        }
                    
                    await asyncio.sleep(0.1)
        
        except Exception as e:
            logger.error(f"Research error: {str(e)}", exc_info=True)
            yield {
                "event": "error",
                "data": json.dumps({"error": str(e)})
            }
    
    return EventSourceResponse(event_generator())


@app.get("/api/report/{report_id}")
async def get_report(report_id: str):
    """Get a saved report by ID"""
    if not re.fullmatch(r"[a-f0-9]{12}", report_id):
        raise HTTPException(status_code=400, detail="Invalid report ID")

    report_file = REPORTS_DIR / f"{report_id}.json"
    
    if not report_file.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    
    try:
        with open(report_file, 'r') as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        raise HTTPException(status_code=500, detail="Report file unreadable")


@app.get("/api/reports")
async def list_reports(limit: int = 10):
    """List recent reports"""
    reports: list[dict[str, Any]] = []
    for report_file in REPORTS_DIR.glob("*.json"):
        try:
            with open(report_file, 'r') as f:
                data = json.load(f)
                reports.append({
                    "id": data.get("id"),
                    "question": data.get("question"),
                    "timestamp": data.get("timestamp")
                })
        except (OSError, json.JSONDecodeError):
            logger.warning(f"Skipping unreadable report file: {report_file}")

    safe_limit = max(1, min(limit, 100))
    reports.sort(key=lambda report: report.get("timestamp", ""), reverse=True)
    return {"reports": reports[:safe_limit]}


@app.get("/health")
async def health():
    return {"status": "ok"}
