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

### Core Tenant and User Models

#### Model: University

-   **Purpose:** The authoritative table for all onboarded institutions, serving as the primary tenant record.
-   **Key Attributes:**
    -   [cite\_start]`university_id` (int, PK): Unique identifier for the university[cite: 1514].
    -   [cite\_start]`registration_request_id` (int, FK): A link to the original, approved onboarding request for audit purposes[cite: 1514].
    -   [cite\_start]`university_name` (varchar, Not Null): Official full name of the university[cite: 1514].
    -   [cite\_start]`acronym` (varchar): Optional shortcode for the university (e.g., UCLM)[cite: 1514].
    -   [cite\_start]`contact_university_email` (varchar, Not Null): The official contact email for the institution[cite: 1515].
    -   [cite\_start]`city` (varchar, Not Null): The city where the university is located[cite: 1515].
    -   [cite\_start]`logo_path` (varchar): The path to the university's logo for branding the UI[cite: 1515].
    -   [cite\_start]`status` (enum): The university's current operational status (e.g., 'active', 'inactive')[cite: 1515].

#### Model: User

-   **Purpose:** The central repository for all individuals who interact with the system within a university context.
-   **Key Attributes:**
    -   [cite\_start]`user_id` (int, PK): Unique identifier for each user[cite: 1574].
    -   [cite\_start]`university_id` (int, FK): Links the user to their institution, enforcing tenancy[cite: 1574].
    -   [cite\_start]`school_id` (varchar, Not Null): The official, university-issued ID number, unique within the university[cite: 1574].
    -   [cite\_start]`username` (varchar, Not Null): The user's editable login username, unique within the university[cite: 1575].
    -   [cite\_start]`email` (varchar, Not Null, Unique): The user's email, unique across the entire system[cite: 1575].
    -   [cite\_start]`password_hash` (varchar, Not Null): Hashed password for secure authentication[cite: 1575].
    -   [cite\_start]`admin_pin_code_hash` (varchar, Null): A secondary hashed PIN for admins, providing an extra security layer[cite: 1575].
    -   [cite\_start]`last_name` (varchar, Not Null): The user's last name[cite: 1575].
    -   [cite\_start]`first_name` (varchar, Not Null): The user's first name[cite: 1575].
    -   [cite\_start]`profile_photo_path` (varchar): Path to the user's profile photo for the UI[cite: 1575].
    -   [cite\_start]`email_verified` (boolean): A flag indicating if the user has verified their email address[cite: 1575].
    -   [cite\_start]`status` (enum): The user's account status (e.g., 'active', 'inactive', 'suspended')[cite: 1575].

#### Model: SuperAdmin

-   **Purpose:** Stores information for system-wide administrators who are separate from any university-specific tenant.
-   **Key Attributes:**
    -   [cite\_start]`super_admin_id` (int, PK): Unique identifier for each super admin[cite: 1597].
    -   [cite\_start]`username` (varchar, Not Null, Unique): The super admin's login username[cite: 1597].
    -   [cite\_start]`email` (varchar, Not Null, Unique): The super admin's email, unique globally[cite: 1597].
    -   [cite\_start]`password_hash` (varchar, Not Null): Hashed password for secure authentication[cite: 1598].
    -   [cite\_start]`super_admin_pin_code_hash` (varchar, Not Null): A secondary hashed PIN for multi-factor authentication[cite: 1598].
    -   [cite\_start]`last_name` (varchar, Not Null): The super admin's last name[cite: 1598].
    -   [cite\_start]`first_name` (varchar, Not Null): The super admin's first name[cite: 1598].
    -   [cite\_start]`profile_photo_path` (varchar): Path to the super admin's profile photo[cite: 1598].
    -   [cite\_start]`status` (enum): The super admin's account status (e.g., 'active', 'locked')[cite: 1598].

### Academic Structure Models

#### Model: Department

-   **Purpose:** Defines the academic departments within a university, supporting a hierarchical structure.
-   **Key Attributes:**
    -   [cite\_start]`department_id` (int, PK): Unique identifier for the department[cite: 1522].
    -   [cite\_start]`university_id` (int, FK): Links the department to its university[cite: 1522].
    -   [cite\_start]`parent_department_id` (int, FK): Self-referencing key to establish hierarchy[cite: 1522].
    -   [cite\_start]`department_head_id` (int, FK): Links to the `User` who is the current head of the department[cite: 1522].
    -   [cite\_start]`department_name` (varchar, Not Null): The official name of the department[cite: 1522].
    -   [cite\_start]`acronym` (varchar): The optional acronym for the department, useful for display in the UI[cite: 1522].
    -   [cite\_start]`is_active` (boolean): A flag for soft deletion or archiving[cite: 1523].

#### Model: SchoolTerm

-   **Purpose:** Defines a university's distinct academic periods.
-   **Key Attributes:**
    -   [cite\_start]`school_term_id` (int, PK): Unique identifier for the term[cite: 1532].
    -   [cite\_start]`university_id` (int, FK): Links the term to its university[cite: 1532].
    -   [cite\_start]`start_school_year` (int, Not Null): The academic starting year (e.g., 2025)[cite: 1532].
    -   [cite\_start]`end_school_year` (int, Not Null): The academic ending year (e.g., 2026)[cite: 1533].
    -   [cite\_start]`semester` (enum): The specific semester ('1st semester', '2nd semester', 'Summer')[cite: 1533].
    -   [cite\_start]`start_date` (date): The optional, specific start date of the term[cite: 1533].
    -   [cite\_start]`end_date` (date): The optional, specific end date of the term[cite: 1533].
    -   [cite\_start]`is_active` (boolean): A flag for archiving past terms[cite: 1533].

#### Model: Program

-   **Purpose:** Catalogs all academic programs, courses, tracks, and grade levels offered by the university.
-   **Key Attributes:**
    -   [cite\_start]`program_id` (int, PK): Unique identifier for the program[cite: 1610].
    -   [cite\_start]`university_id` (int, FK): The university this program belongs to, critical for tenancy[cite: 1610].
    -   [cite\_start]`department_id` (int, FK): The department that owns or manages this program[cite: 1611].
    -   [cite\_start]`program_code` (varchar, Not Null): The university's unique code for the program (e.g., "BSIT")[cite: 1611].
    -   [cite\_start]`program_name` (varchar, Not Null): The official name of the program[cite: 1611].
    -   [cite\_start]`program_level` (enum): The educational stage ('basic education', 'senior_high', 'college', 'graduate')[cite: 1611].
    -   [cite\_start]`is_active` (boolean): Active/archive flag[cite: 1611].

#### Model: Subject

-   **Purpose:** Stores the definitions of all subjects (e.g., courses, classes) offered by the university.
-   **Key Attributes:**
    -   [cite\_start]`subject_id` (int, PK): Unique identifier for the subject[cite: 1618].
    -   [cite\_start]`university_id` (int, FK): Links the subject to its university, enforcing tenancy[cite: 1618].
    -   [cite\_start]`subject_code` (varchar, Not Null): The unique code for the subject (e.g., "IT-101"), unique per university[cite: 1619].
    -   [cite\_start]`name` (varchar, Not Null): The official title of the subject (e.g., "Calculus 1")[cite: 1619].
    -   [cite\_start]`units` (int): Number of academic units or credits[cite: 1619].
    -   [cite\_start]`is_active` (boolean): Active/archive flag[cite: 1619].

### Evaluation Setup Models

#### Model: LikertScaleTemplate

-   **Purpose:** Defines the institution's reusable Likert scales to ensure consistency.
-   **Key Attributes:**
    -   [cite\_start]`likert_scale_template_id` (int, PK): Unique identifier for the scale[cite: 1684].
    -   [cite\_start]`likert_name` (varchar, Not Null): A descriptive name for the scale (e.g., "Standard 1-5 Scale")[cite: 1684].
    -   [cite\_start]`min_value` (tinyint, Not Null): The minimum value of the scale (e.g., 1)[cite: 1684].
    -   [cite\_start]`max_value` (tinyint, Not Null): The maximum value of the scale (e.g., 5)[cite: 1684].

#### Model: EvaluationFormTemplate

-   **Purpose:** Stores the master templates for evaluation forms.
-   **Key Attributes:**
    -   [cite\_start]`form_template_id` (int, PK): Unique identifier for the template[cite: 1677].
    -   [cite\_start]`university_id` (int, FK): Scopes the template to a specific university[cite: 1677].
    -   [cite\_start]`name` (varchar, Not Null): The admin-defined name for the template[cite: 1677].
    -   [cite\_start]`description` (text): Optional details or notes about the form's purpose[cite: 1677].
    -   [cite\_start]`instructions` (text): Custom instructions displayed to the evaluator at the start of the form[cite: 1677].
    -   [cite\_start]`likert_scale_template_id` (int, FK): Defines the Likert scale used for numerical questions on this form[cite: 1677].
    -   [cite\_start]`status` (enum): The template's current lifecycle state ('draft', 'active', 'assigned', 'archived')[cite: 1677].

#### Model: EvaluationCriterion

-   **Purpose:** Represents a distinct, weighted section within an evaluation form template.
-   **Key Attributes:**
    -   [cite\_start]`evaluation_criteria_id` (int, PK): Unique identifier for the criterion[cite: 1693].
    -   [cite\_start]`form_template_id` (int, FK): Links the criterion to its parent form template[cite: 1696].
    -   [cite\_start]`criterion_name` (varchar, Not Null): The title of the section[cite: 1700].
    -   [cite\_start]`criterion_description` (text): Optional further explanation for evaluators[cite: 1704].
    -   [cite\_start]`weight` (decimal, Not Null): The percentage weight of this criterion in the final score calculation[cite: 1707].
    -   [cite\_start]`order` (int, Not Null): The display order of this criterion within the form[cite: 1709, 1713].

#### Model: EvaluationQuestion

-   **Purpose:** Stores the individual questions, supporting both Likert-scale and open-ended questions.
-   **Key Attributes:**
    -   [cite\_start]`question_id` (int, PK): Unique identifier for the question[cite: 1721].
    -   `criterion_id` (int, FK): Links a Likert-scale question to its parent criterion. [cite\_start]`NULL` for open-ended questions[cite: 1722].
    -   [cite\_start]`question_text` (varchar, Not Null): The text of the question prompt[cite: 1722].
    -   [cite\_start]`question_type` (enum): The type of question ('likert' or 'open_ended')[cite: 1722].
    -   [cite\_start]`is_required` (boolean): Specifies if an answer is mandatory[cite: 1722].
    -   [cite\_start]`is_active` (boolean): Archive flag for soft-deleting questions[cite: 1722].

#### Model: EvaluationFormAssignment (Evaluation Period)

-   **Purpose:** Activates an evaluation by linking a form template to an academic term and assessment period.
-   **Key Attributes:**
    -   [cite\_start]`form_assignment_id` (int, PK): Unique identifier for this scheduled period[cite: 1730].
    -   [cite\_start]`university_id` (int, FK): The university this assignment applies to, for tenancy[cite: 1730].
    -   [cite\_start]`school_term_id` (int, FK): The academic term this period belongs to[cite: 1731].
    -   [cite\_start]`assessment_period` (enum): The portion of the term being evaluated ('midterm' or 'finals')[cite: 1731].
    -   [cite\_start]`form_template_id` (int, FK): The specific form template to be used[cite: 1731].
    -   [cite\_start]`evaluator_role` (enum): Specifies who this assignment is for ('student', 'department_head', or 'both')[cite: 1731].
    -   [cite\_start]`start_date_time` (timestamp, Not Null): The precise moment the evaluation becomes available[cite: 1731].
    -   [cite\_start]`end_date_time` (timestamp, Not Null): The precise moment the evaluation closes[cite: 1731].
    -   [cite\_start]`status` (enum): The status of the assignment ('active' or 'archived')[cite: 1731].

### Evaluation Submission & Flagging Models

#### Model: EvaluationSubmission

-   **Purpose:** The central "session" table for an evaluation, linking the evaluator, the subject, and the evaluation period.
-   **Key Attributes:**
    -   [cite\_start]`submission_id` (int, PK): Unique identifier for this submission session[cite: 1759].
    -   [cite\_start]`evaluator_user_id` (int, FK): The user submitting the evaluation[cite: 1760].
    -   [cite\_start]`subject_offering_id` (int, FK): The specific class or subject offering being evaluated[cite: 1760].
    -   [cite\_start]`form_assignment_id` (int, FK): The active evaluation period this submission belongs to[cite: 1760].
    -   [cite\_start]`evaluation_start_time` (timestamp, Not Null): Timestamp when the user begins the evaluation[cite: 1760].
    -   [cite\_start]`evaluation_end_time` (timestamp, Nullable): Timestamp when the user submits the evaluation[cite: 1760].
    -   [cite\_start]`status` (enum): The lifecycle status of the submission ('pending', 'submitted')[cite: 1760].

#### Model: EvaluationLikertAnswer

-   **Purpose:** Stores a single numerical answer to a Likert-scale question for a specific submission.
-   **Key Attributes:**
    -   [cite\_start]`likert_answer_id` (int, PK): Unique identifier for the answer[cite: 1742].
    -   [cite\_start]`submission_id` (int, FK): Links this answer to its parent submission session[cite: 1742].
    -   [cite\_start]`question_id` (int, FK): The specific Likert-scale question being answered[cite: 1742].
    -   [cite\_start]`answer_value` (tinyint, Not Null): The numerical score given by the evaluator[cite: 1742].

#### Model: EvaluationOpenEndedAnswer

-   **Purpose:** Stores a single textual answer to an open-ended question for a specific submission.
-   **Key Attributes:**
    -   [cite\_start]`open_ended_answer_id` (int, PK): Unique identifier for the answer[cite: 1750].
    -   [cite\_start]`submission_id` (int, FK): Links this answer to its parent submission session[cite: 1750].
    -   [cite\_start]`question_id` (int, FK): The specific open-ended question being answered[cite: 1750].
    -   [cite\_start]`open_ended_answer` (text, Not Null): The written feedback from the evaluator[cite: 1750].

#### Model: FlaggedEval

-   **Purpose:** Acts as a case file for a submission that has been flagged for manual administrative review.
-   **Key Attributes:**
    -   [cite\_start]`flagged_evaluation_id` (int, PK): Unique identifier for the flag record[cite: 1833].
    -   [cite\_start]`submission_id` (int, FK): The evaluation submission that was flagged[cite: 1834].
    -   [cite\_start]`flagged_at` (timestamp, Not Null): When the flag was created[cite: 1834].
    -   [cite\_start]`status` (enum): The current review status ('pending', 'reviewed', 'resolved', 'ignored')[cite: 1834].
    -   [cite\_start]`reviewed_by_user_id` (int, FK): The admin who reviewed the flag[cite: 1834].
    -   [cite\_start]`resolution_notes` (text): The admin's notes on why a certain resolution was chosen[cite: 1834].

#### Model: FlaggedReason

-   **Purpose:** Stores the specific, machine-readable reasons why a submission was flagged.
-   **Key Attributes:**
    -   [cite\_start]`flagged_reason_id` (int, PK): Unique identifier for the reason record[cite: 1841].
    -   [cite\_start]`flagged_evaluation_id` (int, FK): The parent flagged evaluation case[cite: 1841].
    -   [cite\_start]`reason_code` (varchar, Not Null): A short, machine-readable code for the flag type[cite: 1841].
    -   [cite\_start]`reason_description` (text, Not Null): A detailed, human-readable explanation of the flag[cite: 1841].

### Analysis, AI, and Notifications Models

#### Model: NumericalAggregate & SentimentAggregate

-   **Purpose:** The primary summary tables designed for fast dashboard reads, storing pre-calculated and normalized scores.
-   **Key Attributes (`NumericalAggregate`):**
    -   [cite\_start]**Composite Primary Key:** Includes `university_id`, `school_term_id`, `faculty_user_id`, and `calc_run_id`[cite: 1792].
    -   [cite\_start]`n_valid_numeric` (int): Count of usable Likert answers processed, for data quality analysis[cite: 1787].
    -   [cite\_start]`quant_score_raw` (decimal): The raw weighted score before normalization[cite: 1787].
    -   [cite\_start]`cohort_n` (int): The number of results used to compute the cohort baseline, for statistical context[cite: 1788].
    -   [cite\_start]**`mu_quant` (decimal): The mean score of the comparison cohort (μ)**[cite: 1787].
    -   [cite\_start]**`sigma_quant` (decimal): The standard deviation of the comparison cohort (σ)**[cite: 1787].
    -   [cite\_start]`z_quant` (decimal): The normalized quantitative z-score (`(raw_score - μ) / σ`)[cite: 1788].
    -   [cite\_start]`final_score_60_40` (decimal): The final blended score (60% quantitative, 40% qualitative)[cite: 1788].
    -   [cite\_start]`is_final_snapshot` (boolean): Flag that freezes this record when the period is locked[cite: 1789].
-   **Key Attributes (`SentimentAggregate`):**
    -   [cite\_start]**Composite Primary Key:** Same as `NumericalAggregate`[cite: 1814].
    -   [cite\_start]`n_valid_comments` (int): Count of comments successfully analyzed[cite: 1801].
    -   [cite\_start]`qual_score_raw` (decimal): A single index summarizing overall sentiment[cite: 1802].
    -   [cite\_start]`cohort_n` (int): The number of results in the qualitative cohort[cite: 1803].
    -   [cite\_start]**`mu_qual` (decimal): The mean qualitative score of the comparison cohort (μ)**[cite: 1802].
    -   [cite\_start]**`sigma_qual` (decimal): The standard deviation of the qualitative cohort (σ)**[cite: 1802].
    -   [cite\_start]`z_qual` (decimal): The normalized qualitative z-score[cite: 1803].
    -   [cite\_start]`prevailing_label` (enum): The dominant sentiment[cite: 1802].

#### Model: UserRegistrationToken

-   **Purpose:** Manages invite/cohort tokens for controlled self-service user onboarding.
-   **Key Attributes:**
    -   [cite\_start]`registration_token_id` (int, PK): Unique identifier for the token record[cite: 1542].
    -   [cite\_start]`university_id` (int, FK): Scopes the token to a specific university[cite: 1542].
    -   [cite\_start]`token_hash` (char(64), Not Null): The SHA-256 hash of the raw token[cite: 1542].
    -   [cite\_start]`intended_role` (enum, Not Null): The user role this token is valid for[cite: 1542].
    -   [cite\_start]`max_uses` (int, Not Null): The maximum number of times this token can be used[cite: 1543].
    -   [cite\_start]`used_count` (int, Not Null): The current number of times the token has been consumed[cite: 1543].

#### Model: AISuggestion

-   **Purpose:** Stores the historical output from the "AI Assistant," allowing users to review their generated insights over time.
-   **Key Attributes:**
    -   [cite\_start]`suggestion_id` (int, PK): Unique ID for the saved suggestion[cite: 1825].
    -   [cite\_start]`university_id` (int, FK): The university tenant for data scoping[cite: 1825].
    -   [cite\_start]`user_id` (int, FK): The user who generated and saved the suggestion[cite: 1825].
    -   [cite\_start]`improvement_area` (varchar, Not Null): The specific area targeted for improvement[cite: 1826].
    -   [cite\_start]`suggestion_text` (text, Not Null): The full text of the AI-generated suggestion[cite: 1826].

#### Model: Notification

-   **Purpose:** Stores system-generated, user-specific notifications for display in the UI.
-   **Key Attributes:**
    -   [cite\_start]`notification_id` (int, PK): Unique ID for the notification[cite: 1848].
    -   [cite\_start]`user_id` (int, FK): The recipient of the notification[cite: 1848].
    -   [cite\_start]`notification_type` (varchar): A machine-readable code for the type of notification[cite: 1848].
    -   [cite\_start]`content` (text, Not Null): The human-readable message[cite: 1848].
    -   [cite\_start]`read_at` (timestamp, Nullable): Timestamp indicating when the user marked the notification as read[cite: 1848].

<!-- end list -->

```

This document now contains our complete work on the architecture up to this point. We need to do a recheck of the Data Models as it is possibly missing other key tables, attributes in alignment and correlation with the current database structure or schema; however, there should be newer tables or models due to newly made decisions on both prd.md and front-end-spec.md; those should be properly checked and strictly verified against to.
```
````
