# Project: Cold Email System & Dashboard App

## 1. Project Overview
This project consists of two distinct parts due to a separation of concerns:
1.  **Current State (Live):** A set of lightweight Python scripts (`send_emails.py`, `process_inbox.py`) running in the root directory to handle actual email sending and reply tracking. This is stable and currently in use.
2.  **Future Goal (To Be Built):** A modern React/Electron Desktop Application ("Cold Email Reach") that provides a beautiful UI for managing leads, campaigns, and settings. **This code exists but is currently archived.**

## 2. Directory Structure
*   **Root (`/`):** Contains the active Python scripts (`send_emails.py`, `process_inbox.py`), data files (`remaining_leads.md`, `sent_emails.log`), and `.env` config.
*   **Archive (`/_archived_app`):** Contains the FULL SOURCE CODE for the React/Electron application that was previously built but shelved due to packaging issues.
    *   `ColdEmailApp/backend`: FastAPI Python backend (Logic for full app).
    *   `ColdEmailApp/frontend`: React + Vite + Tailwind frontend.

## 3. The "Live" System (Scripts)
Currently running for the user.
*   **Data Source:** `remaining_leads.md` (Markdown table format).
*   **Sending Logic:** `send_emails.py` reads the MD file, connects to Gmail via `.env` credentials, and sends emails with a randomized delay (10-20 mins).
*   **Inbox Logic:** `process_inbox.py` scans IMAP for replies/bounces and updates the status column in `remaining_leads.md`.

## 4. The "Dashboard App" (For the Next Agent)
**Your Goal:** Revive the application found in `_archived_app`.

### Context & History
*   **What was built:** A full dashboard with "Premium" dark mode UI, widgets, lead grid, and campaign editor.
*   **Why it stopped:** The build process (`PyInstaller` + `Electron-Builder`) failed repeatedly due to environment corruption (`IndexError: tuple index out of range` in `site-packages`).
*   **The Pivot:** We decided to allow the user to run the *scripts* temporarily while we move the App development to a clean slate.

### Technical Stack (Archived App)
*   **Frontend:** React, Vite, TailwindCSS (Zinc/Violet theme), Lucide React icons.
*   **Backend:** Python FastAPI, SQLAlchemy (Async), SQLite (`app.db`).
*   **Database Schema:**
    *   `Leads`: id, name, email, company, status, source, icebreaker.
    *   `Settings`: smtp_user, smtp_password, daily_limit.
    *   `Campaigns`: template_body, subject, schedule.

### Instructions for the Next Agent
1.  **Copy the Source:** Take the contents of `_archived_app/ColdEmailApp` to a *new* clean folder/workspace to rely on a fresh Python environment.
2.  **Restore the UI:** The frontend code is complete and beautiful. Use `npm install` and `npm run dev` to see it.
3.  **Connect the Backend:** The `main.py` in the backend is ready. It needs to be run (`uvicorn main:app`).
4.  **Fix the Build:** The main challenge is packaging.
    *   *Option A:* Try `PyInstaller` again in your fresh environment.
    *   *Option B:* Use the "Source Deployment" strategy we started (packaging python source files and running them with a bundled python runtime or the user's system python).

**Good luck! The UI is ready, it just needs a stable home and build pipeline.**
