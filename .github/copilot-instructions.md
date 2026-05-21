# Copilot Instructions for LinkPeek

## Project Context
LinkPeek is a full-stack app that transforms social links (Facebook, Instagram, TikTok) into clean previews.

## Preferred Stack
- Backend: FastAPI + async HTTP client (`httpx`)
- Frontend: React + Vite
- Styling: Tailwind CSS

## Backend Expectations
- Keep endpoint surface small and clear.
- Use a normalized preview schema.
- Implement scraper-per-platform pattern.
- Add robust error mapping:
  - 400 for invalid URL/platform
  - 422 for validation issues
  - 502/503 for upstream fetch failures
- Configure CORS for local dev and env-driven production.

## Frontend Expectations
- Single URL input UX.
- Async state model: `idle`, `loading`, `success`, `error`.
- API integration isolated in `src/api/preview.js`.
- Render only non-empty preview fields.
- Never trust raw HTML from unknown sources without sanitization strategy.

## Code Style
- Keep functions short and focused.
- Prefer explicit names over abbreviations.
- Avoid broad refactors unless requested.
- Add tests for parser/normalization logic when adding new platforms.

## Security & Reliability
- Enforce request timeouts.
- Set browser-like headers to reduce scraper blocks.
- Do not log secrets.
- Validate URLs server-side even if frontend validates.
