# Proficiency Faculty Evaluation

Proficiency is a full-stack platform for managing faculty evaluations. The repository is organized as a pnpm-powered monorepo that houses the React frontend, FastAPI backend, shared packages, and infrastructure configuration.

## Project Structure

- `apps/api` – FastAPI service scaffold (Python).
- `apps/web` – React 19 + Vite SPA scaffold (TypeScript).
- `packages` – Reserved for shared libraries (`shared-types`, `ui`, `config`, etc.).
- `infrastructure/docker` – Container configuration (Caddy reverse proxy, service Dockerfiles).
- `docs` – Product, architecture, and planning documentation.

## Prerequisites

- [pnpm](https://pnpm.io/) >= 9
- [Python](https://www.python.org/) 3.12
- [Docker](https://docs.docker.com/get-docker/) & Docker Compose

## Initial Setup

```bash
# Install Node dependencies for all workspaces
pnpm install

# (Optional) Create and activate a Python virtual environment
python -m venv .venv
source .venv/bin/activate
pip install -r apps/api/requirements.txt
```

Copy `.env.example` to `.env` and adjust configuration as needed before running services.

## Local Development with Docker Compose

```bash
# Build frontend assets
pnpm --filter @proficiency/web build

# Launch all services
docker-compose up -d --build
```

Available endpoints:

- Frontend: http://localhost:3000
- API: http://localhost:8000 (proxy available at `/api` on port 3000)
- Redis: `localhost:6379`
- MariaDB: `localhost:3307`

Shutdown the stack with `docker-compose down`.

## Running Tests

```bash
# Frontend Vitest suite
pnpm --filter @proficiency/web test

# Backend pytest suite (requires Python deps)
pnpm --filter @proficiency/api test
```

## Useful Scripts

- `pnpm lint` – Placeholder lint aggregator.
- `pnpm test` – Placeholder test aggregator.
- `pnpm --filter @proficiency/web dev` – Start Vite dev server.
- `pnpm --filter @proficiency/api dev` – Run FastAPI with auto-reload.
