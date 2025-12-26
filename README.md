# Digital Product Passport MVP

Battery passport starter kit aligned with EU Battery Regulation (Annex XIII public tier) and the 18 Feb 2027 compliance date. The stack follows the blueprint in `compass_artifact_wf-b7c7c716-8ff2-4235-a8ba-6c66138b6c5f_text_markdown.md`: Next.js for the public/ops UI, FastAPI for the REST API + QR generation, and PostgreSQL for storage.

## What you get
- Public `/scan/<uuid>` page for QR scans (public tier only)
- Registry + detail views for operators at `/passports`
- FastAPI CRUD (`/api/passports`) with QR PNGs and OpenAPI docs
- Pydantic schema covering all Annex XIII public fields and placeholders for restricted data
- Docker Compose to run Postgres + API + UI together

## Quick start (Docker)
```bash
docker compose up --build
# frontend: http://localhost:3000
# backend:  http://localhost:8000/docs (OpenAPI)
# scan page example: http://localhost:3000/scan/<passport-id>
```

## Quick start (manual dev)
Backend:
```bash
cd backend
python -m venv .venv && .\.venv\Scripts\activate  # or source .venv/bin/activate
pip install -r requirements.txt
set DATABASE_URL=sqlite:///./dev.db  # or your Postgres URL
uvicorn app.main:app --reload --port 8000
```

Frontend:
```bash
cd frontend
npm install
npm run dev -- --port 3000
# set NEXT_PUBLIC_API_BASE_URL if the backend runs elsewhere
```

## API overview
- `POST /api/passports` - create a passport (unique serial required)
- `GET /api/passports` - list passports (newest first)
- `GET /api/passports/{id}` - full record (incl. restricted_data)
- `PATCH /api/passports/{id}` - partial update
- `GET /api/passports/{id}/public` - public tier only
- `GET /api/passports/{id}/qr` - QR PNG pointing to `/scan/{id}`

The data model includes all mandatory public fields (manufacturer, model, manufacturing date/place, category, weight, status, carbon footprint, carbon class, recycled content, rated capacity, expected lifetime, hazardous substances) plus flexible JSON buckets for additional_public_data and restricted_data (conformity docs, dismantling instructions, test reports).

## Environment
- Backend: `DATABASE_URL`, `BASE_PUBLIC_URL` (defaults to `http://localhost:3000/scan`), `CORS_ORIGINS`
- Security/storage toggles: `ENFORCE_ORG_POLICIES=true` to apply Postgres RLS per org, `USE_S3=true` plus `S3_BUCKET`, `S3_REGION` (and optional `S3_ENDPOINT_URL`, AWS credentials) to store artifacts in S3/MinIO instead of local `/storage`.
- Frontend: `NEXT_PUBLIC_API_BASE_URL`, `NEXT_PUBLIC_SCAN_BASE`
Samples are in `backend/.env.example` and `frontend/.env.example`.

## Next steps (from the research)
1) Connect to Postgres/Supabase with RLS for tenant isolation.  
2) Add auth/roles (Clerk orgs or Supabase Auth) to gate restricted tiers.  
3) Expand exports (PDF, JSON-LD) and add audit logging on every write.  
4) Engage GS1 NL/Stichting OPEN for identifier and channel alignment.  
5) Add bulk import (Excel/CSV) and API keys for ERP connectors.
