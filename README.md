# LinkPeek

LinkPeek is a design-driven project for a lightweight preview service that converts Facebook, Instagram, and TikTok URLs into clean, distraction-free preview cards.

## Project overview

- **Goal**: Provide a normalized preview JSON response for supported social links.
- **Platforms**: Facebook, Instagram, TikTok.
- **Architecture**: FastAPI-style async backend, React + Vite frontend, Tailwind CSS styling.
- **Current repo state**: Documentation and architecture notes are present; source implementation files are not yet included.

## Intended architecture

- `GET /api/preview?url=<encodedUrl>`
- Normalize responses to:
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
- Validate URLs before scraping.
- Use async HTTP requests with browser-like headers and timeouts.
- Map failures to safe HTTP errors.
- Render only non-empty fields in the frontend.

## Development expectations

- FastAPI backend with async endpoint handling.
- Platform-specific scraper modules.
- React + Vite frontend with a single URL input flow.
- Tailwind CSS for UI styling.
- CORS configured for local dev origins and env-driven production origins.

## How to use this repo

1. Review `AGENTS.md` for architecture and API contract guidance.
2. Review `prd.md` for product goals, user stories, and success metrics.
3. Add backend implementation under `backend/`.
4. Add frontend implementation in a new `frontend/` or `app/` directory.

## Notes

- This repo is currently documentation-focused and is ready for implementation.
- The backend scaffold directories exist to support future code organization.
- No runtime code is present in the current commit.
