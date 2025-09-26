# Project Structure Guide

## Overview

This monorepo keeps the FastAPI backend, React frontend, and shared automation separated but discoverable. Top-level folders map to the deployment units in [`actual_project_context/project_techstack.md`](../actual_project_context/project_techstack.md):

- `backend/` – API, domain logic, data access, and background workers.
- `frontend/` – Vite + React TypeScript client for dashboards and forms.
- `tests/` – Selenium, integration, and utilities that span services.
- `project-context-and-rules-or-guidelines/` & `project-progress/` – documentation, conventions, and active follow-ups.

Keeping boundaries explicit reduces hidden dependencies and helps contributors land in the right folder quickly.

## Backend layout

The backend in [`../../backend/`](../../backend/) follows standard FastAPI boundaries:

- [`api/routers/`](../../backend/app/api/routers/) – path operations grouped by feature area.
- [`core/`](../../backend/app/core/) – configuration, security helpers, dependency wiring.
- [`db/`](../../backend/app/db/) – engine setup, sessions, and data-loading helpers.
- [`models/`](../../backend/app/models/) & [`schemas/`](../../backend/app/schemas/) – ORM entities and matching Pydantic types.
- [`services/`](../../backend/app/services/) – reusable domain logic that coordinates data and side effects.
- [`workers/`](../../backend/app/workers/) – RQ job definitions executed outside request/response.
- [`ml/`](../../backend/app/ml/) – local inference wrappers.
- [`utils/`](../../backend/app/utils/) – lightweight helpers that do not fit a feature module.

Keep migrations in [`backend/migrations/`](../../backend/migrations/), CLI scripts in [`backend/scripts/`](../../backend/scripts/), and backend-scoped tests in [`backend/tests/`](../../backend/tests/).

## Frontend layout

The frontend in [`../../frontend/`](../../frontend/) keeps source under [`frontend/src/`](../../frontend/src/) with these core buckets:

- [`pages/`](../../frontend/src/pages/) & [`routes/`](../../frontend/src/routes/) – routed views and navigation tables.
- [`features/`](../../frontend/src/features/) – feature slices that own data fetching, state, and UI.
- [`components/`](../../frontend/src/components/) – reusable presentation pieces.
- [`hooks/`](../../frontend/src/hooks/) – shared hook implementations (queries, forms, polling).
- [`lib/api/`](../../frontend/src/lib/api/) – API clients, DTO mappers, and fetch wrappers.
- [`styles/`](../../frontend/src/styles/) – Tailwind extensions or shared CSS modules.
- [`types/`](../../frontend/src/types/) – TypeScript helpers reused across the app.
- [`tests/`](../../frontend/src/tests/) – Vitest/RTL suites colocated with source.
- [`public/`](../../frontend/public/) – static assets exposed by Vite.

## Testing layout

Cross-service tests live in [`../../tests/`](../../tests/) with familiar groupings:

- [`e2e/selenium/`](../../tests/e2e/selenium/) – full browser workflows.
- [`integration/`](../../tests/integration/) – targeted multi-service checks.
- [`fixtures/`](../../tests/fixtures/) – shared factories and data builders.
- [`utils/`](../../tests/utils/) – environment bootstrappers and helpers.

Pytest (see [`backend/requirements.txt`](../../backend/requirements.txt)) drives backend and cross-service suites. Run `pytest backend/tests` for backend coverage, `pytest tests` for shared suites, and use Vitest or React Testing Library under `frontend/src/tests` for UI checks. Share cross-cutting fixtures from `tests/fixtures` to avoid duplication.

## Conventions & tips

- Keep modules focused—ideally one router, service, or component per file.
- Name files after their primary export (`evaluations_router.py`, `useNotifications.ts`).
- Collocate schemas with their functional area and mirror table names or API responses.
- Document non-obvious dependencies (external APIs, datasets) near the code that relies on them.
- Define secrets and environment toggles in `backend/app/core` so workers reuse the same settings.
- Centralize Tailwind configuration and share class names through helpers to keep JSX tidy.
- Use type-safe fetch wrappers in `frontend/src/lib/api` to align with backend schemas.
- Keep deep-dive documentation in `project-context-and-rules-or-guidelines/docs` to lighten the code tree.

## Where new files go

- FastAPI router → [`backend/app/api/routers/`](../../backend/app/api/routers/)
- SQLAlchemy model or Alembic helper → [`backend/app/models/`](../../backend/app/models/) or [`backend/migrations/`](../../backend/migrations/)
- Background job → [`backend/app/workers/`](../../backend/app/workers/)
- Backend service or utility → [`backend/app/services/`](../../backend/app/services/) or [`backend/app/utils/`](../../backend/app/utils/)
- React page or routed view → [`frontend/src/pages/`](../../frontend/src/pages/) (with routes in [`frontend/src/routes/`](../../frontend/src/routes/))
- Feature slice → [`frontend/src/features/`](../../frontend/src/features/)
- Shared component → [`frontend/src/components/`](../../frontend/src/components/)
- Custom hook → [`frontend/src/hooks/`](../../frontend/src/hooks/)
- API client → [`frontend/src/lib/api/`](../../frontend/src/lib/api/)
- Styling token or Tailwind plugin → [`frontend/src/styles/`](../../frontend/src/styles/)
- Shared types → [`frontend/src/types/`](../../frontend/src/types/)
- Backend test → [`backend/tests/`](../../backend/tests/)
- Frontend test → [`frontend/src/tests/`](../../frontend/src/tests/)
- Selenium scenario → [`tests/e2e/selenium/`](../../tests/e2e/selenium/)
- Cross-service test without UI → [`tests/integration/`](../../tests/integration/)
- Shared fixture or helper → [`tests/fixtures/`](../../tests/fixtures/) or [`tests/utils/`](../../tests/utils/)

Following this structure keeps the repository approachable, makes CI automation straightforward, and aligns code with the deployment model in the tech stack brief. Revisit the tech stack document before adding new dependencies or workflows to ensure they stay on-spec.
