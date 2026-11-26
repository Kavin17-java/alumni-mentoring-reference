# Alumni Network and Career Mentoring System

A beginner-friendly Flask and SQLite classroom reference for Project 5 in Exercises 9 and 10. It implements consent-based alumni profiles, searchable directory, transparent mentor suggestions, mentoring requests and status changes, and participation reports with CSV export.

This is a fictional-data learning demo. The role selector is not authentication and does not protect actions. Do not add real student or alumni data or use this as a production service. The official assignment PDF and project plan were available during preparation. The Semester I curriculum PDF was not present in the repository, so the exact syllabus-unit mapping remains provisional.

## Run locally

Python 3.10 or newer is recommended.

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python app.py

On Windows, activate with .venv\Scripts\activate. Open http://127.0.0.1:5000. Startup initializes data/alumni.db and inserts fictional sample data once. Set DATABASE_PATH to a writable file path to use another database. Set SECRET_KEY to a random private value outside source control for a hosted demo.

## Tests

    pytest

Tests use a temporary database. GitHub Actions runs pytest on pushes and pull requests.

## Render setup

Build command: pip install -r requirements.txt. Start command: gunicorn app:app. Configure SECRET_KEY as an environment variable and optionally DATABASE_PATH to a writable path. Initialization and fictional sample loading run when the app starts.

SQLite is a single local file. On hosted services, local files may be lost when an instance is replaced or redeployed unless a supported persistent disk is configured; multiple service instances also cannot safely share a local SQLite file. This app is a teaching demo, not a persistent hosted system. The default local fallback is data/alumni.db.

## Team collaboration

Create a shared GitHub repository and invite both teammates. Everyone clones it, creates a feature branch, commits small changes, pushes the branch and opens a pull request. Review and test before merging to main. Resolve conflicts by pulling the latest main and editing the conflicting lines with the team. Configure a main-branch rule requiring a pull request and the pytest status check. Suggested review cycle: A reviews B, B reviews C, C reviews A. No collaboration history is represented by this reference code.

Suggested branches: feature/alumni-profiles, feature/consent, feature/search-filters, feature/mentor-matching, feature/request-status, feature/participation-report.

See docs/DEMO.md for a guided live walkthrough. See docs/TEAM_WORK_PLAN.md, docs/LEARNING_BLUEPRINT.md, docs/CODE_WALKTHROUGH.md, docs/SYLLABUS_MAPPING.md, docs/VIVA_GUIDE.md, and docs/PROMPT_LOG.md.
