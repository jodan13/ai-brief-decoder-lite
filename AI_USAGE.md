# AI Usage

## Tools Used

- Codex / ChatGPT for repository scaffolding, backend flow design, tests, and extension implementation.

## Delegated Work

- Generated the initial FastAPI layered structure.
- Drafted SQLAlchemy/Alembic persistence.
- Created deterministic fake provider cases for local validation.
- Built the minimal WXT React popup and typed API client.
- Drafted README setup and verification instructions.

## Example Prompts

1. Implement a minimal vertical slice for a FastAPI backend that stores brief decode runs.
2. Create a deterministic fake LLM provider that returns structured JSON and failure modes.
3. Add Pydantic validation tests for malformed JSON and invalid enum values.
4. Build a lightweight WXT React popup for submitting text and rendering structured results.
5. Write concise README commands for Docker, uv, pytest, pyright, ruff, and WXT.

## Accepted, Changed, Rejected

- Accepted: protocol-based provider/repository boundaries, Pydantic response contracts, async SQLAlchemy repository.
- Changed: API tests use dependency injection with an in-memory repository so the unit test suite is fast and does not require Docker.
- Rejected: real LLM integration, auth, queues, heavy UI libraries, and deployment automation for stage 1.

## Verification

- Backend checks are intended to run with:
  - `uv run pytest`
  - `uv run pyright`
  - `uv run ruff check .`
  - `uv run ruff format --check .`
- Extension checks are intended to run with:
  - `npm run typecheck`
  - `npm run build`
- Submission stabilization run:
  - Passed: `docker compose ps` with PostgreSQL `db` service healthy.
  - Passed: `uv sync`
  - Passed: `uv run alembic upgrade head`
  - Passed: `uv run pytest`
  - Passed: `uv run pyright`
  - Passed: `uv run ruff check .`
  - Passed: `uv run ruff format --check .`
  - Passed: `npm install`
  - Passed: `npm run typecheck`
  - Passed: `npm run build`
  - Passed: `npm audit --omit=dev`

## Known Limitations

- The fake provider is deterministic and does not infer deeply from the input.
- The frontend stores no history and only renders the current response.
- PostgreSQL integration is configured through Alembic and SQLAlchemy, while tests use an in-memory repository for speed.
