# Query Assistant

A restaurant query assistant with a React chat interface, a FastAPI backend, and PostgreSQL restaurant data. Ask about cafes, ratings, budgets, online ordering, and table bookings.

## Features

- Chat through REST or WebSocket connections.
- Browse restaurant results with ratings, costs, and booking information.
- Save and manage chat sessions in a local SQLite database.
- Use an optional Google ADK agent with Gemini.

The React backend uses keyword-based SQL query generation. The optional ADK agent is a separate entry point.

## Requirements

- Python 3.10 or newer (use a version supported by the pinned dependencies).
- Node.js 18 or newer and npm.
- Docker with Docker Compose.

## Run locally

From the repository root, create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r query_assistant/requirements.txt
pip install pandas
```

`pandas` is also needed by the CSV data loader.

Start PostgreSQL and import the included sample data:

```powershell
cd query_assistant
docker compose up -d postgres
python load_data.py
```

Wait until PostgreSQL is ready before running the loader. The loader replaces existing restaurant records with the contents of `Zomato-data.csv`.

Start the API from the `query_assistant` directory:

```powershell
python -m uvicorn backend:app --reload --host 127.0.0.1 --port 8000
```

In a second terminal, start the frontend from the repository root:

```powershell
cd frontend
npm install
npm run dev
```

- Chat interface: http://localhost:3000
- API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health

The Compose file and Python database connections contain matching local development credentials. Change these before deploying. Local `.env` files, generated databases, and dependencies are excluded from Git.

## Example queries

- Show me all cafes
- Find cheap restaurants
- Best rated restaurants
- Restaurants with online ordering
- Restaurants with table booking
- All buffet restaurants

## API

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/chat` | Send a message, optionally with a session ID |
| GET | `/sessions` | List saved sessions |
| GET | `/sessions/{session_id}` | Retrieve session details |
| GET | `/sessions/{session_id}/messages` | Retrieve conversation history |
| DELETE | `/sessions/{session_id}` | Delete a session |
| WebSocket | `/ws/{session_id}` | Chat over a persistent connection |
| GET | `/health` | Check API health |

## Project structure

```text
frontend/                  React, TypeScript, Vite, and Tailwind CSS
query_assistant/
  backend.py               FastAPI routes and WebSocket handling
  backend_tools.py         Restaurant query logic for the API
  session_manager.py       SQLite conversation persistence
  agent.py                 Optional Google ADK agent
  tools.py                 ADK restaurant query tool
  load_data.py             CSV-to-PostgreSQL import
  init.sql                 Restaurant database schema
  docker-compose.yml       Local database services and pgAdmin
  Zomato-data.csv           Restaurant sample data
  requirements.txt         Backend dependencies
README_REACT.md            Additional frontend notes
start_react.bat            Windows startup helper
start_simple.bat           Optional ADK startup helper
```

## Optional Google ADK interface

Install `google-adk` separately, configure its Gemini authentication in your local environment, and start the Compose services. The `start_simple.bat` helper runs `adk web` with the PostgreSQL session service on port 5433. Keep API keys in your local environment or an untracked `.env` file.

## Frontend build

```powershell
cd frontend
npm run build
```

To stop the local database services:

```powershell
cd query_assistant
docker compose down
```
