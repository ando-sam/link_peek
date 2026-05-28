# LinkPeek

LinkPeek ingests batches of Facebook, Instagram, and TikTok URLs, processes each URL through Apify, and stores normalized extraction results in the backend database.

## Project architecture

- Backend: Django + Django REST framework
- Frontend: Next.js + TypeScript + Tailwind CSS
- Extraction provider: Apify
- Primary workflow:
  - User submits many social URLs in one request.
  - Backend stores each URL record with status.
  - Backend processes each stored URL through Apify.
  - Backend stores normalized extraction output (or failure reason).

## API overview

- Ingestion endpoint: `POST /api/ingest`
- Retrieval endpoints: read stored URL records and extracted content
- Per-URL processing status values:
  - `pending`
  - `processing`
  - `success`
  - `failed`

Batch request body example:

```json
{
  "urls": [
    "https://www.instagram.com/p/abc123/",
    "https://www.tiktok.com/@demo/video/123456"
  ]
}
```

Normalized content fields:

- `url`
- `platform`
- `title`
- `description`
- `image`
- `author`
- `author_url`
- `embed_html`
- `video_url`
- `thumbnail_url`

Missing values must be returned as `null`.

## Project layout

- `backend/`: Django project, ingestion APIs, persistence models, Apify integration
- `frontend/`: Next.js app for bulk URL input, progress, and result views

## Running locally

1. Install backend dependencies:
   - `python -m venv .venv`
   - `source .venv/bin/activate`
   - `pip install -r requirements.txt`

2. Configure backend environment:
   - Create `backend/.env` from `backend/.env.example` if available
   - Set Apify credentials (for example `APIFY_TOKEN`)
   - Set `CORS_ORIGINS` for local Next.js origins if needed

3. Run database migrations and backend:
   - `cd backend`
   - `python manage.py migrate`
   - `python manage.py runserver`

4. Install and run frontend:
   - `cd frontend`
   - `npm install`
   - `npm run dev`

5. Open frontend:
   - `http://localhost:3000`

## Behavior notes

- Backend validates each URL before processing.
- Unsupported or invalid URLs return clear user-safe errors.
- Apify/upstream failures are mapped to safe server errors.
- Frontend renders only non-empty fields from normalized output.
- Raw embed HTML must be rendered only in safe/sanitized containers.
