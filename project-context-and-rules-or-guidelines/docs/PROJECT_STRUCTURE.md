# Project Structure Guide

## Overview

This monorepo keeps the faculty evaluation platform cohesive while leaving clear seams between the FastAPI backend, the React frontend, and cross-service automation. Each top-level area mirrors a deployment unit from the documented stack in [`actual_project_context/project_techstack.md`](../actual_project_context/project_techstack.md). The backend directory focuses on synchronous API endpoints backed by SQLAlchemy models and Redis-backed RQ workers for longer jobs. The frontend directory houses a Vite-powered React TypeScript application that renders dashboards, dynamic forms, and notification flows. A dedicated `tests` arena supports cross-cutting checks such as Selenium-powered end-to-end journeys that exercise both services together. Shared documentation, operational notes, and progress tracking live under `project-context-and-rules-or-guidelines` and `project-progress` so that every contributor can quickly find constraints, conventions, and pending follow-up work.

Keeping code in the prescribed folders matters because the stack balances synchronous HTTP handlers with background processing for AI workloads, PDF export, and CSV imports. The layout also anticipates infrastructure elements like Alembic migrations, reusable scripts, and Selenium fixtures. Grouping responsibilities this way ensures that new files land beside similar examples, dependency graphs remain manageable, and future agents can map a story to the right module without rereading the entire repository.

## Backend layout

The backend lives in [`../../backend/`](../../backend/). The heart of the service is [`backend/app/`](../../backend/app/), which mirrors FastAPI patterns and keeps imports clean. Use [`backend/app/api/routers/`](../../backend/app/api/routers/) for route modules that register path operations on the application instance. Centralize environment configuration, security helpers (JWT utilities, password hashing, TOTP verification), and shared dependencies inside [`backend/app/core/`](../../backend/app/core/). Database orchestration belongs in [`backend/app/db/`](../../backend/app/db/), including the SQLAlchemy engine, session factories, base metadata declarations, and any seed helpers that bootstrap reference data per tenant.

Domain entities defined with SQLAlchemy go under [`backend/app/models/`](../../backend/app/models/), while Pydantic request and response schemas live in [`backend/app/schemas/`](../../backend/app/schemas/). Encapsulate reusable business logic, such as CSV import flows, notification fan-out, or analytics aggregations, within [`backend/app/services/`](../../backend/app/services/). Dedicated worker tasks should be stored in [`backend/app/workers/`](../../backend/app/workers/) so that RQ job definitions remain isolated from request handlers. Local inference wrappers for XLM-R sentiment analysis, KeyBERT keyword extraction, or Flan-T5 suggestion generation belong in [`backend/app/ml/`](../../backend/app/ml/). Use [`backend/app/utils/`](../../backend/app/utils/) for lightweight helpers (formatting, parsing, word-count checks) that do not deserve their own domain service.

Alembic state is organized under [`backend/migrations/`](../../backend/migrations/). Place the migration environment script, version files, and revision helpers here to keep schema changes traceable. Scripts that interact with the API or DB from the command line—for example, maintenance tasks, seed routines, or ad-hoc data patches—should live in [`backend/scripts/`](../../backend/scripts/). Backend-scoped tests stay in [`backend/tests/`](../../backend/tests/); use this folder for pytest modules that target routers, services, database interactions, RQ job enqueuing, or schema validation without booting the frontend. When adding fixtures that are specific to backend-only tests, prefer placing them next to the modules they support or in a `conftest.py` inside this directory.

## Frontend layout

The frontend application resides in [`../../frontend/`](../../frontend/). Source files sit beneath [`frontend/src/`](../../frontend/src/) to align with the Vite tooling pipeline. High-level route definitions and page-level components belong to [`frontend/src/pages/`](../../frontend/src/pages/) and [`frontend/src/routes/`](../../frontend/src/routes/), where React Router segments can map to user roles such as Student or Department Head. Shared presentational building blocks and layout primitives live in [`frontend/src/components/`](../../frontend/src/components/). Feature-oriented slices that bundle state, services, and UI for a single capability (e.g., evaluation forms, dashboards, notification center) should go into [`frontend/src/features/`](../../frontend/src/features/).

Encapsulate reusable hooks—such as TanStack Query wrappers, polling strategies, or React Hook Form adapters—in [`frontend/src/hooks/`](../../frontend/src/hooks/). Centralize API request utilities, fetch abstractions, and client-side DTO mappers within [`frontend/src/lib/api/`](../../frontend/src/lib/api/). Style configuration, including Tailwind extensions and shared CSS modules, fits under [`frontend/src/styles/`](../../frontend/src/styles/). TypeScript helper types and Zod schemas that are reused across pages live in [`frontend/src/types/`](../../frontend/src/types/). Frontend-specific tests, whether run by Vitest or Jest, should be stored in [`frontend/src/tests/`](../../frontend/src/tests/) so they can resolve relative imports cleanly while remaining close to the code under test. Public assets exposed by the Vite build continue to reside in [`frontend/public/`](../../frontend/public/).

## Testing layout

Cross-service tests have a dedicated home in [`../../tests/`](../../tests/). Use [`tests/e2e/selenium/`](../../tests/e2e/selenium/) for browser automation that walks through full workflows—logging in with seeded accounts, completing evaluations, verifying sentiment displays, or downloading exported PDFs. Keep page objects, driver utilities, and synchronization helpers together so end-to-end suites remain maintainable. Place integration scenarios that spin up only portions of the stack (for instance, API plus a fake Redis worker) in [`tests/integration/`](../../tests/integration/). Share factories, fixtures, and test data generators through [`tests/fixtures/`](../../tests/fixtures/). Common helpers such as environment bootstrappers, CLI wrappers, or Selenium capability builders live in [`tests/utils/`](../../tests/utils/).

Pytest is the default runner per [`backend/requirements.txt`](../../backend/requirements.txt). Store `pytest.ini` or equivalent configuration at the repo root or within the relevant test folder once defined. Selenium appears in the same requirements list, so plan for WebDriver binaries or remote services when scripting end-to-end flows. Backend-only tests should continue to run via `pytest backend/tests`, while the frontend can use Vitest or React Testing Library harnesses under `frontend/src/tests`. Cross-service tests can call `pytest tests` with markers to split e2e and integration coverage. Fixtures that cross boundaries—for example, provisioning a seeded database for UI tests—should live in `tests/fixtures` and be imported from backend or frontend contexts as needed to avoid duplication.

## Conventions & tips

- Keep modules short and focused. Prefer one router or service class per file, and avoid monolithic utilities.
- Name files after their primary export (`evaluations_router.py`, `useNotifications.ts`).
- Collocate schemas with their functional area, but mirror table names and API responses consistently.
- Document any non-obvious dependency (external API, third-party dataset) in README snippets next to the code using it.
- When adding secrets or environment toggles, define them inside `backend/app/core` settings objects and reference them in workers through the same module to avoid drift.
- Maintain Tailwind configuration in a single place and import shared class names via helper functions to keep JSX tidy.
- Use type-safe fetch wrappers in `frontend/src/lib/api` to enforce parity with backend schemas and reduce runtime parsing errors.
- Prefer storing long-form markdown or architecture deep dives inside `project-context-and-rules-or-guidelines/docs` to keep the code tree lightweight.

## Where new files go

- New FastAPI router → [`backend/app/api/routers/`](../../backend/app/api/routers/)
- SQLAlchemy model or Alembic helper → [`backend/app/models/`](../../backend/app/models/) or [`backend/migrations/`](../../backend/migrations/)
- Background RQ job → [`backend/app/workers/`](../../backend/app/workers/)
- CSV import service or PDF generator → [`backend/app/services/`](../../backend/app/services/)
- Shared utility or validation helper → [`backend/app/utils/`](../../backend/app/utils/)
- React page representing a routed view → [`frontend/src/pages/`](../../frontend/src/pages/)
- Reusable UI building block → [`frontend/src/components/`](../../frontend/src/components/)
- Feature module coordinating data fetching and state → [`frontend/src/features/`](../../frontend/src/features/)
- Custom React hook (query, form, polling) → [`frontend/src/hooks/`](../../frontend/src/hooks/)
- API client wrapper → [`frontend/src/lib/api/`](../../frontend/src/lib/api/)
- Frontend styling token or Tailwind plugin → [`frontend/src/styles/`](../../frontend/src/styles/)
- Frontend type definitions or validation schema → [`frontend/src/types/`](../../frontend/src/types/)
- Backend unit/integration test → [`backend/tests/`](../../backend/tests/)
- Frontend component or hook test → [`frontend/src/tests/`](../../frontend/src/tests/)
- Full-stack Selenium scenario → [`tests/e2e/selenium/`](../../tests/e2e/selenium/)
- Cross-service integration check without UI → [`tests/integration/`](../../tests/integration/)
- Shared fixtures or utilities used by multiple suites → [`tests/fixtures/`](../../tests/fixtures/) or [`tests/utils/`](../../tests/utils/)

Following this structure keeps the repository approachable for new contributors, makes CI automation straightforward, and aligns code with the deployment model outlined in the tech stack brief. Refer back to the project tech stack document whenever you introduce a new dependency or workflow to ensure the implementation stays lean and on-spec.
