# Proficiency Fullstack Architecture Document

---

## Section 1: Introduction

This document outlines the complete fullstack architecture for **Proficiency**, including backend systems, frontend implementation, and their integration. It serves as the single source of truth for AI-driven development, ensuring consistency across the entire technology stack. This unified approach combines what would traditionally be separate backend and frontend architecture documents, streamlining the development process for modern fullstack applications where these concerns are increasingly intertwined.

#### Starter Template or Existing Project

The project is based on a pre-defined **monorepo structure** that is already initialized. The specific layout for the backend, frontend, and shared testing directories is detailed in the `PROJECT_STRUCTURE.md` document. This existing structure will serve as the foundation for all subsequent development, and this architectural document will align with its conventions.

#### Change Log

| Date       | Version | Description                                                                                                                     | Author             |
| :--------- | :------ | :------------------------------------------------------------------------------------------------------------------------------ | :----------------- |
| 2025-10-03 | 1.0     | Initial draft of the fullstack architecture document, including finalized High-Level Architecture, Tech Stack, and Data Models. | Winston, Architect |

---

## Section 2: High-Level Architecture (Revised)

#### Technical Summary

The Proficiency platform will be implemented as a **monolithic, multi-tenant SaaS application** housed within a single monorepo. The architecture is designed for simplicity and resilience, featuring a **React/TypeScript frontend** and a **Python/FastAPI backend**. For improved performance and data safety, the stateful components (**database and Redis queue**) will be decoupled into **external managed services**. The frontend will communicate with the backend via a synchronous REST API, with all computationally intensive tasks offloaded to an **asynchronous background worker**. The stateless application services will be deployed to a **single VPS using Docker Compose**. This architecture directly supports the PRD's goals of providing a modern, data-centric, and responsive user experience while ensuring high availability and minimal data loss risk.

#### Platform and Infrastructure Choice

The deployment target utilizes a hybrid approach, combining a self-hosted application server with managed services for state, aligning with the project's need for both control and resilience.

-   **Application Host:** Single Virtual Private Server (Ubuntu) with Docker.
-   **Key Services (via Docker Compose):**
    -   `caddy`: Serves as the reverse proxy, handles automatic HTTPS/TLS, and serves the static frontend build.
    -   `api`: The core FastAPI backend application.
    -   `worker`: The RQ background worker(s) for processing heavy tasks.
-   **Managed Services:**
    -   **Managed MariaDB/MySQL Database:** Decouples the primary database from the application host, providing automated backups, Point-in-Time Recovery (PITR), and reducing resource contention.
    -   **Managed Redis Instance:** Ensures the reliability and availability of the job queue, independent of the application server's status.

#### Repository Structure

The project will use a **Monorepo structure** as specified in the PRD and `PROJECT_STRUCTURE.md`. This simplifies dependency management and ensures consistency between frontend and backend code.

-   **Structure:** Monorepo.
-   **Package Organization:** The structure will follow the provided `PROJECT_STRUCTURE.md`, with distinct top-level directories for `backend/`, `frontend/`, and `tests/` to maintain clear boundaries.

#### High-Level Architecture Diagram

This revised diagram illustrates the decoupled architecture, with stateful managed services separated from the stateless application host.

```mermaid
graph TD
    User([User]) --> Browser;

    subgraph "Managed Cloud Services"
        DB[(Managed<br/>MariaDB/MySQL)];
        Redis[Managed<br/>Redis];
    end

    subgraph "Application VPS (Docker Compose)"
        Browser -- HTTPS --> Caddy[Caddy Reverse Proxy];
        Caddy --> Frontend[React Frontend<br/>(Static Build)];
        Caddy -- /api --> Backend[FastAPI API];
        Worker[RQ Worker(s)];
    end

    Frontend -- API Calls --> Backend;
    Backend -- Sync Ops --> DB;
    Backend -- Enqueues Job --> Redis;
    Worker -- Dequeues Job --> Redis;
    Worker -- Heavy Processing --> AI_Models[Local AI Models<br/>(XLM-R, KeyBERT)];
    Worker -- Writes Results --> DB;
```

````

#### Architectural Patterns

-   **Monolithic Application, Decoupled State:** The system remains a "simple monolith" in its application logic but decouples its state (database and queue) into managed services. This pattern provides the development simplicity of a monolith while gaining the resilience and data safety of managed services.
-   **Asynchronous Background Processing (Worker Queue):** All long-running tasks are offloaded to background workers. We will implement **multiple priority queues** (e.g., `high`, `default`, `low`) to ensure time-sensitive jobs are not blocked. The system will run **multiple worker processes** concurrently to better utilize server resources and increase throughput.
-   **Optimized Client-Side Polling:** For near real-time updates, the frontend will use polling with **HTTP `ETag` caching**. This allows the backend to return a lightweight `304 Not Modified` status when data has not changed, dramatically reducing unnecessary load and bandwidth.
-   **Component-Based UI:** The frontend will be built using a component-based architecture with React and `shadcn/ui`.
-   **Service Layer (Backend):** The backend will utilize a service layer pattern to separate business logic from the API routing layer.

---

## Section 3: Tech Stack (Final Approved)

#### Technology Stack Table

| Category                 | Technology                               | Version       | Purpose                                                                 | Rationale                                                                                                                            |
| :----------------------- | :--------------------------------------- | :------------ | :---------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------- |
| **Frontend Language**    | TypeScript                               | Latest Stable | Adds static typing to JavaScript for robustness.                        | Explicitly chosen for type safety in the frontend core.                                                                              |
| **Frontend Framework**   | React                                    | Latest Stable | Core UI library for building the component-based interface.             | The foundation of the specified frontend stack.                                                                                      |
| **UI Component Library** | shadcn/ui                                | Latest Stable | Provides accessible, unstyled component primitives.                     | Chosen for accessibility and direct integration with Tailwind. Updates will be managed via a manifest and scripted overwrites.       |
| **CSS Framework**        | Tailwind CSS                             | Latest Stable | Utility-first CSS framework for styling.                                | Explicitly chosen for consistent and rapid UI development.                                                                           |
| **Routing (Frontend)**   | React Router                             | Latest Stable | Handles client-side navigation and role-based views.                    | Specified as the library for client-side routing.                                                                                    |
| **Form Handling**        | React Hook Form + Zod                    | Latest Stable | Manages complex form state and schema-based validation.                 | Chosen for performance and robust validation capabilities.                                                                           |
| **State Management**     | TanStack Query                           | v5            | Manages server state, caching, and data fetching/polling.               | Explicitly chosen to handle server state, avoiding a global state manager.                                                           |
| **Charting**             | Echarts + echarts-wordcloud              | Latest Stable | Renders all data visualizations (bar, line, word cloud).                | Selected for its powerful and versatile charting capabilities.                                                                       |
| **Backend Language**     | Python                                   | 3.11+         | The core language for the API and background worker.                    | The foundation of the specified backend stack.                                                                                       |
| **Backend Framework**    | FastAPI                                  | Latest Stable | High-performance framework for building the REST API.                   | Chosen for speed and type hints. High-I/O endpoints will be targeted for `async` implementation to mitigate bottlenecks.             |
| **API Style**            | REST                                     | N/A           | Standard for client-server communication.                               | Explicitly chosen, with a non-goal of using GraphQL/gRPC.                                                                            |
| **Database**             | MariaDB                                  | 11.x          | Primary relational database for all application data.                   | Chosen as the specific MySQL-compatible variant.                                                                                     |
| **Data Layer / ORM**     | SQLAlchemy + Alembic, PyMySQL            | 2.0 (Sync)    | Provides ORM, schema migrations, and the DB driver.                     | The designated ORM and driver for database interaction, using sync mode for simplicity.                                              |
| **Cache / Queue**        | Redis                                    | 7.x           | In-memory store used as the message broker for RQ.                      | Required dependency for the RQ background job system.                                                                                |
| **Data Processing**      | pandas, openpyxl, WeasyPrint, Pillow     | Latest Stable | Handles CSV/Excel imports, PDF reports, and image processing.           | [cite\_start]The specified libraries for all bulk data, reporting, and output generation tasks[cite: 1854].                          |
| **AI / ML**              | Gemini API, Transformers, Torch, KeyBERT | Latest Stable | Hybrid model: Gemini API for suggestions, local libraries for analysis. | Uses an external API for suggestion generation to reduce server load. Local models are retained for core sentiment/keyword analysis. |
| **Authentication**       | JWT + PyOTP, passlib[bcrypt]             | Latest Stable | Manages user sessions, password hashing, and Super Admin MFA.           | Specified for secure, stateless authentication and TOTP.                                                                             |
| **Frontend Testing**     | Vitest / RTL                             | Latest Stable | Unit and component testing for the React frontend.                      | Inferred from the standard Vite + React ecosystem and project structure.                                                             |
| **Backend Testing**      | Pytest, pytest-cov, fakeredis, pypdf     | Latest Stable | Testing framework, coverage, and mocking for the backend.               | [cite\_start]Standard Python testing stack with tools for mocking Redis and validating PDFs[cite: 1854].                             |
| **E2E Testing**          | Selenium                                 | Latest Stable | Browser automation for end-to-end workflow validation.                  | [cite\_start]Specified as the tool for cross-service tests[cite: 1854].                                                              |
| **Build Tool / Bundler** | Vite                                     | Latest Stable | Fast development server and production build tool for the frontend.     | Explicitly chosen for frontend development performance.                                                                              |
| **IaC / Orchestration**  | Docker Compose                           | Latest Stable | Defines and runs the multi-container application services.              | Specified as the core tool for local development and VPS deployment. Worker containers will have resource limits enforced.           |
| **Reverse Proxy**        | Caddy                                    | Latest Stable | Handles ingress, routing, and automatic HTTPS for all services.         | Chosen for its simplicity and automatic TLS certificate management.                                                                  |
| **CI / CD**              | GitHub Actions                           | N/A           | Automates testing and deployment workflows.                             | Inferred from the `.github/workflows` directory in the project structure.                                                            |

---

## Section 4: Data Models (Final Verified Version)

This section defines the core data models for the system, derived from the provided Data Dictionary.

#### 0) Conventions & Principles

**Naming**
- Primary keys: `snake_case_id` (e.g., `evaluation_period_id`).
- Foreign keys mirror the source PK name (e.g., `university_registration_request_id`).
- Timestamps: every table has `created_at`, `updated_at`; use `deleted_at` when soft delete semantics exist.

**MySQL/MariaDB enforcement**
- Emulate partial-unique constraints via **generated columns + UNIQUE**.
- Use CHECK constraints if supported by target engine/version; otherwise enforce with triggers or service layer.
- Prefer **explicit invariants** here; validate complex cross-entity rules in service layer and materialized views.

**Privacy & compliance**
- Raw text answers remain in restricted tables; the UI reads only redacted/published projections.
- Aggregation/analytics use eligibility views to avoid drift and protect anonymity.

---

#### 1) Domain Map

1. **University Onboarding & Tenancy**
   - `university_registration_requests`, `university_registration_actions`, `university_registration_documents`, `universities`.
2. **Identity, Roles & Departments**
   - `users`, `user_roles`, `user_department_assignments`, (optionally `super_admins`).
3. **Academic Structure & Offerings**
   - `programs`, `subjects`, `program_subjects`, `subject_departments`, `school_terms`, `subject_offerings`, `student_enrollments`, `subject_offering_faculty_history`.
4. **Evaluation Authoring (Forms)**
   - `likert_scale_templates`, `evaluation_form_templates`, `evaluation_criteria`, `evaluation_questions`.
5. **Evaluation Periods & Forms** *(new parent model)*
   - **Parent**: `evaluation_periods` (supports **scheduled** periods)
   - **Child**: `evaluation_period_forms` (per-audience: student / department_head)
6. **Submissions & Answers**
   - `evaluation_submissions`, `evaluation_likert_answers`, `evaluation_text_answers` (renamed from open-ended).
7. **Qualitative (NLP) & Publication**
   - `text_answer_sentiments`, `text_answer_keywords`, `evaluation_text_answers_published` (job-maintained redaction table).
8. **Flags & Resubmission**
   - `flagged_evaluations`, `flagged_reasons`, `resubmission_windows`.
9. **Aggregates, Snapshots & Jobs**
   - `numerical_aggregates`, `sentiment_aggregates`, final snapshot tables; `background_jobs`.
10. **Notifications**
   - `notifications` (FE inbox, unread counts, deep links).

---

#### 2) Cross-cutting Invariants (summary)

- **One active evaluation period per university**; `active` and `cancelling` are mutually exclusive with any other active/"cancelling" period. **Scheduled** periods are allowed in the future (multiple allowed).
- **Two audience templates max per period**: one for `student`, one for `department_head`. The legacy `both` semantics are removed.
- **Students** submit per **enrolled subject offering** they take with a given faculty; **department heads** submit per **faculty member within their department** (not tied to a specific subject offering).
- **One submission per evaluator × target × role × period** (detailed below).
- **Open-ended → Text** rename is canonical; FE reads only **Published** redacted text (anonymity threshold ≥ 3).
- **Flags & resubmission** exclude submissions from aggregates until resolved; `resubmission_windows` enforce the 48h grace.
- **Hybrid reporting**: live views/caches for day-to-day; immutable snapshots at finalization for reproducibility.

---

#### 3) University Onboarding & Tenancy

##### 3.1 Tables & Purpose
- **University_Registration_Requests** — inbound tenant onboarding requests.
- **University_Registration_Actions** — reviewer actions/locks for a given request; **exactly one active lock** at any time.
- **University_Registration_Documents** — artifacts uploaded during review.
- **Universities** — tenant record (contact details, branding, status).

##### 3.2 Keys & Constraints
- **Canonical FK/PK**: use `university_registration_request_id` everywhere (requests, actions, documents, and `universities`).
- **Global uniqueness**: `universities.contact_university_email` is globally unique.
- **One-active-lock**: generated column + UNIQUE on actions:
  `active_lock_key := CASE WHEN is_active THEN university_registration_request_id END`.

---

#### 4) Identity, Roles & Departments

##### 4.1 Users
- **Status enum**: `{active, archived, suspended}` only.
  *Auth:* only `active` may log in. Consider `archived_reason`, `archived_reason_notes`, `archived_at` for auditability.

##### 4.2 Roles & Tenure
- **User_Roles** — multi-role (e.g., faculty, department_head); uniqueness for active role per user.
- **User_Department_Assignments** — add `user_role_id` (FK→`user_roles`), `started_at`, `ended_at` to record tenure (who/when someone served as department head/faculty in a department).
  *Policy (v1):* multiple faculty in a department allowed; one head enforced by service logic (DB uniqueness can be added later if required).

##### 4.3 Registration Codes (Invites)
- Rename *Tokens* → **User_Registration_Codes**.
- Columns: `intended_role`, `max_uses`, `used_count`, `status (active/inactive)`, expiry, created_by.
- **Traceability**: `users.registration_code_id` FK.
- **Atomic usage**: single guarded `UPDATE` (status active, not expired, `used_count < max_uses`).

---

#### 5) Academic Structure & Offerings

- **School_Terms**: `UNIQUE(university_id, start_school_year, end_school_year, semester)`; `start <= end`.
- **Subject_Offerings**: may have optional `program_id` (for GE/cross-listed).
- **Faculty change history**: trigger on `subject_offerings.faculty_user_id` updates → append to `subject_offering_faculty_history`.
- **Student_Enrollments**: add optional `drop_reason` enum, `drop_reason_notes`, `dropped_at` for reporting.

---

#### 6) Evaluation Authoring (Forms)

- **Evaluation_Form_Templates**: lifecycle `draft ↔ active → assigned`; `assigned` = locked; editing an `active` template that fails validation reverts it to `draft`.
- **Evaluation_Questions**: types include `likert` and **`text`** (renamed from `open_ended`).

---

#### 7) Evaluation Periods & Forms (Parent/Child)

##### 7.1 Evaluation_Periods (Parent)
- **Status enum**: `scheduled | active | cancelling | cancelled | archived`.
  - *Scheduled*: allows admins to **create future periods** ahead of time.
  - *Active*: counting towards aggregates; submissions accepted.
  - *Cancelling*: transitional; async invalidation job in progress; blocks creating another active period.
  - *Cancelled*: closed, excluded from aggregates.
  - *Archived*: ended normally; stays included.
- **One-active invariant**: generated column + UNIQUE across `(university_id)` when status in `{active, cancelling}`.
  *Note*: Multiple `scheduled` periods are allowed for planning. Service validation can warn about time overlaps, but overlaps are permitted by DB (admin override possible).
- **Window constraints**: `starts_at < ends_at`; optional trigger to hard-enforce.

##### 7.2 Evaluation_Period_Forms (Child)
- Per-period, per-audience form assignment.
- **evaluator_role**: `student` | `department_head` (no `both`).
- **Uniqueness**: `UNIQUE(evaluation_period_id, evaluator_role)`.
- **Status**: mirror parent (`active/archived/cancelling/cancelled`); `scheduled` not required here—the parent controls timing.

---

#### 8) Submissions & Eligibility

##### 8.1 Evaluation_Submissions (unified model)
**Key columns**
- `evaluation_period_id` (FK), `evaluator_role` (`student`|`department_head`), `evaluator_user_id`.
- Target identity:
  - **Student route**: `subject_offering_id` (NOT NULL), and `evaluated_faculty_user_id` (derived from offering at submit-time, stored for denormalized joins & snapshots).
  - **Department-head route**: `department_id` (NOT NULL), and `evaluated_faculty_user_id` (explicit target within that department).
- Timing: `evaluation_start_time`, `evaluation_end_time` (supports configurable min-seconds “nudge”).

**Submission uniqueness**
- **Students**: one per `(evaluation_period_id, evaluator_role='student', subject_offering_id, evaluator_user_id)`.
- **Dept Heads**: one per `(evaluation_period_id, evaluator_role='department_head', evaluated_faculty_user_id, evaluator_user_id)`.

**Integrity checks** *(DB or service-layer)*
- **Student route**: evaluator must be **enrolled** in `subject_offering_id` for the period’s time window; the offering’s `faculty_user_id` must equal `evaluated_faculty_user_id` at the time of submission (history table ensures traceability if faculty changed mid-term).
- **Dept head route**: evaluator must hold an **active department_head** role in `department_id` during the period window; `evaluated_faculty_user_id` must be an **active faculty** in the same department during that window.
- **Role-target guard**: CHECK or trigger to enforce:
  - if `evaluator_role = 'student'` → `subject_offering_id IS NOT NULL` and `department_id IS NULL`.
  - if `evaluator_role = 'department_head'` → `department_id IS NOT NULL` and `subject_offering_id IS NULL`.

##### 8.2 Answers
- **Likert**: `UNIQUE(submission_id, question_id)`.
- **Text** *(renamed)*: `evaluation_text_answers(text_answer_id, text_response)`; `UNIQUE(submission_id, question_id)`.

---

#### 9) Qualitative (NLP) & Publication

- **Sentiments / Keywords**: rename to `text_answer_sentiments`, `text_answer_keywords` (FK → `evaluation_text_answers.text_answer_id`).
- **Published text answers (UI-facing)**: `evaluation_text_answers_published` materialized by job.
  - Only publish when the **anonymity threshold ≥ 3** for the relevant cohort.
  - Store `redacted_text`, `cohort_response_count`, linkage to `evaluation_period_id` & `question_id` (& `text_answer_id` for provenance).
  - FE **never** reads raw answers.

---

#### 10) Flags & Resubmission

- **Flagged_Evaluations.status**: `{pending, approved, archived, resubmission_requested}`.
- **Resubmission_Windows**: one per `submission_id`, with `window_starts_at`, `window_ends_at = +48h`.
- **Aggregate eligibility**: flagged `pending` or `resubmission_requested` and submissions under `cancelled` periods are excluded from all views/aggregations until resolved.

---

#### 11) Aggregates, Snapshots & Jobs

- **Eligibility views**: centralize rules for inclusion (status, period state, anonymity threshold). All live dashboards read from these views; caches hydrate from them.
- **Finalization**: produce immutable **snapshot tables** (e.g., `*_final_snapshots`) when a period is finalized; reports/CSVs/PDFs draw from snapshots.
- **Cancellation**: background job transitions `active → cancelling → cancelled`, invalidates caches and any provisional aggregates derived from that period.

---

#### 12) Notifications

- Use existing `notifications` table; add `context_type/context_id` later if needed for deep links to flags/resubmissions.
- AI suggestion notifications are visible only to faculty & department heads (service-level enforcement; optional DB CHECK by type if/when typed).

---

#### 13) DB Patterns & Example Keys (MySQL/MariaDB)

- **One-active reviewer lock** (registration actions):
  `active_lock_key := CASE WHEN is_active THEN university_registration_request_id END`  → `UNIQUE(active_lock_key)`
- **One-active evaluation period per university** (allow multiple scheduled):
  `active_period_key := CASE WHEN status IN ('active','cancelling') THEN university_id END`  → `UNIQUE(active_period_key)`
- **Per-audience form**: `UNIQUE(evaluation_period_id, evaluator_role)`
- **Student submission uniqueness**: `UNIQUE(evaluation_period_id, evaluator_role, subject_offering_id, evaluator_user_id)`
- **Dept-head submission uniqueness**: `UNIQUE(evaluation_period_id, evaluator_role, evaluated_faculty_user_id, evaluator_user_id)`

---

#### 14) Differences vs. Prior Baseline (quick diff)

- **New parent** `evaluation_periods` with **scheduled** status added; legacy `both` evaluator_role removed.
- **Split** child `evaluation_period_forms` per audience (student/department_head).
- **Users.status** reduced to `{active, archived, suspended}`; old `inactive/locked` removed.
- **User_Department_Assignments** gains `user_role_id`, `started_at`, `ended_at` for tenure.
- **Open-ended → Text** rename + cascades; **Published** redacted table added; FE reads published only.
- **Enrollment** adds `drop_reason`, `drop_reason_notes`, `dropped_at`.
- **Flags** enum aligned; **Resubmission_Windows** added.
- **Universities** enforces global uniqueness on `contact_university_email`.
- **Reviewer locks** enforced via generated-column unique.

---

#### 15) Future-proofing Notes

- If a third evaluator type appears (e.g., peer/self), extend `evaluation_period_forms` with a new `evaluator_role` value and replicate the submission uniqueness pattern for that role.
- If the institution requires DB-level enforcement of **one department head per department**, add a generated-column unique keyed on `(department_id)` when the corresponding `user_role_id` denotes `department_head` and the assignment is active.
- Consider a materialized **evaluation_eligibilities** table per period for large cohorts to accelerate FE pickers and server validation (precomputed join of enrolled students×offerings and department_head×faculty-in-department). The service can rely on this table for quick eligibility checks.

---

#### 16) Handoff Checklist (for Dev & QA)

- Migrations aligned with the change set (Step B): ensure renames, new tables, and uniqueness keys exist.
- Access control: raw vs. published answers; snapshot immutability.
- FE/BE contract: submission payloads differ by role (student vs dept-head).
  - Student: `{ period_id, role: 'student', subject_offering_id }` → server derives & stores `evaluated_faculty_user_id`.
  - Dept-head: `{ period_id, role: 'department_head', department_id, evaluated_faculty_user_id }`.
- Jobs: redaction/publish, period cancellation, finalize-to-snapshot, cache invalidation.
- Views: eligibility views power analytics and must exclude ineligible rows.

```

This document now contains our complete work on the architecture up to this point. We need to do a recheck of the Data Models as it is possibly missing other key tables, attributes in alignment and correlation with the current database structure or schema; however, there should be newer tables or models due to newly made decisions on both prd.md and front-end-spec.md; those should be properly checked and strictly verified against to.
```
````
