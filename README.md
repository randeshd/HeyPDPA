# HeyPDPA!

A compliance analysis tool that reviews an organization's governance and security documents against Sri Lanka's Personal Data Protection Act (PDPA), Act No. 9 of 2022, as amended by Act No. 22 of 2025.

**Live app:** https://hey-pdpa.vercel.app

## What it does

Upload a governance or security document (PDF or DOCX) and get an instant gap analysis against 23 structured PDPA requirements — spanning lawful basis for processing, data subject rights, DPO appointment, breach notification, cross-border data flow, and more. For each requirement, the tool reports whether the document shows evidence it is **Met**, **Partially Met**, or **Not Addressed**, along with a short explanation, an overall compliance percentage, and prioritized, actionable recommendations for the most significant gaps.

The checklist tracks each requirement's legal enforcement status separately from its severity, since most PDPA provisions are not yet in force in Sri Lanka. This lets an organization see both how prepared it is and what is currently legally binding, without conflating the two.

## Features

- **Checker** — upload a PDF/DOCX, get a full 23-point gap analysis with a compliance score, requirement-by-requirement breakdown, and recommendations
- **Requirements** — browse all 23 checklist items with search, category, severity, and enforcement-status filters
- **How It Works** — explains the extraction → checklist → AI analysis → scoring pipeline
- **Scoring** — documents the exact scoring model: points per status, the score formula, score bands, and how severity relates to the score
- **Disclaimer** — scope and limitations notice

## Tech stack

- **Backend:** Python 3 / Flask, served in production via Gunicorn
- **Text extraction:** pypdf (PDF), python-docx (DOCX, including tables)
- **AI analysis:** Google Gemini API
- **Frontend:** Plain HTML/CSS/JavaScript, no framework
- **Backend hosting:** Render (free tier)
- **Frontend hosting:** Vercel (free tier)

## Setup

### Prerequisites
- Python 3
- A Gemini API key from [Google AI Studio](https://aistudio.google.com)

### Installation

1. Clone the repo:
   ```
   git clone https://github.com/randeshd/HeyPDPA.git
   cd HeyPDPA
   ```

2. Create and activate a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r backend/requirements.txt
   ```

4. Set up your API key:
   - Copy `backend/.env.example` to `backend/.env`
   - Add your actual Gemini API key inside

### Running locally

1. Start the backend:
   ```
   cd backend
   python3 app.py
   ```
   Runs on `http://127.0.0.1:5001`

2. Open `frontend/index.html` (recommended: VS Code's Live Server extension)

## Deployment

The app is deployed on free-tier hosting, both tracking the `main` branch:

| Component | Platform | URL |
|---|---|---|
| Backend | Render | https://pdpa-checker.onrender.com |
| Frontend | Vercel | https://hey-pdpa.vercel.app |

The backend runs via `gunicorn app:app --timeout 120` in production (a longer timeout than Gunicorn's default, since AI analysis requests can take a while). The Gemini API key is set as an environment variable directly in Render's dashboard, never committed to the repo.

Note: Render's free tier spins the backend down after ~15 minutes of inactivity, so the first request after idle can take 30–60 seconds while it wakes back up.

## Roadmap

- Supabase (Postgres) integration for persisting past analysis results
- Supabase Auth — email/password login, followed by Google OAuth

## Status

Live and functional end-to-end. Actively developed.
