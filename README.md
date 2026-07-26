# AI Job Application Agent

An autonomous agent that finds remote jobs, filters them with an LLM, generates tailored resumes and cover letters, and automates the application process using Playwright.

## What it does

1. **Collects** remote job listings from multiple job boards (Jobicy, We Work Remotely)
2. **Filters** each job with an LLM against a configurable profile (target roles, countries, minimum match score)
3. **Generates** a tailored resume and cover letter per job (DOCX export)
4. **Applies** automatically via Playwright — detects the apply flow, uploads documents, fills text inputs, dropdowns, radio buttons, checkboxes, and textareas (with AI-generated answers for open-ended questions)
5. Tracks every job's status, application result, and errors in a local database

## Tech stack

- **Python**
- **SQLAlchemy + SQLite** — job tracking and application state
- **Playwright** — browser automation for applying
- **Groq** — LLM provider for filtering and content generation (multi-provider architecture, Gemini/OpenAI-ready)

## Architecture

```
backend/
├── app/
│   ├── agents/       # job source fetchers, analyzer, resume/cover letter generators, Playwright automation
│   ├── database/     # SQLAlchemy models and session setup
│   ├── models/        # Job model
│   ├── prompts/       # LLM prompt templates
│   └── services/      # LLM provider abstraction
├── save_jobs.py        # fetch + filter jobs → DB
├── analyze_jobs.py     # LLM scoring pass
├── generate_resumes.py # resume + cover letter generation
├── apply_jobs.py       # Playwright application runner
└── create_db.py        # DB schema setup
```

**Pipeline:** `save_jobs.py` → `analyze_jobs.py` → `generate_resumes.py` → `apply_jobs.py`

**Design rule:** `apply_jobs.py` owns all database writes (status, timestamps, errors). The Playwright agent only automates the browser and returns a result — it never touches the database directly.

## Setup

```bash
git clone https://github.com/nikhilvanjari02nv-create/AI-job-application-agent.git
cd AI-job-application-agent/backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
playwright install
```

Copy the example env and profile files and fill in your own values:
```bash
cp .env.example .env
cp app/profile.py.example app/profile.py
```

Create the database:
```bash
python create_db.py
```

Run the pipeline:
```bash
python save_jobs.py
python analyze_jobs.py
python generate_resumes.py
python apply_jobs.py
```

`apply_jobs.py` runs in `DRY_RUN` mode by default with a configurable `MAX_APPLICATIONS` cap — review before disabling dry run.

## Known limitations

- **Bot detection:** Some job aggregators use Cloudflare-style human verification checks that block headless automation at the fetch or apply stage. RemoteOK and Remotive were dropped from the source list for this reason. This is a known, intentional constraint, not a bug — automatically defeating these checks is out of scope for this project.
- **Generic form handling only:** The Playwright agent currently uses a generic apply flow rather than ATS-specific handlers (Greenhouse, Lever, Workday, etc.). ATS-specific handlers are a planned next step, to be built only where the generic flow proves insufficient after real-world testing.
- **Human-in-the-loop by design:** `AUTO_APPLY` defaults to `False`. This project is built to assist and speed up applying, not to fully replace human review before submission.

## Status

Foundation (data pipeline, resume/cover letter generation, generic Playwright automation): substantially complete.
Automation reliability across varied job sites: in progress — actively being improved based on real-world test results.
