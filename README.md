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

### Environment variables

The minimal variables required for backend services live in `.env`:

| Variable | Purpose | Default (Docker) |
| --- | --- | --- |
| `DATABASE_URL` | SQLAlchemy connection string for Alembic and the API | `mysql+pymysql://root:@db:3306/proficiency-database` |
| `REDIS_URL` | Redis connection string for queues/caching | `redis://redis:6379/0` |
| `VITE_API_BASE_URL` | Frontend → API proxy base URL | `http://localhost:3000/api` |

Adjust these for your target environment. For example, when running the API directly on your host you might use `mysql+pymysql://root:password@127.0.0.1:3306/proficiency`.

## Database setup & migrations

### Local workflow

1. Ensure `.env` is present with the desired `DATABASE_URL`.
2. Start dependent services:
   ```bash
   docker compose up -d db redis
   ```
3. Apply the schema with Alembic:
   ```bash
   pnpm db:migrate
   # internally runs: docker compose run --rm api alembic upgrade head
   ```
4. (Optional) Inspect the database directly:
   ```bash
   docker compose exec db mysql -u root -p
   mysql> SHOW TABLES;
   mysql> SELECT * FROM alembic_version;
   ```
5. When finished, tear down containers with `docker compose down` (add `-v` to wipe the volume).

### Deployment workflow

For staging/production environments, run the same migration step against the live database before releasing the API:

```bash
# Substitute DATABASE_URL for your production credentials (env var or .env file)
docker compose --profile prod run --rm api alembic upgrade head
```

If you deploy via another orchestrator, ensure the API container (or a dedicated migration job) runs `alembic upgrade head` with the appropriate credentials before the application serves traffic.

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

## AI/ML worker environment

The asynchronous worker installs heavy AI/ML dependencies up front so later tasks execute quickly. The Dockerfile lives at `apps/api/worker.Dockerfile` and pins:

- `transformers`
- `torch`
- `keybert`
- `google-generativeai`
- `scikit-learn`

To build or refresh the worker image:

```bash
docker compose build worker
```

This command may take several minutes on the first run as it downloads model runtimes. For production, incorporate the same build step (or push a pre-built image) so deployment nodes do not recompile these packages on boot.

## Running Tests

```bash
# Frontend Vitest suite
pnpm --filter @proficiency/web test

# Backend pytest suite (requires Python deps)
pnpm --filter @proficiency/api test
```

## Useful Scripts

- `pnpm lint` – Placeholder lint aggregator.
- `pnpm db:migrate` – Apply the latest Alembic migration inside the API container.
- `pnpm test` – Placeholder test aggregator.
- `pnpm --filter @proficiency/web dev` – Start Vite dev server.
- `pnpm --filter @proficiency/api dev` – Run FastAPI with auto-reload.
