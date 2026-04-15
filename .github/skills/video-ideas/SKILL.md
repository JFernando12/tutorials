---
name: video-ideas
description: Generates new tutorial video ideas for @fernancode's Instagram and TikTok channel. Use this when asked for video ideas, content ideas, tutorial ideas, or what to build next.
---

You are helping @fernancode brainstorm new mini tutorial ideas for short-form videos on Instagram and TikTok. The format is always: one short video showing a concept step-by-step, backed by a real, clone-and-run project.

## Step 1 — Check what already exists

List the top-level directories in the repository. Each directory is an existing tutorial project. Avoid suggesting topics that are already covered.

## Step 2 — Research current trends

Search the web for what is trending right now in backend and full-stack development. Use queries like:

- "trending backend libraries 2025"
- "what developers are building with FastAPI 2025"
- "trending Python packages GitHub 2025"
- "popular developer tutorials Instagram TikTok 2025"
- "what is trending in web development 2025"

Also check GitHub Trending (https://github.com/trending) and look for:
- Libraries or tools with sudden spikes in stars
- Topics that appear repeatedly across multiple trending repos

## Step 3 — Generate ideas

Ideas come from two sources — both are equally valid:

**Trending:** topics with current buzz, new libraries, framework releases, viral dev content.

**Evergreen:** fundamental concepts every developer needs to know. These never go out of style and always get views. Examples of evergreen categories:
- Working with external APIs (REST, GraphQL, webhooks)
- Databases (SQL, NoSQL, ORMs, migrations, indexing)
- Authentication & authorization (JWT, OAuth, sessions, API keys)
- Caching (Redis, in-memory, HTTP caching)
- Background jobs & queues (workers, task queues, cron)
- File uploads & storage
- Email sending
- Environment & configuration management
- Logging & error handling
- Dockerizing an app
- Testing (unit, integration, mocking)
- Real-time features (WebSockets, SSE)
- Rate limiting & security basics

Mix both sources in the final list.

Produce a list of **10 video ideas**. For each idea, output a card in this format:

---
### 💡 [Short punchy title — as it would appear on screen]

**Type:** Trending | Evergreen
**Stack:** [language + main libraries]
**Hook:** [One sentence that grabs attention — what problem does this solve or what will the viewer learn?]
**Steps (single-file outline):**
1. Step 1 title
2. Step 2 title
3. Step 3 title
4. ...

**Why it works:** [One sentence on why this makes a great short video — trending buzz, search volume, or universal developer need]
---

## Guidelines for good ideas

- Each idea must be completable in a single file first, then refactorable into a structured project.
- Prefer topics where the viewer gets something **working and useful** by the end (not just theory).
- Prioritize topics with high search volume or community buzz right now.
- Mix difficulty levels: some beginner-friendly, some intermediate.
- Ideas can span any language or framework — not just Python/FastAPI.
- Avoid anything that requires a paid API key as the main feature.
- Short-form video sweet spot: 3–7 steps in the single-file version.

## Step 4 — Recommend the top 3

After the full list, highlight the **top 3 ideas** with the highest potential for engagement right now, and explain briefly why each one would perform well as a short video.
