## **Development Workflow**

This section provides the definitive, practical guide for setting up the local development environment and running the **Proficiency** application. It is designed to ensure a consistent, efficient, and predictable workflow for all developers and AI agents contributing to the project.

### **Group 1: Foundational Setup & Prerequisites**

**Purpose:** To provide a complete, step-by-step guide for a developer to go from a clean machine to a fully installed and bootstrapped project, ready for development.

#### **1.1. System Prerequisites**

Before cloning the repository, it is mandatory that the following software is installed and correctly configured on the development machine. These versions are aligned with our chosen tech stack to ensure a consistent and reproducible environment.

| Tool                        | Version         | Purpose                                             |
| :-------------------------- | :-------------- | :-------------------------------------------------- |
| **Node.js**                 | 20.x (LTS)      | JavaScript runtime for `pnpm` and frontend tooling. |
| **pnpm**                    | latest          | The designated package manager for our monorepo.    |
| **Python**                  | 3.12.x          | Backend language and runtime.                       |
| **Docker & Docker Compose** | 2.27.x or newer | Containerization and local service orchestration.   |
| **Git**                     | latest          | Version control for managing the codebase.          |

**Recommendation:** It is highly advisable to use a version manager like `nvm` for Node.js and `pyenv` for Python to easily switch between versions and avoid system-level conflicts.

***

#### **1.2. Initial Project Setup**

Follow these one-time setup steps to get the project running locally.

1. **Clone the Repository**

   Clone the monorepo from the source control provider to your local machine.

   ```bash
   git clone <repository_url>/prof-evaluation-app.git
   cd prof-evaluation-app
   ```

2. **Set Up Local Environment Variables**

   The project uses a central `.env.example` file at the root. You must create local environment files for the services that require them before the initial build.

   * First, copy the example file to create your primary local configuration:
     ```bash
     cp .env.example .env
     ```
   * Next, open the newly created `.env` file and fill in any required secrets (e.g., database passwords, external API keys).

3. **Build and Start All Services**

   This single command will build the Docker images for all services (API, worker, and web proxy) and start them in a detached mode. The build process automatically installs all `npm` and `pip` dependencies inside the containers.

   ```bash
   docker-compose up --build -d
   ```

4. **Run Initial Database Migrations**

   With the containers running, execute the initial database migration to create all tables and relationships as defined in our schema. This command is run *inside* the running `api` container, using the Alembic tool specified in our architecture.

   ```bash
   docker-compose exec api alembic upgrade head
   ```

***

### **Group 2: Core Development Commands & Workflow**

**Purpose:** To define the essential, day-to-day commands a developer will use to run the application, execute tests, and maintain code quality, ensuring a consistent and efficient development cycle.

***

#### **2.1. Running the Application**

The following workflows describe how to run the application's services. The primary workflow utilizes **Docker Compose** to ensure an environment that closely mirrors production.

**Primary Workflow (Docker Compose)**

This is the recommended approach for most development tasks.

* **Start All Services:**
  To start all services (`api`, `web`, `worker`, `db`, `redis`) in the background, run the following from the project root:

  ```bash
  docker-compose up -d
  ```

* **View Service Logs:**
  To view the real-time, aggregated logs from all running services:

  ```bash
  docker-compose logs -f
  ```

  To follow the logs for a specific service (e.g., the `api`):

  ```bash
  docker-compose logs -f api
  ```

* **Stop All Services:**
  To gracefully stop all running services:

  ```bash
  docker-compose down
  ```

* **Rebuild and Restart:**
  If you have made changes to dependencies (`requirements.txt` or `package.json`) or Docker configurations, you must rebuild the images:

  ```bash
  docker-compose up --build -d
  ```

**Alternative Workflow (Individual Local Services)**

This workflow is useful for focused, rapid iteration on a single service (primarily the frontend) without restarting the entire Docker stack. It assumes you have a running Docker instance for the database and other dependencies.

* **Run Frontend Only (Vite HMR):**
  For the fastest frontend development experience with Hot Module Replacement (HMR), run the Vite dev server directly:

  ```bash
  # From the monorepo root
  pnpm --filter web dev
  ```

* **Run Backend Only (FastAPI Live Reload):**
  To run the FastAPI server with live-reloading, execute the following from the `apps/api` directory (ensure you have an active Python virtual environment with dependencies installed):

  ```bash
  # From the apps/api directory
  uvicorn src.main:app --reload
  ```

***

#### **2.2. Testing & Quality Assurance**

This section details the commands for executing our comprehensive testing and linting strategies, which are critical for maintaining code quality and integrity.

* **Running the Full Test Suite:**
  To execute all backend (**Pytest**) and frontend (**Vitest**) tests across the monorepo, run the master script from the project root:

  ```bash
  # This command will be configured in the root package.json
  pnpm test
  ```

* **Running Backend Tests (Pytest):**
  To run the backend test suite inside its Docker container, which ensures the testing environment is consistent, use the `exec` command:

  ```bash
  docker-compose exec api pytest
  ```

* **Running Frontend Tests (Vitest):**
  To run the frontend unit and integration tests using **Vitest**, use the pnpm filter command from the root:

  ```bash
  pnpm --filter web test
  ```

* **Running End-to-End Tests (Cypress):**
  To open the **Cypress** test runner for interactive E2E testing:

  ```bash
  pnpm --filter web cypress:open
  ```

  To run all Cypress tests headlessly, as they would run in our CI pipeline:

  ```bash
  pnpm --filter web cypress:run
  ```

* **Code Linting and Formatting:**
  To check the entire codebase for linting errors based on our shared **ESLint** preset:

  ```bash
  pnpm lint
  ```

  To automatically fix fixable linting and formatting issues:

  ```bash
  pnpm format
  ```

***

### **Group 3: Environment Configuration & Secrets Management**

**Purpose:** To provide a definitive guide on how to configure local environment variables, ensuring developers can connect to all necessary services without exposing sensitive credentials. This is a critical step for both application functionality and security.

***

#### **3.1. Environment Variable Setup**

The project utilizes a `.env` file at the monorepo root to manage all environment-specific configurations and secrets. A template file, `.env.example`, is provided in the repository to serve as a blueprint.

To create your local configuration, copy the template:

```bash
cp .env.example .env
```

After creating the `.env` file, you must open it and populate the values for your local setup.

**CRITICAL:** The `.env` file is explicitly listed in the project's `.gitignore`. It contains sensitive information and **must never be committed to version control**.

***

#### **3.2. Required Variables**

The single root `.env` file provides configuration to all services orchestrated by Docker Compose, as defined in our architecture. The table below lists the variables required for the application to run correctly.

| Variable                          | Example Value              | Service(s)            | Description                                                                   |
| :-------------------------------- | :------------------------- | :-------------------- | :---------------------------------------------------------------------------- |
| **`DB_USER`**                     | `prof_user`                | `db`, `api`, `worker` | The username for the MariaDB database.                                        |
| **`DB_PASSWORD`**                 | `your_secure_password`     | `db`, `api`, `worker` | The password for the database user. **Must be set.**                          |
| **`DB_HOST`**                     | `db`                       | `api`, `worker`       | The Docker service name for the database container.                           |
| **`DB_PORT`**                     | `3306`                     | `api`, `worker`       | The internal port for the database container.                                 |
| **`DB_NAME`**                     | `proficiency_db`           | `db`, `api`, `worker` | The name of the application database.                                         |
| **`REDIS_HOST`**                  | `redis`                    | `api`, `worker`       | The Docker service name for the Redis container.                              |
| **`REDIS_PORT`**                  | `6379`                     | `api`, `worker`       | The internal port for the Redis container.                                    |
| **`SECRET_KEY`**                  | `a_long_random_hex_string` | `api`                 | A secret key used for signing JWTs. **Must be set to a long, random string.** |
| **`ACCESS_TOKEN_EXPIRE_MINUTES`** | `15`                       | `api`                 | The lifespan of a JWT access token.                                           |
| **`GEMINI_API_KEY`**              | `your_gemini_api_key`      | `worker`              | The API key for the external Gemini service.                                  |
| **`SMTP_HOST`**                   | `smtp.mailprovider.com`    | `worker`              | The hostname for the external SMTP relay service.                             |
| **`SMTP_PORT`**                   | `587`                      | `worker`              | The port for the SMTP service.                                                |
| **`SMTP_USER`**                   | `your_smtp_username`       | `worker`              | The username for the SMTP service.                                            |
| **`SMTP_PASSWORD`**               | `your_smtp_password`       | `worker`              | The password for the SMTP service.                                            |

**Note on Frontend Variables:**
In our Docker Compose setup, the Caddy server (`web` service) acts as a reverse proxy, serving the frontend and forwarding API requests from the same origin. Therefore, the frontend application does not require a `VITE_API_URL` environment variable for local development, as all API calls are relative paths (e.g., `/api/v1/...`).

***
