# Copilot Instructions

This is **@fernancode's** tutorial repository. Each directory is a self-contained mini-project used as the basis for short-form tutorials on Instagram and TikTok. Projects span multiple languages and frameworks.

## Repository Purpose & Structure

Every project lives in its own top-level directory and must be independently runnable after a minimal setup. A root `README.md` indexes all projects.

### Each project directory must contain

| File / Dir | Purpose |
|---|---|
| `<project-name>.py` (or equivalent single file) | Step-by-step tutorial file — mirrors the video |
| `app/` (or equivalent structured dir) | Production-style full project |
| `README.md` | Setup and run instructions for both versions |
| `.env.example` | All required env vars with working defaults where possible |
| `.gitignore` | Ignore `.env`, `__pycache__`, `.venv`, build artifacts, etc. |
| `docker-compose.yaml` | **Required** when the project depends on any external service (DB, cache, queue, etc.) |

---

## Project Conventions

### 1. Clone-and-run first

Every project must be runnable with the fewest possible steps after cloning:

1. `cp .env.example .env` (and fill in any secrets that can't ship with defaults)
2. Start external services: `docker compose up <service> -d`
3. Install deps and run

`.env.example` must ship with **working defaults** for everything except secrets (passwords, API keys). Never leave a variable blank if a safe default exists.

### 2. Single-file version — step-by-step tutorial file

The single file (e.g., `jwt-fastapi.py`) mirrors the video. It must:

- Use numbered step comments as section separators — use the comment syntax of the language:
  ```python
  # Step 1: Import dependencies
  # Step 2: Configure JWT settings and create the app
  ```
- Be **complete and runnable** on its own (not just stubs/placeholders)
- Steps must match the "What's covered" list in `README.md`
- Keep it flat — no sub-imports, everything in one file

### 3. Structured project — full `app/` layout

The structured version shows the production-ready architecture. It must match the single-file in functionality.

#### Python/FastAPI projects

```
app/
├── app.py          # FastAPI factory: create_app(), router registration, lifespan
├── config/         # env singleton (app/config/environment.py → env object)
├── models/         # Pydantic / SQLModel schemas
├── routes/         # Thin APIRouter handlers — one call to a service, nothing more
├── services/       # All business logic
├── security/       # (auth projects) JWT, hashing, auth dependency
└── database/       # (DB projects) engine, session factory, SessionDep
```

`main.py` at the project root is the `uvicorn.run` entry point only.

For other languages/frameworks, follow the same principle: config, models, routes/controllers, services — each in its own layer.

### 4. `__init__.py` re-exports (Python)

Every subpackage exposes its public API through `__init__.py`. Import from the package, not the internal module:

```python
# ✅
from app.security import CurrentUserDep
# ❌
from app.security.security import CurrentUserDep
```

### 5. README structure

Each project `README.md` must follow this structure:

```markdown
# <Project Title>

One-line description.

---

## Setup

Steps to copy .env and start external services (if any).

---

## Approach 1 — Single file (video / learning)

Run command + "What's covered" numbered list matching the step comments.

---

## Approach 2 — Structured project (real-world)

Folder tree + run command (+ Docker run command if applicable).
```

### 6. Docker Compose

Any project that requires an external service (database, cache, broker, etc.) must include a `docker-compose.yaml` with:
- The external service(s) with a `healthcheck`
- An `api` service that `depends_on` the external service with `condition: service_healthy`
- A named volume for persistent data

---

## Existing Projects

| Directory | Stack | Description |
|---|---|---|
| `jwt-fastapi/` | Python, FastAPI, PyJWT, pwdlib | JWT authentication with Argon2 password hashing |
| `postgres-fastapi/` | Python, FastAPI, SQLModel, PostgreSQL | PostgreSQL CRUD API with Docker |

---

## Python-specific Notes

- **Package manager**: `uv`. Always use `uv sync` and `uv run`.
- **Python version**: 3.12+. Use modern syntax (`X | Y` unions, `list[X]` generics).
- **Password hashing**: `pwdlib[argon2]` (Argon2), not bcrypt.
- **Config**: a single `env = Environment()` singleton in `app/config/environment.py`, loaded via `python-dotenv`. All config accessed as `env.ATTRIBUTE`.
- **Dependency injection aliases**: use `Annotated` type aliases (`CurrentUserDep`, `SessionDep`) as parameter type hints in route functions.
- **Timing-safe auth**: always do a dummy hash verification when a user is not found to prevent timing-based user enumeration.
