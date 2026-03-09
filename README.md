# Agent Research Assistant

Autonomous research assistant with a FastAPI backend and Next.js frontend.

It takes a research question, runs a multi-step agent workflow, streams progress, and returns:

- a final markdown report
- extracted findings
- source list with credibility scores
- a quality critique

## Stack

- Backend: FastAPI, LangGraph, LangChain OpenAI, Tavily, arXiv
- Frontend: Next.js 14, React, Tailwind
- Streaming: Server-Sent Events (SSE)

## Current Status (Verified)

The following checks pass in this repository:

- backend dependency installation
- backend module import (`import api`)
- frontend lint
- frontend production build
- setup verification script (`verify.sh`) except missing API keys if `.env` is not set yet

## Important Runtime Notes

- No repository can guarantee "zero bugs" in all environments.
- This app still depends on runtime conditions:
- valid `OPENAI_API_KEY` and `TAVILY_API_KEY`
- internet/API availability
- provider quotas/rate limits
- Python 3.14 currently shows a non-fatal LangChain warning; app still imports and runs.

## Requirements

- Python 3
- Node.js + npm

## Setup

```bash
./setup.sh
cp backend/.env.example backend/.env
```

Edit `backend/.env` and add:

- `OPENAI_API_KEY`
- `TAVILY_API_KEY`

Optional:

- `OPENAI_MODEL` (default `gpt-4o-mini`)
- `CORS_ORIGINS` (default `http://localhost:3000`)

## Run the Application

### 1. Start backend

```bash
cd backend
source venv/bin/activate
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start frontend

In a new terminal:

```bash
cd frontend
npm install
npm run dev
```

If your backend URL is different:

```bash
echo 'NEXT_PUBLIC_API_BASE_URL=http://localhost:8000' > frontend/.env.local
```

### 3. Open app

- http://localhost:3000
- Shared report page: `/report/{report_id}`

## Terminal-Only Usage

With backend running:

```bash
curl -N -H "Content-Type: application/json" \
  -X POST http://localhost:8000/api/research \
  -d '{"question":"What are recent advances in small language models?","depth":"advanced"}'
```

## Verification

Run:

```bash
bash verify.sh
```

## Project Docs

- Quickstart: `QUICKSTART.md`
- Minimal run checklist: `torun.txt`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
