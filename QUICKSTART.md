# Quickstart

## 1. Install dependencies

```bash
./setup.sh
```

## 2. Configure environment

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` and set:

- `OPENAI_API_KEY`
- `TAVILY_API_KEY`

Optional:

- `OPENAI_MODEL` (default: `gpt-4o-mini`)
- `CORS_ORIGINS` (comma-separated; default: `http://localhost:3000`)

## 3. Start backend

```bash
cd backend
source venv/bin/activate
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

## 4. Start frontend

```bash
cd frontend
npm install
npm run dev
```

If backend is not on `http://localhost:8000`, set:

```bash
echo 'NEXT_PUBLIC_API_BASE_URL=http://localhost:8000' > frontend/.env.local
```

## 5. Open app

- [http://localhost:3000](http://localhost:3000)
- Shared report route: `/report/{report_id}`

## Terminal-only run

With backend running:

```bash
curl -N -H "Content-Type: application/json" \
  -X POST http://localhost:8000/api/research \
  -d '{"question":"What are recent advances in small language models?","depth":"advanced"}'
```
