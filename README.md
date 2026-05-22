# LinkPeek

LinkPeek converts Facebook, Instagram, and TikTok URLs into clean preview cards.

## Project architecture

- Backend: Django + Django REST framework
- Frontend: Next.js + TypeScript + Tailwind CSS
- Preview endpoint: `GET /api/preview?url=<encodedUrl>`
- Normalized response fields:
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

## Project layout

- `backend/` — Django project and preview API implementation
- `frontend/` — Next.js application with the preview UI

## Running locally

1. Install backend dependencies:
   - `python -m venv .venv`
   - `source .venv/bin/activate`
   - `pip install -r backend/requirements.txt`

2. Run the Django backend:
   - `cd backend`
   - `python manage.py migrate`
   - `python manage.py runserver`

3. Install frontend dependencies:
   - `cd frontend`
   - `npm install`
   - `npm run dev`

4. Open the Next.js app at `http://localhost:3000`.

## Notes

- The frontend uses a Next.js rewrite so `/api/preview` forwards to the Django backend in development.
- The backend validates and scrapes supported Facebook, Instagram, and TikTok URLs.
- Environment config for Django is available in `backend/.env.example`.
- GitHub Actions CI, Dependabot, and CodeQL scans are configured under `.github/`.
