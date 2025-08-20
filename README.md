# Truck Audit App — Full Stack (FastAPI + React + Postgres)

This repository contains a full-stack app:
- Backend: FastAPI (backend/)
- Frontend: React + Vite (frontend/)
- Dockerfile builds the frontend and backend into a single image
- render.yaml for Render blueprint (web service + Postgres DB)

## Quick local dev (sqlite)
1. Backend:
   ```bash
   cd backend
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   export DATABASE_URL=sqlite:///./dev.db
   uvicorn app.main:app --reload --app-dir backend
   ```
2. Frontend:
   ```bash
   cd frontend
   npm i
   VITE_API_URL=http://localhost:8000 npm run dev
   ```

## Deploy to Render
1. Push repo to GitHub.
2. In Render, create a Blueprint and select the repo.
3. Render will create a web service and a Postgres DB per render.yaml.
4. Set any required env vars in the web service (SECRET_KEY if you want to override generated).
5. Deploy — site root serves frontend; API under /api/*.
