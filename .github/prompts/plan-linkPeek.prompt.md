## Plan: LinkPeek Full-Stack App

**TL;DR** — FastAPI backend scrapes OG tags + TikTok oEmbed, React/Vite frontend renders clean previews. CORS handled via FastAPI middleware + Vite dev proxy.

---

### Phase 1 — Backend

| Step | File | What |
|---|---|---|
| 1 | `backend/requirements.txt` | fastapi, uvicorn, httpx, bs4, lxml, pydantic, python-dotenv |
| 2 | `backend/models/preview.py` | Pydantic `PreviewResponse` model |
| 3 | `backend/scrapers/base.py` | `BaseScraper` ABC — browser headers, `_get_html()`, `_get_json()`, `_og()` helper |
| 4 | `backend/scrapers/facebook.py` | OG tag scraper → title, description, image, author |
| 5 | `backend/scrapers/instagram.py` | OG tag scraper → title, description, thumbnail |
| 6 | `backend/scrapers/tiktok.py` | `https://www.tiktok.com/oembed?url=…` (no auth, official) |
| 7 | `backend/scrapers/router.py` | `detect_platform(url)` → dispatch to correct scraper |
| 8 | `backend/main.py` | FastAPI app, `CORSMiddleware`, `GET /api/preview?url=…` |

### Phase 2 — Frontend

| Step | File | What |
|---|---|---|
| 9 | `frontend/package.json` | react, vite, tailwind, postcss, autoprefixer |
| 10 | `frontend/vite.config.js` | proxy `/api` → `http://localhost:8000` |
| 11 | `frontend/tailwind.config.js` + `postcss.config.js` | Tailwind setup |
| 12 | `frontend/src/api/preview.js` | `fetchPreview(url)` async fetch helper |
| 13 | `frontend/src/components/URLInput.jsx` | Controlled input + submit button |
| 14 | `frontend/src/components/PreviewCard.jsx` | Renders title, description, image, author, embed HTML |
| 15 | `frontend/src/App.jsx` | State machine: `idle → loading → success/error` |
| 16 | `frontend/src/main.jsx` + `index.html` | Entry point |

### Phase 3 — Wiring & Validation

- CORS: FastAPI allows `localhost:5173` (Vite dev) + `localhost:4173` (preview)
- Vite proxy eliminates CORS issues in dev entirely
- Input validation: URL must match `facebook.com | instagram.com | tiktok.com`
- Error states: invalid URL, unsupported platform, scrape failure → user-friendly messages

---

**Relevant files**
- `backend/scrapers/` — empty dirs already exist, ready to populate
- `backend/models/` — empty dir already exists

**Scope exclusions**
- No auth, no DB, no caching, no Twitter/X/YouTube

**Further Considerations**
1. **Production CORS** — Vite proxy only works in dev. For prod, need `CORS_ORIGINS` env var. I'll add `.env.example` + `python-dotenv` to handle this cleanly.
2. **Instagram scraping** — Meta increasingly blocks scrapers. OG tags work for public posts but may need a fallback. Want a graceful degradation message rather than an error?

---

Ready to implement? I'll build Phase 1 (backend) first, then Phase 2 (frontend), then wire everything together.
