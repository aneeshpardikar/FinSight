# FinSight

A personal expense tracking application with a FastAPI backend and a Next.js frontend.

**Live demo:** [https://finsight-pi-drab.vercel.app/](https://finsight-pi-drab.vercel.app/)

## Project Structure

```graphql
finsight/
├── app/                    # Next.js frontend and API proxy routes
├── app.py                  # Legacy Streamlit frontend entry point
├── auth.py                 # Authentication helper
├── database.py             # Database connection/session setup
├── main.py                 # Core FastAPI routes and authentication
├── models.py               # SQLAlchemy models
├── schemas.py              # Pydantic schemas
├── test_stock.py           # Legacy stock test
├── requirements.txt        # Python dependencies
├── package.json            # Frontend dependencies
├── .env.local.example      # Example frontend environment variables
└── README.md
```

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, bcrypt, JWT
- **Frontend:** Next.js, React
- **Database:** SQLite (local development)
- **AI:** Groq

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

3. Create a `.env` file:

   ```env
   GROQ_API_KEY=your-groq-api-key
   SECRET_KEY=your-long-random-secret
   ```

4. Run the backend server:

   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at `http://127.0.0.1:8000`.

### Frontend Setup

1. Install dependencies from the project root:

   ```bash
   npm install
   ```

2. Run the development server:

   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`.

## Environment Variables

| Variable | Description | Example |
| --- | --- | --- |
| `GROQ_API_KEY` | Groq API key used for AI Insights | `gsk_...` |
| `SECRET_KEY` | Secret used to sign JWT login tokens | Long random string |
| `NEXT_PUBLIC_API_URL` | Optional backend API URL override | `http://127.0.0.1:8000` |

## Features

- User registration and secure login
- Personal expense records and categories
- Monthly budgets and spending analytics
- Transaction filters and deletion
- AI financial insights
- Purchase affordability calculator

## Deployment Notes

- The frontend is deployed on [Vercel](https://vercel.com): [FinSight live demo](https://finsight-pi-drab.vercel.app/).
- The FastAPI backend requires a Python-compatible host such as [Render](https://render.com) or [Railway](https://railway.app).
- SQLite is suitable for local development. Use a hosted database such as Postgres for production because serverless filesystems are not persistent.
- Configure the deployed frontend with the URL of the hosted FastAPI backend.

