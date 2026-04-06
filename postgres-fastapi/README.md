# PostgreSQL + FastAPI

This repo has two approaches — pick the one that fits your goal.

---

## Database

Both approaches need a running PostgreSQL instance. The easiest way:

```bash
docker compose up db -d
```

Then copy the example env file:

```bash
cp .env.example .env
```

---

## Approach 1 — Single file (video / learning)

Everything in one file, great for following along with the video.

```bash
uv sync
uv run uvicorn postgres-fastapi:app --reload
```

**What's covered:**
1. Import dependencies
2. Configure database connection
3. Define the Note model and schemas
4. Create the FastAPI app with lifespan (auto-creates tables)
5. `POST /notes` — create a note
6. `GET /notes` — list all notes
7. `GET /notes/{id}` — get a single note

---

## Approach 2 — Structured project (real-world)

Proper folder structure following production conventions.

```
app/
├── config/       # environment variables
├── database/     # engine, session dependency
├── models/       # SQLModel table definitions
├── routes/       # API routers
└── services/     # business logic
```

**Run locally:**

```bash
uv sync
uv run uvicorn app.app:app --reload
```

**Run with Docker (API + DB together):**

```bash
docker compose up --build
```

API available at `http://localhost:8000` — docs at `http://localhost:8000/docs`
