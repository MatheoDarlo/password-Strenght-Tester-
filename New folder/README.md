# Password Strength Tester

A simple full-stack app to evaluate password strength and suggest strong passphrases. Backend: Flask (Python). Frontend: vanilla HTML/CSS/JS.

## Features
- Score passwords with multiple signals (length, character variety, dictionary/sequence checks, breach heuristics).
- Suggest strong passphrases with separators, digits, and symbols.
- REST API: POST /api/evaluate, GET /api/suggest, GET /api/health.
- CORS enabled for local frontend development.

## Project Structure
- app.py — Flask entrypoint and API wiring.
- backend/ — password evaluation logic (checker.py), helpers (utils.py), config data (config.py), routes (routes.py).
- index.html, script.js, style.css — simple frontend to call the API.

## Requirements
- Python 3.10+ recommended.
- Install: pip install flask flask-cors

## Run Backend
```
python app.py
```
The API listens on http://localhost:5000.

## Run Frontend
Open index.html in a browser (or serve via a simple static server). The frontend expects the backend at http://localhost:5000.

## API
- POST /api/evaluate — body: { "password": "..." }, returns strength, tips, and indicators.
- GET /api/suggest — returns { "suggestion": "passphrase" }.
- GET /api/health — returns { "status": "ok" }.

## Notes
- Do not reuse weak or breached passwords.
- For production, run Flask behind a real server (gunicorn/uwsgi) and disable debug.
