# AGENTS.md

## Mission
Build and maintain LinkPeek: a full-stack app that extracts clean previews (text + media) from Facebook, Instagram, and TikTok URLs.

## Product Goals
- Fast async preview retrieval
- Clean, distraction-free content rendering
- Predictable API contract between frontend and backend
- Safe defaults: validation, clear errors, CORS configured

## Architecture
- Backend: FastAPI (async), platform scrapers, normalized response model
- Frontend: React + Vite, single input flow, preview card rendering
- Transport: JSON API over `/api/preview?url=...`

## Canonical Response Shape
```json
{
  "url": "https://...",
  "platform": "facebook|instagram|tiktok",
  "title": "...",
  "description": "...",
  "image": "https://...",
  "author": "...",
  "author_url": "https://...",
  "embed_html": "<blockquote...>",
  "video_url": "https://...",
  "thumbnail_url": "https://..."
}
```

## Engineering Rules
- Keep backend handlers async end-to-end.
- Add strict URL/platform validation before scraping.
- Use timeouts and browser-like headers in remote requests.
- Fail with user-safe error messages; do not leak internals.
- Preserve response keys; missing fields should be `null`.

## CORS + Frontend Integration
- Allow local dev origins: `http://localhost:5173`, `http://localhost:4173`.
- In production, set allowed origins from env (`CORS_ORIGINS`).
- Prefer Vite proxy in dev for stable API calls.

## Definition of Done
- URL can be submitted from frontend and returns normalized preview data.
- Unsupported/invalid URLs show clean error state.
- TikTok uses oEmbed path.
- Facebook/Instagram parse OG metadata when available.
- No blocking sync I/O in request path.
