# PRD: LinkPeek

## 1. Product overview

### 1.1 Document title and version
- PRD: LinkPeek
- Version: 1.1

### 1.2 Product summary
LinkPeek is a web application that accepts many social media URLs at once, processes them through Apify, and stores normalized content in a database. Users submit a batch of URLs, and the system ingests each link, extracts metadata/media details, and persists both source URLs and extraction results for later retrieval and review.

## 2. Goals

### 2.1 Business goals
- Enable a lightweight preview experience for social links.
- Reduce content noise by exposing only key metadata and media.
- Support fast iteration with a simple backend/frontend architecture.
- Establish a maintainable integration pattern for social extraction.
- Support scalable bulk URL ingestion and processing using Apify.
- Persist ingested URLs and extracted content for auditability and reuse.

### 2.2 User goals
- Submit many Facebook, Instagram, or TikTok links in one action.
- Understand content without visiting full social platforms.
- See clean media previews and metadata in a distraction-free UI.
- Receive clear per-URL feedback when links are invalid, unsupported, or failed.

### 2.3 Non-goals
- Not a social media feed or content aggregator.
- No user accounts, history, favorites, or personalization.
- No support for Twitter/X, YouTube, or other platforms in the initial version.

## 3. User personas

### 3.1 Key user types
- Product reviewers needing fast bulk link previews.
- Developers or content editors validating many social links.
- Users wanting safe, fast previews without platform noise.

### 3.2 Basic persona details
- **Link reviewer**: inspects multiple posts before sharing or citing.
- **Content editor**: checks metadata/media quickly during content workflows.
- **Casual browser**: previews links without following redirects.

### 3.3 Role-based access
- **Anonymous user**: full access to submit URLs and view processed results.
- **System**: backend service that validates URLs, calls Apify, normalizes results, and persists records.

## 4. Functional requirements

- **Bulk URL entry and validation** (Priority: High)
  - Accept a list of URLs (multi-line input or bulk payload).
  - Validate URL syntax for each submitted item.
  - Validate platform support: Facebook, Instagram, TikTok.
  - Return clear per-URL validation errors for unsupported links.

- **Bulk ingestion and persistence** (Priority: High)
  - Store each submitted URL in the backend database.
  - Track per-URL status: `pending`, `processing`, `success`, `failed`.
  - Store timestamps and error details for failed processing.

- **Ingestion and retrieval APIs** (Priority: High)
  - Expose a bulk ingestion endpoint (e.g., `POST /api/ingest`).
  - Expose retrieval endpoints for stored URL records and extracted content.
  - Return a normalized content schema with fields:
    - `url`, `platform`, `title`, `description`, `image`, `author`, `author_url`, `embed_html`, `video_url`, `thumbnail_url`.
  - Preserve response keys with `null` for missing values.

- **Backend extraction architecture** (Priority: High)
  - Use asynchronous backend request handling.
  - Use Apify as the primary extraction provider for supported social URLs.
  - Read each stored URL, call Apify, normalize output, and store extraction results.
  - Use request timeouts and retry policy for Apify calls.
  - Map Apify/upstream failures to safe HTTP errors.

- **Frontend experience** (Priority: High)
  - Build frontend with **Next.js**.
  - Use Tailwind CSS for styling.
  - Maintain async state model: `idle`, `loading`, `success`, `error`.
  - Render only non-empty preview fields.
  - Avoid rendering untrusted raw HTML directly; sanitize or isolate in safe containers.

- **CORS and integration** (Priority: High)
  - Allow local dev origins: `http://localhost:3000` and `http://localhost:3001` for Next.js dev.
  - Support env-driven production origins via `CORS_ORIGINS`.
  - Ensure local frontend/backend integration does not fail due to CORS.

- **Error handling** (Priority: Medium)
  - Return HTTP 400 for invalid/unsupported URLs.
  - Return HTTP 422 for validation issues.
  - Return HTTP 502/503 for Apify/upstream failures.
  - Display user-friendly errors on the frontend.

## 5. User experience

### 5.1 Entry points and first-time flow
- Landing page provides bulk URL input and submit action.
- User pastes many social URLs and starts ingestion.
- System validates each URL before backend processing.

### 5.2 Core experience
- **Enter URLs**: user pastes a batch of Facebook, Instagram, or TikTok links.
- **Submit ingestion**: frontend calls ingestion API.
- **Store and process**: backend stores URLs and processes each via Apify.
- **Show progress**: UI displays per-item status and batch summary.
- **Render results**: show normalized content for successes and clear errors for failures.

### 5.3 Advanced features and edge cases
- If a record has no image, render text-only metadata.
- If author or description is missing, omit those fields in UI.
- If TikTok returns embed HTML, render in a sanitized/safe container.
- If Apify cannot extract a URL, mark record failed with a clear reason.

### 5.4 UI/UX highlights
- Minimal layout focused on content and status.
- Clear states: idle, loading, success, error.
- Compact result cards and batch-level summary.
- Responsive behavior for desktop and mobile.

## 6. Narrative
A user pastes many Facebook, Instagram, or TikTok URLs and submits them once. LinkPeek stores all submitted URLs, processes each URL through Apify, and saves normalized metadata/media in the database so users can review structured results quickly without visiting source pages.

## 7. Success metrics

### 7.1 User-centric metrics
- 90% of supported URLs in a batch are processed successfully.
- 100% of visible previews omit empty fields.
- Per-URL error messages are shown for invalid/unsupported/failed URLs.

### 7.2 Business metrics
- Reduce time to review shared social links.
- Provide reliable batch link verification for content teams.
- Keep architecture simple for rapid iteration.

### 7.3 Technical metrics
- Ingestion requests accepted and persisted under 2 seconds for medium batches.
- Processing latency per URL remains within acceptable Apify SLA bounds.
- No synchronous blocking I/O in request path.
- Backend uses one normalized response schema.
- 100% of submitted URLs persist with status history.
- Frontend build passes without errors.

## 8. Technical considerations

### 8.1 Integration points
- Next.js frontend calls bulk ingestion and retrieval APIs.
- Backend calls Apify API for extraction.
- Backend normalizes payload and persists URL + content entities.
- Backend enforces validation, CORS, and error mapping.

### 8.2 Data storage and privacy
- Persistent storage is required for submitted URLs and extracted content.
- No user account data is required for MVP.
- URL requests and extraction outcomes are stored with processing metadata.

### 8.3 Scalability and performance
- Use async HTTP clients for Apify communication.
- Configure request timeout and retry strategy.
- Keep payloads normalized and minimal.
- Support future queue/worker model for larger batches.
- Support future caching without changing frontend contract.

### 8.4 Potential challenges
- Apify actor reliability and rate limits under high volume.
- Platform metadata variability and missing fields.
- Safe rendering requirements for embed HTML.
- Correct CORS setup across local and production environments.

## 9. Milestones and sequencing

### 9.1 Project estimate
- Size: Small-medium
- Estimate: 2-3 weeks for MVP, including full integration.

### 9.2 Team size and composition
- 2 engineers (backend + frontend) or 1 full-stack engineer.
- Optional designer for UI polish.

### 9.3 Suggested phases
- **Phase 1**: Backend scaffolding and ingestion models (3 days)
  - URL/content models, ingestion endpoints, status fields, CORS.
- **Phase 2**: Apify integration and persistence pipeline (3 days)
  - Apify client, normalization mapping, retries/timeouts, failure handling.
- **Phase 3**: Next.js bulk UX and result views (2 days)
  - Bulk input UI, progress/status display, result cards, error states.

## 10. User stories

### 10.1 Ingest supported social links in bulk
- **ID**: GH-001
- **Description**: As a user, I want to submit many Facebook, Instagram, or TikTok URLs in one run so I can review content quickly.
- **Acceptance criteria**:
  - App accepts multiple URLs in one submission.
  - Backend stores each URL with processing status.
  - Backend stores normalized content for each successful URL.

### 10.2 Validate unsupported links
- **ID**: GH-002
- **Description**: As a user, I want clear feedback for unsupported URLs so I can correct input quickly.
- **Acceptance criteria**:
  - App rejects URLs outside supported platforms.
  - Backend returns descriptive 400 responses per invalid item.
  - Frontend displays clear per-item error state.

### 10.3 Handle malformed URLs
- **ID**: GH-003
- **Description**: As a user, I want malformed URLs detected early so bad requests are not processed.
- **Acceptance criteria**:
  - Frontend performs initial validation.
  - Backend validates format and returns HTTP 422 where appropriate.
  - Error messaging helps user correct the URL.

### 10.4 Render only available content
- **ID**: GH-004
- **Description**: As a user, I want missing fields omitted so results stay clean.
- **Acceptance criteria**:
  - `null` or empty fields are not rendered.
  - Card layout adapts for text-only results.

### 10.5 Secure async extraction flow
- **ID**: GH-005
- **Description**: As a developer, I want async extraction via Apify with safe error handling so the service remains responsive.
- **Acceptance criteria**:
  - Backend uses async HTTP client for Apify calls.
  - Requests use timeouts and retry strategy.
  - Extraction failures map to safe, user-facing error codes/messages.

### 10.6 Local dev integration with CORS
- **ID**: GH-006
- **Description**: As a developer, I want stable local frontend/backend integration using Next.js so development is frictionless.
- **Acceptance criteria**:
  - Backend allows local Next.js origins.
  - Local API calls do not fail due to CORS.
  - Env-based origin config supports production.

### 10.7 Persist extraction outcomes
- **ID**: GH-007
- **Description**: As a developer, I want each URL's extraction outcome stored for traceability and retry workflows.
- **Acceptance criteria**:
  - Backend stores success and failure outcomes.
  - Failure records include reason and timestamp.
  - Retrieval APIs expose current status and normalized result payload.
