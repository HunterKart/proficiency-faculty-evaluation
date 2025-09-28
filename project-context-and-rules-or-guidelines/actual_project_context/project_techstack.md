# Project Tech Stack (Final, Minimal)

This is the complete, **no-overengineering** stack required to deliver the system end-to-end as specified (roles, dynamic forms, sentiment & keywords, suggestions for faculty/heads, CSV/Excel onboarding, exports, notifications, dashboards, and flags).

---

## Frontend

-   **React + TypeScript** — Core UI framework with type safety.
-   **Vite** — Fast dev server and build tool.
-   **Tailwind CSS** — Utility-first styling for consistent, rapid UI work.
-   **shadcn/ui (Radix UI + Tailwind primitives)** — Accessible component library scaffolding for consistent layouts and form controls.
-   **React Router** — Client-side routing for role-based areas (Student, Faculty, Dept Head, Admin, Super Admin).
-   **React Hook Form + Zod** — Forms + schema validation (Likert ranges, 5–300 word limits, time checks on submit).
-   **TanStack Query** — Data fetching, caching, and **polling** for notifications & dashboard refresh.
-   **Echarts** — Bar/line charts for analytics.
-   **echarts echarts-wordcloud** — Render keyword clouds from KeyBERT outputs.

## Backend

-   **Python**, **FastAPI**, **Uvicorn** — REST API (keep endpoints synchronous by default).
-   **Pydantic v2** (+ `pydantic-settings`) — Request/response models & environment-based config.
-   **Auth (JWT)** — Access/refresh tokens; **bcrypt** password hashing; **TOTP (pyotp)** for Super Admin MFA.
-   **Validation (server-side)** — Enforce dynamic Likert ranges, **5–300** words, **~45s** min time-on-form, and rating–sentiment mismatch flags.
-   **CSV/Excel** — `pandas` + `openpyxl` for onboarding & bulk operations.
-   **PDF exports** — **WeasyPrint** (HTML → PDF) for reports and AI suggestion exports.
-   **Email (SMTP)** — Send notifications/banners via a simple SMTP relay.

## Database & Data Layer

-   **MySQL/MariaDB** — Primary relational database.
-   **SQLAlchemy 2.0 (sync) + Alembic** — ORM & migrations.
-   **Driver** — `PyMySQL`.

## Background Jobs

-   **RQ (Redis Queue) + Redis** — Single worker process for:
    -   Batch **sentiment** (XLM-R) + **keyword** (KeyBERT) processing
    -   **CSV/Excel** imports
    -   **PDF** report generation
    -   **Email** notification fan-out

## AI/ML (Local Inference Only)

-   **XLM-RoBERTa** — Sentiment classifier (fine-tuneable on your data).
-   **KeyBERT** (+ `sentence-transformers`) — Keyword extraction for dashboards/word clouds.
-   **Flan-T5 (small/base)** — Prompted “suggestions” generation (visible only to Faculty/Dept Heads).

## Deployment

-   **Single VPS (Ubuntu) + Docker Compose**, services:
    1. `api` (FastAPI)
    2. `worker` (RQ)
    3. `redis`
    4. `db` (MariaDB/MySQL)
    5. `caddy` (reverse proxy + HTTPS; also serves the frontend build)
-   **Domain & TLS** — Buy a domain (e.g., Namecheap/Porkbun); DNS → VPS; **Caddy** auto-HTTPS; done only at completion of system
-   **Backups** — Nightly DB dumps; keep off-box copies weekly.
-   **Environment** — `.env` files for DB/JWT/SMTP secrets.

## Explicit Non-Goals (to prevent overengineering)

-   **No WebSockets/Push** (use polling with TanStack Query)
-   **No GraphQL / gRPC**
-   **No microservices** (single API + single worker)
-   **No external LLM APIs** (local models only)
-   **No async SQLAlchemy/async only if necessary** (sync ORM is simpler but if absolutely necessary async ORM can be used; heavy work in worker)
-   **No global state manager** (React Query + RHF are sufficient)

---

## Crucial Nuances

### 1) Polling (what it is and how to do it)

-   The frontend periodically refetches (e.g., every **10–30s**) from endpoints like `/notifications?since=<ts>` and `/dashboard?since=<ts>`.
-   The backend returns **only deltas** (items updated after `since`). If nothing changed, return an empty list or a `count=0` summary.
-   Keep payloads small; paginate if needed.

### 2) Async Strategy (simple, effective, and fast enough)

-   **API stays synchronous** (plain `def` endpoints, sync SQLAlchemy).
-   **All heavy/slow tasks** (AI, imports, PDF) run in the **RQ worker** to avoid blocking requests.
-   If you truly need streaming later, add a small **SSE** (`text/event-stream`) endpoint for job progress; otherwise keep polling.

### 3) Validation Rules (enforced server-side **and** client-side)

-   Dynamic **Likert** scales (configurable per form).
-   Open-ended answers must be **5–300 words**.
-   Enforce minimum **~45s** time-on-form to reduce spam/low-effort responses.
-   Store and act on **rating–sentiment mismatch** flags.

### 4) Roles & Data Isolation

-   Roles: **Student, Faculty, Department Head, Admin, Super Admin**.
-   Check role/ownership on every endpoint.
-   Include a `university_id` (tenant guard) in all relevant tables and queries.

### 5) Performance & Scalability Basics

-   Add DB indexes on: `university_id`, `updated_at`, `teacher_id`, `term_id`.
-   Keep polling intervals modest (10–30s) and return only deltas.
-   Scale by adding **another RQ worker** process if batches queue up.
-   Bound dashboard queries with `LIMIT`/pagination.

### 6) Security Essentials

-   **HTTPS** everywhere (Caddy handles certs).
-   **JWT** with sensible expiries; refresh tokens stored server-side or securely.
-   **Password hashing** (bcrypt); validate emails on signup.
-   **CORS** locked to your domain(s); secrets via `.env` only.
-   Restrict admin/super-admin endpoints; log access.

### 7) Migrations & Backups

-   Apply **Alembic** migrations on deploys (API container entrypoint or manual step).
-   Nightly **DB dumps**; test restore periodically.

---

## Minimal Package List (by area)

**Frontend**

-   `react` `react-dom` `typescript` `vite` `tailwindcss` `postcss` `autoprefixer`
-   `shadcn-ui` scaffolding (`@radix-ui/*` primitives, `class-variance-authority`, `clsx`, `tailwind-merge`, `lucide-react`)
-   `react-router-dom` `@tanstack/react-query` `react-hook-form` `zod` `@hookform/resolvers`
-   `echarts echarts-wordcloud`

**Backend**

-   `fastapi` `uvicorn[standard]` `pydantic` `pydantic-settings` `python-dotenv`
-   `pyjwt` `passlib[bcrypt]` `pyotp`
-   `sqlalchemy` `alembic` `pymysql`
-   `redis` `rq` `pandas` `openpyxl` `weasyprint` `email-validator`

**AI**

-   `transformers` `torch` `keybert` `sentence-transformers`
