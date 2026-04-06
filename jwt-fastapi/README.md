# JWT Authentication with FastAPI

This repo has two approaches — pick the one that fits your goal.

---

## Environment

Both approaches need a `JWT_SECRET` env variable. Copy the example env file:

```bash
cp .env.example .env
```

Then generate a secure secret:

```bash
python -c "import secrets; print('JWT_SECRET=' + secrets.token_hex(32))"
```

---

## Approach 1 — Single file (video / learning)

Everything in one file, great for following along with the video.

```bash
uv sync
uv run uvicorn jwt-fastapi:app --reload
```

**What's covered:**
1. Import dependencies
2. Configure JWT settings and create the app
3. Set up password hashing (Argon2 — stronger than bcrypt)
4. Create and decode access tokens
5. Build the `get_current_user` dependency
6. `POST /token` — login and get a token
7. `GET /me` — protected route

---

## Approach 2 — Structured project (real-world)

Proper folder structure following production conventions.

```
app/
├── config/       # environment variables
├── security/     # JWT helpers, password hashing, auth dependency
├── models/       # Pydantic schemas
├── routes/       # API routers
└── services/     # business logic
```

**Run locally:**

```bash
uv sync
uv run uvicorn app.app:app --reload
```

API available at `http://localhost:8000` — docs at `http://localhost:8000/docs`
```
