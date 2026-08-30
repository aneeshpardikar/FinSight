# StockBot

A stock portfolio tracking application with a FastAPI backend and a Next.js frontend.

## Project Structure

```
stockbot/
├── app/                    # Next.js frontend
├── app.py                  # FastAPI app entry point
├── auth.py                 # Authentication logic
├── database.py             # Database connection/session setup
├── main.py                 # Core API routes (portfolio, etc.)
├── models.py                # SQLAlchemy models
├── schemas.py               # Pydantic schemas
├── test_stock.py            # Tests
├── requirements.txt         # Python dependencies
├── package.json              # Frontend dependencies
├── .env.local.example        # Example frontend environment variables
└── .gitignore
```

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy
- **Frontend:** Next.js
- **Database:** SQLite (local development)

## Getting Started

### Backend Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the backend server:
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`.

### Frontend Setup

1. Install dependencies:
   ```bash
   cd app
   npm install
   ```

2. Copy the example environment file and update as needed:
   ```bash
   cp .env.local.example .env.local
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:3000`.

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | Base URL of the backend API | `http://127.0.0.1:8000` |

## Deployment Notes

- The frontend (Next.js) can be deployed directly to [Vercel](https://vercel.com).
- The backend (FastAPI) requires a host that supports persistent Python servers, such as [Render](https://render.com) or [Railway](https://railway.app), since it is not natively serverless.
- SQLite is used for local development only. For production, migrate to a hosted database (e.g., Postgres via Neon or Supabase) since serverless/ephemeral filesystems will not persist a local `.db` file.
- Set `NEXT_PUBLIC_API_URL` in your frontend hosting provider's environment variable settings to point to your deployed backend URL.

## License

Add your license here.
