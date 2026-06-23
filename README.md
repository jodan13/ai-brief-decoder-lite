# AI Brief Decoder Lite

Minimal working test-assignment slice:

Chrome Extension popup -> FastAPI backend -> fake LLM provider -> Pydantic structured output validation -> PostgreSQL persistence -> rendered popup result.

## What Works

- `GET /health`
- `POST /v1/briefs/decode`
- `GET /v1/briefs/runs/{run_id}`
- Deterministic fake provider with configurable failure modes.
- Pydantic v2 validation for structured provider output.
- Async SQLAlchemy 2 repository over PostgreSQL/asyncpg.
- Alembic migration for `decode_runs`.
- Backend tests for validation, happy path, and safe failure handling.
- Minimal WXT React popup with typed API client, loading/error states, result rendering, and JSON copy.

## Prerequisites

- Python 3.12
- uv
- Docker with the Docker daemon running
- Node.js 20+

## Backend

```bash
docker compose up -d db
cd backend
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

Run checks:

```bash
cd backend
uv run pytest
uv run pyright
uv run ruff check .
uv run ruff format --check .
```

Exercise the API:

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/v1/briefs/decode \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Build a small launch plan for a browser extension\"}"
```

Provider modes:

- `fake_success`
- `fake_invalid_severity`
- `fake_malformed_json`
- `fake_missing_fields`
- `fake_provider_error`

Set `BRIEF_PROVIDER_MODE` to exercise failure paths locally.

## Extension

```bash
cd extension
npm install
npm run dev
npm run build
npm run typecheck
```

The popup calls `VITE_API_BASE_URL`, defaulting to `http://localhost:8000`.

## Environment

Copy `.env.example` values into your local environment or shell. Do not commit real secrets. Stage 1 does not require any paid LLM key.

## Assumptions and Tradeoffs

- This is a submission-focused MVP, so the provider is deterministic and no real LLM key is required.
- PostgreSQL is used for the runtime persistence path; backend API tests use an in-memory repository to stay fast and deterministic.
- The extension is intentionally minimal and calls the backend directly through `VITE_API_BASE_URL`.
- Deployment, authentication, background jobs, and production observability are out of scope for this slice.

## Known Limitations

- No real LLM provider is implemented.
- No auth, queues, billing, or background jobs.
- API tests use an in-memory repository; the Alembic migration covers the PostgreSQL table creation path.
- CORS defaults are local-development oriented. For a packaged extension, keep `CORS_ORIGIN_REGEX` restrictive or configure exact extension origins.
