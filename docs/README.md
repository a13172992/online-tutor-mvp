# Online Tutor MVP (Docs)

This document provides quick-start instructions and development notes for the MVP version of Online Tutor.

Overview
- Backend: FastAPI with SQLite persistence for MVP.
- Frontend: Static HTML page for demonstration.
- Branching: main for stable, dev for ongoing development (new features, experiments).

Getting Started
- Prereqs: Python 3.11+, Git
- Local run:
  1) Install dependencies: see backend/requirements.txt
  2) Run backend: uvicorn backend.main:app --reload --port 8000 --host 0.0.0.0
- Remote repository: Push to GitHub using the dev/main branches as described in the previous steps.

Branch Strategy
- main: Stable MVP baseline
- dev: Active development; features merged here before landing on main

Next Steps (Suggested)
- Add user authentication layer
- Expand daily practice and question bank
- Integrate with NLP/LLM services for sentence analysis and essay scoring
- Improve frontend UX with a SPA framework
