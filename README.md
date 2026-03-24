# Movie Recommendation System

A movie recommendation web app that combines:

- **Content-based recommendations** using a local TF-IDF model
- **Live TMDB data** for posters, metadata, cast, and discovery

## Live Website

https://movie-recommendation-system-1-75kq.onrender.com/

## Tech Stack

- Python
- FastAPI (backend API)
- Streamlit (frontend UI)
- Scikit-learn (TF-IDF similarity)
- Pandas / NumPy / SciPy
- TMDB API

## Project Structure

- `main.py` - FastAPI backend (recommendations + TMDB integration)
- `app.py` - Streamlit frontend
- `model.ipynb` - notebook used for model/data preparation
- `df.pkl`, `indices.pkl`, `tfidf.pkl`, `tfidf_matrix.pkl` - model artifacts
- `requirements.txt` - Python dependencies

## Features

- Search movies via TMDB
- View rich movie details (overview, genres, cast, trailer info)
- Get TF-IDF based similar movie recommendations
- Get genre-based recommendation cards
- Browse home categories (popular, top rated, upcoming, etc.)

## Setup (Local)

### 1) Clone and enter the project

```bash
git clone <your-repo-url>
cd movie_recommendation_system
```

### 2) Create virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3) Configure environment variables

Create a `.env` file in the project root:

```env
TMDB_API_KEY=your_tmdb_api_key_here
```

Optional frontend setting:

```env
API_BASE_URL=http://127.0.0.1:8000
```

## Run the Project

### Start backend (FastAPI)

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Start frontend (Streamlit)

In another terminal:

```bash
streamlit run app.py
```

Then open the Streamlit URL shown in terminal (usually `http://localhost:8501`).

## API Endpoints (Main)

- `GET /health` - service health check
- `GET /home?category=popular&limit=24` - home feed cards
- `GET /tmdb/search?query=<movie>` - TMDB keyword search
- `GET /movie/id/{tmdb_id}` - detailed movie info
- `GET /recommend/genre?tmdb_id=<id>&limit=18` - genre-based recommendations
- `GET /actor/{actor_id}/movies?limit=24` - movies by actor
- `GET /recommend/tfidf?title=<title>&top_n=10` - TF-IDF recommendations
- `GET /movie/search?query=<movie>` - bundled details + recommendations

## Notes

- Ensure model pickle files are present in the project root.
- If `TMDB_API_KEY` is missing, TMDB-backed endpoints will fail.
- CORS is currently open in development for easy local integration.

## Deployment

Deployed on Render:

https://movie-recommendation-system-1-75kq.onrender.com/
