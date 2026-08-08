# AI Resume Builder

A full-stack resume builder with LLM-assisted content generation, built with FastAPI, PostgreSQL, and React.

## What it does

- **Auth** — JWT-based signup/login
- **Resume CRUD** — structured resume data (personal info, education, projects, skills, extracurricular), scoped per user
- **AI bullet optimizer** — rewrites a raw resume bullet into the XYZ formula ("Accomplished X, measured by Y, by doing Z") using Groq's LLM API
- **AI project generator** — paste a public GitHub repo URL, and the app fetches the repo's metadata + README, then generates a structured project entry (name, tech tags, achievement bullets) and a categorized skills breakdown
- **GitHub profile skill sync** — aggregates languages across a user's public GitHub repos and categorizes them into resume skill groups
- **PDF export** — server-rendered PDF styled to match a clean, single-column academic resume layout

## Why this is more than "call an LLM and print the output"

Every AI-generated field in this project goes through the same discipline:

1. **Schema-validated output.** The LLM is instructed to return JSON matching a specific shape, and the response is parsed and validated against a Pydantic model before it's ever returned to the client. Malformed output is caught and surfaced as a clean `502`, not a crash.
2. **Explicit anti-hallucination constraints.** Every prompt that touches resume content forbids the model from inventing metrics, percentages, user counts, or claims ("production", "live") not clearly supported by what the user gave it. Where a metric is genuinely unknown, the model is told to either use a placeholder (`[X%]`) or drop the number entirely and write a qualitative bullet instead — never to fill the gap with something plausible-sounding but false. This matters more than it might sound: resumes are documents people use to represent themselves for real opportunities, and an LLM will confidently fabricate a "40% improvement" out of nothing if you let it.
3. **Provider abstraction.** The Groq client sits behind a single `generate_json()` function, so the rest of the app doesn't know or care which LLM provider is behind it.

## Architecture

```
app/
├── auth/          # JWT auth, signup/login, get_current_user dependency
├── resumes/        # Resume CRUD, ownership-scoped endpoints
├── ai/             # Groq client, prompt builders, GitHub API fetchers
├── export/          # ReportLab-based PDF generation
└── core/            # config, DB session
```

**Backend:** FastAPI, SQLAlchemy 2.0 (async), PostgreSQL, PyJWT, passlib/bcrypt
**AI:** Groq API (`openai/gpt-oss-20b`), called directly via REST for reliability
**PDF:** ReportLab (Platypus flowables) — chosen over WeasyPrint/Playwright after WeasyPrint's native GTK dependency proved unreliable on Windows
**Frontend:** React (Vite), React Router, Axios — JWT held in memory only (not localStorage), traded off against session persistence to reduce XSS exposure

## Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Create a `.env` file:
```
DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost:5432/resume_builder
SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_hex(32))">
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
GROQ_API_KEY=<your key from console.groq.com>
```

```bash
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Known limitations / next steps

- No JD/ATS keyword-matching feature yet (scoped but not built)
- No Alembic migrations — schema changes currently require dropping/recreating tables in development
- GitHub profile skill sync makes up to ~30 API calls per sync (one per repo), which eats into GitHub's unauthenticated 60 req/hour rate limit fairly fast