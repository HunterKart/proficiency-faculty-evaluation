## Unified Project Structure

This section defines the complete directory and file structure for the **Proficiency** monorepo. The structure is a direct physical implementation of our architectural decisions, designed to enforce separation of concerns, facilitate code sharing, and provide a clear, predictable organization for both developers and AI agents. It is managed by **pnpm workspaces** as the chosen monorepo tool.

***

### Group 1: Monorepo Root & Core Tooling

This foundational group establishes the root of the monorepo and contains the project-wide configuration files that govern tooling, dependency management, container orchestration, and continuous integration. It is the central nervous system of our development environment.

```plaintext
prof-evaluation-app/
├── .github/
│   └── workflows/
│       ├── ci.yml         # Continuous Integration: Linting, Testing, Building
│       └── deploy.yml     # Continuous Deployment: Push to VPS
├── docs/
├── scripts/
├── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yml     # Orchestrates all services for local development
├── package.json           # Monorepo root, defines workspaces and scripts
├── pnpm-workspace.yaml    # pnpm workspace configuration
└── README.md
```

#### **Breakdown of Root Directories & Files:**

* **`.github/workflows/`**: This directory will contain our **GitHub Actions** configurations.

  * `ci.yml`: Defines the Continuous Integration pipeline that will automatically run on every push and pull request. It will be responsible for installing dependencies, running linters, and executing the entire test suite for both the frontend and backend.
  * `deploy.yml`: Defines the Continuous Deployment pipeline. This workflow will be triggered on merges to the main branch and will be responsible for securely connecting to our single VPS, pulling the latest changes, and restarting the services via Docker Compose.

* **`docs/`**: The designated location for all high-level project documentation, including the `prd.md`, `front-end-spec.md`, and this `architecture.md` document.

* **`scripts/`**: This directory will house any custom shell scripts needed for managing the monorepo, such as a script to run all services concurrently or to clean all build artifacts.

* **`docker-compose.yml`**: The core orchestration file for our local development environment. It defines all the services specified in our tech stack (`api`, `web`, `worker`, `db`, `redis`), their container configurations, networking, and volume mounts, as required by Story 1.1.

* **`package.json`**: The root `package.json` for the monorepo. It will define the pnpm workspace paths and contain scripts for running commands across all packages (e.g., `pnpm run test:all`).

* **`pnpm-workspace.yaml`**: This is the configuration file specific to **pnpm**, defining the locations of our application and shared packages (e.g., `apps/*`, `packages/*`) to enable the monorepo functionality.

***

### Group 2: Application Packages (`apps/`)

This directory contains the primary, deployable applications. Following our decoupled architectural pattern, we have a distinct package for the frontend (`web`) and the backend (`api`). This separation allows for independent development and scaling while benefiting from the monorepo's shared tooling.

```plaintext
prof-evaluation-app/
└── apps/
    ├── api/      # The Python/FastAPI Backend Application
    └── web/      # The TypeScript/React Frontend Application
```

***

#### **`apps/web` (Frontend)**

This package contains the entire React Single-Page Application (SPA). Its structure is organized by feature and function, adhering to the patterns established in the **Frontend Architecture** section of this document.

```plaintext
apps/web/
├── public/
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── features/
│   │   ├── layouts/
│   │   ├── shared/
│   │   └── ui/
│   ├── context/
│   ├── hooks/
│   ├── lib/
│   ├── pages/
│   ├── routes/
│   ├── services/
│   └── types/
│   ├── App.tsx
│   └── main.tsx
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

**Breakdown of Frontend Structure:**

* **`src/index.css`**: Imports Tailwind CSS and defines design tokens using the v4 CSS-first `@theme` workflow. This file replaces the legacy `tailwind.config.js` and `postcss.config.js` setup; all global styling primitives live here.
* **`src/components/`**: This is the core of the UI library, organized using the hybrid Atomic Design methodology previously defined. It is divided into `/ui` (primitives from `shadcn/ui`), `/layouts` (page structures), `/shared` (custom reusable components), and `/features` (domain-specific components).
* **`src/pages/`**: Contains the top-level components for each route, which are lazy-loaded by the router for performance.
* **`src/routes/`**: Centralizes all client-side routing logic using **React Router**, including the `RouteGuard` for authentication and authorization.
* **`src/services/` & `src/hooks/`**: This is the dedicated data-fetching layer. The `services` directory contains functions for making API calls, while the `hooks` directory wraps this logic with **TanStack Query** for caching, refetching, and managing server state.
* **Tailwind Configuration**: Tailwind CSS v4 no longer relies on `tailwind.config.js` or `postcss.config.js`. Do not add those files; instead, declare tokens and additional utilities inside `src/index.css` using the `@theme` and `@utility` directives provided by Tailwind v4 (see Tailwind Labs, “Tailwind CSS v4.0” update).

***

#### **`apps/api` (Backend)**

This package contains our monolithic **FastAPI** application, including the API server, background worker definitions, and all related business logic. The structure follows the clean, layered architecture previously defined.

```plaintext
apps/api/
├── alembic/
├── src/
│   ├── api/
│   │   └── v1/
│   │       ├── deps.py
│   │       └── endpoints/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── worker/
│   ├── main.py
├── tests/
├── alembic.ini
├── Dockerfile
├── package.json
└── requirements.txt
```

**Breakdown of Backend Structure:**

* **Layered Architecture**: The structure enforces a strict separation of concerns into an HTTP layer (`src/api/v1/endpoints/`), a business logic layer (`src/services/`), and a data access layer (`src/repositories/`).
* **Data Contracts**: The `src/models/` directory contains the **SQLAlchemy** ORM models, while `src/schemas/` holds the **Pydantic** models for API validation.
* **Asynchronous Tasks**: The `src/worker/` directory defines all background jobs to be executed by our **RQ worker**, such as data imports and report generation.
* **Database & Testing**: The `alembic/` directory stores database migration scripts, and the `tests/` directory contains the entire **Pytest** suite.

***

### Group 3: Shared Packages (`packages/`)

This directory is critical for maintaining consistency and reducing code duplication. It houses packages designed to be consumed by other applications in the monorepo. This creates a **single source of truth** for shared logic, types, and configurations, eliminating a common source of bugs in decoupled applications.

```plaintext
prof-evaluation-app/
└── packages/
    ├── config/
    │   ├── eslint-preset/
    │   └── tsconfig/
    ├── shared-types/
    └── ui/
```

#### **Breakdown of Shared Packages:**

* **`config/`**: This package centralizes our development tooling configurations to enforce a consistent standard across the entire monorepo.

  * `eslint-preset/`: Contains a shared **ESLint** configuration. Both the `web` application and other shared packages will extend this preset to ensure a uniform coding style and quality standard.
  * `tsconfig/`: Contains a base **TypeScript** configuration (`tsconfig.base.json`). All TypeScript-based packages will extend this file to ensure consistent compiler options.

* **`shared-types/`**: This package defines and exports all **TypeScript interfaces** for our data models and API payloads. By having both the frontend and backend reference this single package for data contracts, we guarantee type safety and prevent "data drift" between the client and server.

* **`ui/`**: This package will house our project-specific, reusable **React components** built from `shadcn/ui` primitives. As mandated by the UI/UX spec, leveraging the monorepo for a shared UI package ensures a consistent look and feel throughout the application.

***

### Group 4: Configuration Packages (`packages/config/`)

This directory is a best-practice implementation for a scalable monorepo. Its purpose is to centralize the configurations for our essential development tools, ensuring that every package in the workspace adheres to the same standards for code style and compilation. This creates a single source of truth for our development standards, providing a consistent experience for all developers and our CI pipeline.

```plaintext
prof-evaluation-app/
└── packages/
    └── config/
        ├── eslint-preset/
        │   ├── index.js
        │   └── package.json
        └── tsconfig/
            ├── base.json
            └── package.json
```

#### **Breakdown of Configuration Packages:**

* **`eslint-preset/`**: This package contains our shared **ESLint** configuration.

  * **Purpose**: It defines the single set of rules for code style, quality, and formatting that will be enforced across all TypeScript code in the monorepo (including the `web` app and the `ui` and `shared-types` packages).
  * **Implementation**: Other packages will install this preset as a development dependency and extend its configuration in their local `eslintrc.js` file. This guarantees that all code adheres to the same standard.

* **`tsconfig/`**: This package provides a base **TypeScript** configuration for the entire project.

  * **Purpose**: The `base.json` file will contain all common compiler options, path aliases, and settings that should apply globally.
  * **Implementation**: Each TypeScript package (`apps/web`, `packages/ui`, etc.) will have its own `tsconfig.json` that simply `extends` this base configuration. This ensures consistency while allowing for minor, package-specific overrides (like JSX settings for React).

***

### Group 5: Operational & Documentation Directories

This final group contains top-level directories that are essential for the project's operation and maintenance but are not part of the application source code itself. They house our infrastructure definitions and the formal documentation that guides the project.

```plaintext
prof-evaluation-app/
├── docs/
└── infrastructure/
    └── docker/
        ├── api/
        │   └── Dockerfile
        ├── web/
        │   └── Caddyfile
        └── worker/
            └── Dockerfile
```

#### **Breakdown of Operational Directories:**

* **`docs/`**: This directory serves as the **single source of truth for all project planning and design artifacts**. It contains the critical documents that define the "what, why, and how" of the project, including the `prd.md`, `front-end-spec.md`, and this `architecture.md` document.

* **`infrastructure/`**: This directory contains all configurations related to our deployment and local development environments, implementing our "Infrastructure as Code" approach.

  * **`docker/`**: This subdirectory centralizes all configurations for building our service containers.
    * `api/Dockerfile`: Defines the build process for creating the production-ready container image for our **FastAPI backend application**.
    * `web/Caddyfile`: The configuration file for our **Caddy reverse proxy**. It will contain the rules for serving the static React frontend assets and for securely proxying all requests to `/api/*` to our backend service.
    * `worker/Dockerfile`: Defines the build process for our **RQ background worker** container, ensuring its environment is consistent with the API service.

***

### **The Complete Project Structure**

Here is the fully consolidated structure, which serves as the definitive blueprint for our project repository.

```plaintext
prof-evaluation-app/
├── .github/                 # Group 1: CI/CD Workflows
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── apps/                    # Group 2: Primary Applications
│   ├── api/                 # Backend: FastAPI
│   │   ├── alembic/
│   │   ├── src/
│   │   │   ├── api/
│   │   │   │   └── v1/
│   │   │   │       ├── deps.py
│   │   │   │       └── endpoints/
│   │   │   ├── core/
│   │   │   ├── db/
│   │   │   ├── models/
│   │   │   ├── repositories/
│   │   │   ├── schemas/
│   │   │   ├── services/
│   │   │   └── worker/
│   │   │   └── main.py
│   │   ├── tests/
│   │   ├── alembic.ini
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── requirements.txt
│   └── web/                 # Frontend: React (Vite)
│       ├── public/
│       │   └── favicon.ico
│       ├── src/
│       │   ├── components/
│       │   │   ├── features/
│       │   │   ├── layouts/
│       │   │   ├── shared/
│       │   │   └── ui/
│       │   ├── context/
│       │   ├── hooks/
│       │   ├── lib/
│       │   ├── pages/
│       │   ├── routes/
│       │   ├── services/
│       │   └── types/
│       │   ├── App.tsx
│       │   └── main.tsx
│       ├── index.html
│       ├── package.json
│       ├── tsconfig.json
│       └── vite.config.ts
├── docs/                    # Group 5: Project Documentation
├── infrastructure/          # Group 5: Infrastructure as Code
│   └── docker/
│       ├── api/
│       │   └── Dockerfile
│       ├── web/
│       │   └── Caddyfile
│       └── worker/
│           └── Dockerfile
├── packages/                # Group 3 & 4: Shared Code & Configs
│   ├── config/
│   │   ├── eslint-preset/
│   │   └── tsconfig/
│   ├── shared-types/
│   └── ui/
├── scripts/                 # Group 1: Monorepo Scripts
├── .dockerignore            # Group 1
├── .env.example             # Group 1
├── .gitignore               # Group 1
├── docker-compose.yml       # Group 1
├── package.json             # Group 1
├── pnpm-workspace.yaml      # Group 1
└── README.md                # Group 1
```

***
