# PRD: LinkPeek

## 1. Product overview

### 1.1 Document title and version
- PRD: LinkPeek
- Version: 1.0

### 1.2 Product summary
LinkPeek is a web application that transforms Facebook, Instagram, and TikTok URLs into clean, distraction-free preview cards. Users paste a social media URL and receive a normalized preview containing title, description, media, and author details without navigating the source site.

## 2. Goals

### 2.1 Business goals
- Enable a lightweight preview experience for social links.
- Reduce content noise by exposing only key metadata and media.
- Support fast iteration with a simple backend/frontend architecture.
- Establish a maintainable integration pattern for social scrapers.

### 2.2 User goals
- Quickly preview Facebook, Instagram, or TikTok links.
- Understand the content without visiting the full social platform.
- See clean media embeds and metadata in a distraction-free UI.
- Receive clear error feedback when a URL is invalid or unsupported.

### 2.3 Non-goals
- Not a social media feed or content aggregator.
- No user accounts, history, favorites, or personalization.
- No database persistence for previews.
- No support for Twitter/X, YouTube, or other platforms in the initial version.

## 3. User personas

### 3.1 Key user types
- Product reviewers needing quick link previews.
- Developers or content editors verifying shared social links.
- Users wanting safe, fast previews without site noise.

### 3.2 Basic persona details
- **Link reviewer**: Wants to inspect a social post before sharing or citing it.
- **Content editor**: Needs metadata and media details quickly for workflow checks.
- **Casual browser**: Wants to preview a social link without following redirects.

### 3.3 Role-based access
- **Anonymous user**: Full access to paste URLs and view previews.
- **System**: Backend service that validates, scrapes, and normalizes preview data.

## 4. Functional requirements

- **URL entry and validation** (Priority: High)
  - Accept a single URL input from the user.
  - Validate that the URL is syntactically correct.
  - Validate that the URL belongs to Facebook, Instagram, or TikTok.
  - Return a clear error for unsupported platforms.

- **Preview API** (Priority: High)
  - Expose `GET /api/preview?url=<encodedUrl>`.
  - Return a normalized JSON response with fields:
    - `url`, `platform`, `title`, `description`, `image`, `author`, `author_url`, `embed_html`, `video_url`, `thumbnail_url`.
  - Preserve response keys with `null` for missing values.

- **Backend scraper architecture** (Priority: High)
  - Use FastAPI for asynchronous request handling.
  - Implement a scraper-per-platform pattern:
    - Facebook: OG tag parsing.
    - Instagram: OG tag parsing / metadata scraping.
    - TikTok: official oEmbed endpoint.
  - Use browser-like request headers and request timeouts.
  - Map upstream fetch failures to safe HTTP errors.

- **Frontend experience** (Priority: High)
  - Build with React + Vite.
  - Use Tailwind CSS for styling.
  - Maintain an async state model: `idle`, `loading`, `success`, `error`.
  - Render only non-empty preview fields and media.
  - Avoid rendering untrusted raw HTML directly; sanitize or use safe embed containers.

- **CORS and integration** (Priority: High)
  - Allow local dev origins: `http://localhost:5173`, `http://localhost:4173`.
  - Support env-driven production origins via `CORS_ORIGINS`.
  - Use a Vite dev proxy for `/api` to avoid CORS problems in development.

- **Error handling** (Priority: Medium)
  - Return HTTP 400 for invalid or unsupported URLs.
  - Return HTTP 422 for validation issues.
  - Return HTTP 502/503 for upstream fetch failures.
  - Display user-friendly error messages on the frontend.

## 5. User experience

### 5.1 Entry points & first-time user flow
- The landing view presents a single URL input and submit action.
- The user pastes a social link and clicks a preview button.
- The system validates the URL before sending it to the backend.

### 5.2 Core experience
- **Enter URL**: user pastes a Facebook, Instagram, or TikTok link.
- **Fetch preview**: frontend sends request to `/api/preview`.
- **Show loading**: display a spinner while the preview loads.
- **Render preview**: show title, description, author, image, and embedded media.
- **Handle errors**: show a clean error card for invalid URLs or scrape failures.

### 5.3 Advanced features & edge cases
- If the preview has no image, show only text metadata.
- If author or description is missing, omit those fields.
- If TikTok returns embed HTML, render it safely in a media container.
- If a platform blocks scraping, return a graceful failure message.

### 5.4 UI/UX highlights
- Minimal chrome and strong focus on preview content.
- Clear status states: idle, loading, success, error.
- Compact card layout for metadata and media.
- Responsive design for both desktop and mobile.

## 6. Narrative
A user pastes a Facebook, Instagram, or TikTok URL and instantly receives a concise preview. LinkPeek removes page clutter by normalizing headers, descriptions, media, and author details into a single clean card, enabling quick decision-making without visiting the source page.

## 7. Success metrics

### 7.1 User-centric metrics
- 90% of supported URLs return a preview successfully.
- 100% of visible previews omit empty fields.
- Error messages are shown for unsupported or invalid URLs.

### 7.2 Business metrics
- Decrease time to understand shared social links.
- Provide a reliable link review tool for content editors.
- Keep architecture simple for fast iteration.

### 7.3 Technical metrics
- API requests complete under 5 seconds for valid URLs.
- No synchronous blocking I/O in request processing.
- Backend scrapers use a single normalized response schema.
- Frontend build passes without errors.

## 8. Technical considerations

### 8.1 Integration points
- React frontend calls `GET /api/preview?url=...`.
- Backend scrapers fetch remote page metadata via `httpx`.
- FastAPI handles validation, CORS, and error mapping.
- Vite proxy rewrites `/api` to backend during local development.

### 8.2 Data storage & privacy
- No persistent storage is required for MVP.
- No user data or history is stored.
- URL preview requests are transient and returned immediately.

### 8.3 Scalability & performance
- Use async HTTP clients for remote fetches.
- Configure request timeout to avoid slow upstream hangs.
- Keep response payloads minimal and normalized.
- Support future caching without changing the frontend contract.

### 8.4 Potential challenges
- Instagram and Facebook may block scraper requests.
- TikTok embed HTML may require safe rendering.
- Platform metadata can vary by post and may miss fields.
- CORS must be configured correctly for both dev and production.

## 9. Milestones & sequencing

### 9.1 Project estimate
- Size: Small-medium
- Estimate: 2–3 weeks for MVP, including frontend/backend integration.

### 9.2 Team size & composition
- 2 engineers: backend and frontend, or 1 full-stack engineer.
- Optional designer for higher-fidelity UI polish.

### 9.3 Suggested phases
- **Phase 1**: Backend scaffolding and scraper architecture (3 days)
  - FastAPI app, preview model, platform dispatch, CORS.
- **Phase 2**: Frontend app and API integration (3 days)
  - React + Vite, input component, preview card, state flows.
- **Phase 3**: Validation, error handling, polish (2 days)
  - URL validation, user feedback, responsive layout.

## 10. User stories

### 10.1 Preview a supported social link
- **ID**: GH-001
- **Description**: As a user, I want to paste a Facebook, Instagram, or TikTok URL and see a clean preview so I can understand the content quickly.
- **Acceptance criteria**:
  - The app accepts a URL and displays a preview card.
  - The preview card includes title, description, media, and author when available.
  - The backend returns normalized preview JSON for supported platforms.

### 10.2 Validate unsupported link
- **ID**: GH-002
- **Description**: As a user, I want to receive a clear message when I paste an unsupported URL so I do not wait for a failed fetch.
- **Acceptance criteria**:
  - The app rejects URLs outside Facebook, Instagram, and TikTok.
  - The backend returns HTTP 400 with a descriptive message.
  - The frontend displays the error state clearly.

### 10.3 Handle invalid or malformed URLs
- **ID**: GH-003
- **Description**: As a user, I want the app to detect malformed URLs and show an error without sending bad requests.
- **Acceptance criteria**:
  - The frontend prevents invalid URL submission.
  - The backend validates the URL format and returns HTTP 422 if invalid.
  - The error message helps the user correct the URL.

### 10.4 Render only available preview content
- **ID**: GH-004
- **Description**: As a user, I want the preview card to omit missing fields so the view stays clean.
- **Acceptance criteria**:
  - Fields with `null` or empty values are not rendered.
  - The preview card adjusts layout for text-only responses.

### 10.5 Maintain a secure async scraper flow
- **ID**: GH-005
- **Description**: As a developer, I want the backend to fetch remote metadata asynchronously and safely so the service remains responsive.
- **Acceptance criteria**:
  - The backend uses `httpx.AsyncClient`.
  - Requests include browser-like headers and timeouts.
  - Scraper failures map to safe error codes and messages.

### 10.6 Support local dev integration with CORS
- **ID**: GH-006
- **Description**: As a developer, I want the app to work locally with a Vite proxy and CORS policy so frontend/backend integration is easy.
- **Acceptance criteria**:
  - FastAPI allows local dev origins.
  - Vite config proxies `/api` to the backend.
  - Local dev requests do not fail due to CORS.
