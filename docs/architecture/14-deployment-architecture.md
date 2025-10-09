## **Deployment Architecture**

This section outlines the comprehensive strategy for deploying the **Proficiency** application to our production environment. It covers the specific methods for building and running both the frontend and backend services, the automated pipeline for continuous integration and deployment, and the definition of our application environments. The entire strategy is centered on our foundational architectural decision to use **Docker Compose** on a **single VPS**, ensuring a simple, manageable, and cost-effective deployment for Version 1.

### **Deployment Prerequisites**

Before a production deployment can occur, the following infrastructure prerequisites must be met:

* **Registered Domain Name:** A domain name (e.g., `proficiency-app.com`) must be registered and available.
* **DNS Management:** A plan for managing DNS records must be in place. At a minimum, this involves creating an **A record** pointing the domain and any subdomains (e.g., `app`, `staging`) to the static IP address of the production VPS.

***

### **Group 1: Deployment Strategy**

This group defines the practical, step-by-step process for how our frontend and backend applications are built and run in the production environment.

#### **Frontend Deployment**

The frontend application is a static build of our React SPA, served directly to users by our Caddy web server.

* **Platform:** **Caddy Server**, running within a Docker container on the production VPS.
* **Build Command:** `pnpm --filter web build`
* **Output Directory:** The build generates static assets into `apps/web/dist`, which is mounted as a volume into the Caddy container.
* **CDN/Edge Strategy:** For our single-VPS architecture, the **Caddy server itself will act as our edge layer**, handling asset serving, optimal caching headers, and automatic HTTPS encryption.

#### **Backend Deployment**

The backend is our monolithic FastAPI application, run as a containerized service managed by Docker Compose.

* **Platform:** **Docker Container** on the production VPS, orchestrated by Docker Compose.
* **Build Command:** `docker-compose build api`
* **Deployment Method:** The FastAPI application is run via `uvicorn` inside the container. The `docker-compose up` command starts this container along with dependent services (`db`, `redis`, `worker`). Caddy is configured to reverse-proxy `/api/*` requests to this `api` container.

***

### **Group 2: CI/CD Pipeline**

We will use **GitHub Actions** to automate the build, test, and deployment lifecycle. The pipeline is now divided into four primary jobs: `ci`, `deploy_staging`, `e2e_tests`, and `deploy_production`. This enhanced flow ensures that code is only promoted after passing all unit, integration, and end-to-end tests in a live-like environment.

The entire workflow is defined in `.github/workflows/ci.yml`.

#### **Conceptual CI/CD Pipeline Configuration (`ci.yml`)**

This configuration is the definitive blueprint for our GitHub Actions workflow, now updated to include the E2E testing gate.

```yaml
name: Continuous Integration & Deployment

on:
    push:
        branches: [main]
    pull_request:
        branches: [main]

jobs:
    # ----------------------------------------------------
    # JOB 1: Continuous Integration (Build & Unit/Integration Tests)
    # ----------------------------------------------------
    ci:
        name: Build & Test
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v4
            - uses: pnpm/action-setup@v2
              with: { version: 8 }
            - uses: actions/setup-node@v4
              with: { node-version: "20.x", cache: "pnpm" }
            - uses: actions/setup-python@v5
              with: { python-version: "3.12" }
            - name: Install Dependencies
              run: |
                  pnpm install --frozen-lockfile
                  pip install -r apps/api/requirements.txt
            - name: Lint Code
              run: pnpm lint
            - name: Run Unit & Integration Tests
              run: |
                  pnpm --filter web test
                  pnpm --filter api test
            - name: Verify Docker Build
              run: docker-compose build

    # ----------------------------------------------------
    # JOB 2: Deploy to Staging Environment
    # ----------------------------------------------------
    deploy_staging:
        name: Deploy to Staging
        needs: ci
        runs-on: ubuntu-latest
        steps:
            - uses: webfactory/ssh-agent@v0.9.0
              with:
                  ssh-private-key: ${{ secrets.STAGING_SSH_PRIVATE_KEY }}
            - name: Add Server to Known Hosts
              run: ssh-keyscan -H ${{ secrets.STAGING_SSH_HOST }} >> ~/.ssh/known_hosts
            - name: Deploy to Staging Server
              run: |
                  ssh ${{ secrets.STAGING_SSH_USER }}@${{ secrets.STAGING_SSH_HOST }} '
                    cd /path/to/prof-evaluation-app && \
                    git pull origin main && \
                    docker-compose -f docker-compose.yml -f docker-compose.staging.yml down && \
                    docker-compose -f docker-compose.yml -f docker-compose.staging.yml up --build -d && \
                    docker-compose exec api alembic upgrade head
                  '

    # ----------------------------------------------------
    # JOB 3: Run End-to-End Tests
    # ----------------------------------------------------
    e2e_tests:
        name: Run End-to-End Tests
        needs: deploy_staging
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v4
            - uses: pnpm/action-setup@v2
              with: { version: 8 }
            - uses: actions/setup-node@v4
              with: { node-version: "20.x", cache: "pnpm" }
            - name: Install Frontend Dependencies
              run: pnpm install --frozen-lockfile
            - name: Install Cypress
              run: pnpm --filter web exec cypress install
            - name: Run Cypress E2E Suite (with Accessibility Checks)
              run: pnpm --filter web exec cypress run --browser chrome
              env:
                  CYPRESS_BASE_URL: https://staging.proficiency-app.com

    # ----------------------------------------------------
    # JOB 4: Deploy to Production
    # ----------------------------------------------------
    deploy_production:
        name: Deploy to Production
        needs: e2e_tests
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        runs-on: ubuntu-latest
        steps:
            - uses: webfactory/ssh-agent@v0.9.0
              with:
                  ssh-private-key: ${{ secrets.PROD_SSH_PRIVATE_KEY }}
            - name: Add Server to Known Hosts
              run: ssh-keyscan -H ${{ secrets.PROD_SSH_HOST }} >> ~/.ssh/known_hosts
            - name: Deploy to Production Server
              run: |
                  ssh ${{ secrets.PROD_SSH_USER }}@${{ secrets.PROD_SSH_HOST }} '
                    cd /path/to/prof-evaluation-app && \
                    git pull origin main && \
                    docker-compose down && \
                    docker-compose up --build -d && \
                    docker-compose exec api alembic upgrade head && \
                    docker system prune -af
                  '
```

#### **Key Principles & Secrets Management**

* **Automation Trigger:** The workflow triggers on any `push` or `pull_request` to the `main` branch.
* **Job Dependency:** The pipeline now follows a strict, sequential dependency: `ci` -> `deploy_staging` -> `e2e_tests` -> `deploy_production`. A failure at any stage prevents promotion to the next.
* **E2E Testing Gate:** The `e2e_tests` job is now a mandatory quality gate. Production deployment can only occur after all Cypress tests (including accessibility checks) have passed against the live staging environment.
* **Secrets Management:** Secrets are managed via GitHub Repository Secrets. The secret names have been updated to be environment-specific (e.g., `STAGING_SSH_HOST`, `PROD_SSH_HOST`) to support the multi-stage pipeline.

***

### **Group 3: Environments**

To ensure a stable and predictable path from development to release, the **Proficiency** platform will utilize three distinct environments. Each environment is isolated and serves a specific purpose in our development and deployment workflow.

| Environment     | Frontend URL                          | Backend URL                                  | Purpose                                                                                                                              |
| :-------------- | :------------------------------------ | :------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------- |
| **Development** | `http://localhost:5173`               | `http://localhost/api/v1`                    | Local development and rapid iteration by developers on their individual machines.                                                    |
| **Staging**     | `https://staging.proficiency-app.com` | `https://staging.proficiency-app.com/api/v1` | A production-like environment for final testing, user acceptance testing (UAT), and stakeholder reviews before a production release. |
| **Production**  | `https://app.proficiency-app.com`     | `https://app.proficiency-app.com/api/v1`     | The live environment accessible to all end-users.                                                                                    |

***
