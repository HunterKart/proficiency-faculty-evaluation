## **Components**

This section breaks down the **Proficiency** platform into its primary logical components. The components are organized into functional groups that align with the core domains of the application. Each component's responsibility, interfaces, dependencies, and core technologies are defined to provide a clear blueprint for implementation.

### **Group 1: Core Platform & Tenancy Services**

This group defines the foundational, cross-cutting components that enable the multi-tenant platform to operate. This includes user identity, authentication, notifications, and the top-level administrative functions for managing tenants.

#### **`[Frontend]` Application Shell**

* **Responsibility:** Serves as the main layout container for the authenticated user experience. It holds the persistent elements like the collapsible sidebar navigation, the main header, and the content area where individual pages are rendered. It also manages the root-level application state, such as the current user's session.
* **Key Interfaces:** A root-level React component that utilizes `React Router` to render child routes. It will expose a context or state hook for child components to interact with global UI elements (e.g., toggling the sidebar).
* **Dependencies:** `React Router`, `Authentication Service` (via a global auth hook), `Notification Center`.
* **Technology Stack:** React, TypeScript, Tailwind CSS, `shadcn/ui` (for layout primitives), `lucide-react` (for icons).

#### **`[Frontend]` Authentication Components**

* **Responsibility:** Manages the entire user-facing authentication lifecycle. This includes the distinct login forms for regular users and Super Admins, the multi-step university registration process, and the user's own profile management and password change forms.
* **Key Interfaces:** A set of pages/routes including `/login`, `/register`, `/super-admin/login`, and `/profile`. It will consist of components such as `LoginForm`, `RegistrationForm`, and `UserProfileForm`.
* **Dependencies:** `Authentication Service [Backend]`, `React Hook Form` & `Zod` (for robust client-side validation), `TanStack Query` (for handling API mutations like login and registration).
* **Technology Stack:** React, TypeScript, React Hook Form, Zod, TanStack Query, `shadcn/ui` (for forms, inputs, buttons).

#### **`[Frontend]` Notification Center**

* **Responsibility:** **Subscribes** to a WebSocket channel to receive live events from backend services. It is responsible for displaying real-time, in-app notifications to the user and managing their read/unread status. It must provide an immediate visual indicator when a new notification arrives without requiring a page refresh.
* **Key Interfaces:** A `NotificationPanel` component, rendered within the `Application Shell`, which displays a list of `NotificationItem` components.
* **Dependencies:** A WebSocket connection for receiving real-time events, and the `Notification Service [Backend]` for fetching historical notifications and updating their status via REST API calls.
* **Technology Stack:** React, TypeScript, `shadcn/ui` (Dropdown Menu or Sheet), `lucide-react` (icons).

#### **`[Frontend]` Super Admin Module**

* **Responsibility:** Provides the complete user interface for Super Admins to manage the university onboarding lifecycle and perform essential user management for tenants.
* **Key Interfaces:** A suite of components rendered under the `/super-admin/*` route prefix, including the `UniversityRequestBoard` (Kanban), `UniversityDetailsView`, and `TenantUserManagementTable`.
* **Dependencies:** `University Onboarding Service [Backend]` and `User & Role Service [Backend]` via API calls. It will heavily utilize `TanStack Query` for fetching, caching, and invalidating data to ensure the UI stays in sync.
* **Technology Stack:** React, TypeScript, TanStack Query, `shadcn/ui` (Table, Dialog, Card).

#### **`[Backend]` Authentication Service**

* **Responsibility**: Manages all security-critical logic. This includes credential verification (password hashing with `bcrypt`), multi-factor authentication for Super Admins (`pyotp`), and the generation/validation of stateless JWT access and refresh tokens. It is also responsible for issuing and validating **time-limited, single-use tokens** for actions like account verification and password resets. It handles the token invalidation mechanism via the `tokenVersion` field in the user models.
* **Key Interfaces**: Exposes the API endpoints under `/auth/*` and `/super-admin/login/*` as defined in the API Specification.
* **Dependencies**: `User & Role Service` (to fetch user data), Database (to access `users` and `super_admins` tables).
* **Technology Stack**: Python, FastAPI, SQLAlchemy, `passlib[bcrypt]`, `pyotp`, `python-jose`.

#### **`[Backend]` User & Role Service**

* **Responsibility:** Manages the business logic for user accounts, roles, and profiles. It handles CRUD operations and ensures that actions are authorized based on the user's role and tenancy.
* **Key Interfaces:** Exposes API endpoints such as `GET /profile`, `PUT /profile`, and the tenant-specific user management endpoints for Super Admins.
* **Dependencies:** Database (to interact with `users`, `roles`, and associated tables).
* **Technology Stack:** Python, FastAPI, SQLAlchemy, Pydantic.

#### **`[Backend]` University Onboarding Service**

* **Responsibility:** Manages the entire lifecycle of a `UniversityRegistrationRequest`, from submission to approval or rejection. The approval process, which creates both the `University` and initial `User` records, **must be executed within a single, atomic database transaction** to guarantee data consistency. Subsequent actions, like triggering notifications, are dispatched only after the transaction's successful commit.
* **Key Interfaces:** Exposes the API endpoints under `/super-admin/university-requests/*` and the public `POST /university-requests`. These endpoints should be designed to be **idempotent** where applicable to prevent duplicate actions on retries.
* **Dependencies:** Database, `File Storage` (for uploaded documents), `Notification Service` (to dispatch emails), `Redis` (to enqueue subsequent import jobs if applicable).
* **Technology Stack:** Python, FastAPI, SQLAlchemy, Pydantic.

#### **`[Backend]` Notification Service**

* **Responsibility:** A centralized service for creating, managing, and dispatching notifications. Asynchronous jobs dispatched by this service, especially those triggering external actions like sending emails, **must be designed to be idempotent** and include a retry strategy to handle transient failures. It is also responsible for broadcasting events to the WebSocket channel for real-time client updates.
* **Key Interfaces:** Exposes the `GET /notifications` and `PUT /notifications/{id}/status` API endpoints. Internally, it provides a function like `create_notification()` for other services to call.
* **Dependencies:** Database (`notifications` table), `Redis` (to enqueue email sending jobs), `User & Role Service` (to get recipient details), WebSocket Manager.
* **Technology Stack:** Python, FastAPI, SQLAlchemy, Pydantic, `websockets`.

***

### **Group 2: Academic & Data Management Services**

This group encompasses all components required for University Admins to build out and manage their institution's foundational data, either manually or via bulk import. This group also includes the central job monitoring system, which is critical for observing and managing all asynchronous operations across the platform.

#### **`[Frontend]` Academic Structure Module**

* **Responsibility**: Provides the user interface for University Admins to perform manual Create, Read, Update, and Delete (CRUD) operations on the core academic hierarchy: **Departments**, **Programs**, and **Subjects**. This component is for making granular corrections or additions without needing a full file import.
* **Key Interfaces**: A set of pages under the `/admin/academic-structure/*` route, featuring tables for listing entities and forms (within dialogs or on separate pages) for creating and editing them.
* **Dependencies**: `Academic Structure Service [Backend]`, `TanStack Query`, `shadcn/ui` components.
* **Technology Stack**: React, TypeScript, TanStack Query, `shadcn/ui` (Table, Dialog, Form, Input), React Router.

***

#### **`[Frontend]` Bulk Import Module**

* **Responsibility**: Implements the multi-step wizard UI for uploading, validating, and processing bulk data files (CSV/Excel). It is designed to provide clear, actionable feedback to the Admin, including row-specific error messages if validation fails, ensuring data quality before processing begins.
* **Key Interfaces**: A page at `/admin/bulk-import` that guides the user through file selection, type detection, validation, and a final confirmation step before enqueuing the job.
* **Dependencies**: `Bulk Import Service [Backend]`.
* **Technology Stack**: React, TypeScript, `shadcn/ui` (File Input, Progress Bar, Alert Dialog, Table for displaying errors).

***

#### **`[Frontend]` Job Monitor Module**

* **Responsibility**: A centralized dashboard that provides Admins with a real-time view of all background jobs. It **must implement a resilient WebSocket client** with automatic reconnection logic. Upon reconnection, it must re-fetch the latest job state via a REST call to prevent displaying stale data. It displays job status (including `Completed_Partial_Failure`), progress, and provides actions to manage jobs, such as `Cancel`, `Download Error Report`, and `Force Fail`.
* **Key Interfaces**: A page at `/admin/job-monitor` that establishes and maintains a WebSocket connection. It primarily features a table of all background jobs.
* **Dependencies**: `Job Monitoring Service [Backend]` (via WebSockets for real-time updates and a REST API for initial data load and performing actions).
* **Technology Stack**: React, TypeScript, `shadcn/ui` (Table, Button, Progress Bar, AlertDialog), native WebSocket API.

***

#### **`[Backend]` Academic Structure Service**

* **Responsibility**: Exposes the secure API endpoints for all manual CRUD operations on the academic hierarchy (`Departments`, `Programs`, `Subjects`). This service is responsible for enforcing all business logic, relational constraints, and tenancy rules. It must gracefully handle database errors for violations of **`ON DELETE RESTRICT`** constraints and return a user-friendly `409 Conflict` response.
* **Key Interfaces**: RESTful API endpoints under `/admin/academic-structure/*` (e.g., `POST /admin/academic-structure/departments`).
* **Dependencies**: Database, `Authentication Service`.
* **Technology Stack**: Python, FastAPI, SQLAlchemy, Pydantic.

***

#### **`[Backend]` Bulk Import Service**

* **Responsibility**: Manages the two-stage file import process. The first stage involves accepting a file, performing a comprehensive validation, and returning either a detailed error report or a temporary ID for the validated file. The second stage accepts this ID and enqueues the processing job in Redis.
* **Key Interfaces**: API endpoints `POST /admin/bulk-import/validate` and `POST /admin/bulk-import/process`.
* **Dependencies**: `Redis`, `File Storage`, `Data Import Job Handlers [Worker]`.
* **Technology Stack**: Python, FastAPI, Pydantic, Pandas.

***

#### **`[Backend]` Job Monitoring Service**

* **Responsibility**: Acts as the single source of truth for the state of all background jobs. It manages the `BackgroundTask` database table, provides REST endpoints for listing jobs and initiating management actions, and broadcasts status updates over the WebSocket channel. The "Force Fail" action **must be implemented as an atomic, transactional operation** to prevent race conditions.
* **Key Interfaces**: REST API endpoints under `/admin/job-monitor/*` and the WebSocket endpoint at `/ws/job-progress/{jobId}`.
* **Dependencies**: Database (`BackgroundTask` table), `Redis` (to query the state of RQ jobs), WebSocket Manager.
* **Technology Stack**: Python, FastAPI, SQLAlchemy, Pydantic, `websockets`.

***

#### **`[Worker]` Data Import Job Handlers**

* **Responsibility**: A collection of distinct, asynchronous tasks that execute the data import logic. All jobs **must be configured with a definitive timeout** within the RQ framework to prevent "zombie" processes. All import jobs must process data in transactional batches and update progress after each batch. If a batch fails, the job continues and finishes with a `completed_partial_failure` status, generating an error report of only the failed rows. On any unhandled failure, the job **must populate the `log_output` field** in the `BackgroundTask` table with the exception traceback before terminating.
* **Key Interfaces**: Python functions consumed from the Redis job queue; they do not expose any network APIs.
* **Dependencies**: Database, `Notification Service`.
* **Technology Stack**: Python, RQ, SQLAlchemy, Pandas.

#### **`[Worker]` Scheduled Cleanup Task (New Component)**

* **Responsibility**: A system-level, scheduled task (e.g., cron job) that runs periodically. Its sole purpose is to ensure system self-healing by identifying jobs that have been marked as timed-out by the underlying RQ framework but have not yet been updated in the application's primary `BackgroundTask` database table. It transitions these "zombie" jobs to a final `failed` state.
* **Key Interfaces**: This component is triggered by a system scheduler (e.g., cron), not by an API call or a user-initiated job queue.
* **Dependencies**: Database (`BackgroundTask` table), Redis (to query RQ's failed/timed-out queues).
* **Technology Stack**: Python, RQ, SQLAlchemy.

***

### **Group 3: Evaluation Lifecycle Management**

This group contains all components related to the administrative setup of the evaluation process. It empowers University Admins to create dynamic form templates, schedule evaluation periods, and manage the entire lifecycle of an evaluation from creation to potential cancellation.

#### **`[Frontend]` Form Builder Module**

* **Responsibility**: Provides a rich, interactive user interface for Admins to create, manage, and preview dynamic evaluation form templates. It implements an auto-save feature that periodically saves changes for `draft` templates. It **must gracefully handle `409 Conflict` errors** received during auto-save by notifying the user that the form has been updated by someone else and providing a clear action to refresh the data.
* **Key Interfaces**: A main page at `/admin/form-management` and a multi-step wizard or tabbed interface for form creation/editing.
* **Dependencies**: `Form Template Service [Backend]`, `TanStack Query`, `shadcn/ui` components.
* **Technology Stack**: React, TypeScript, TanStack Query, React Hook Form, Zod, `dnd-kit`.

***

#### **`[Frontend]` Period Scheduler Module**

* **Responsibility**: Implements the user interface for Admins to schedule a new evaluation period. This includes selecting the academic term, setting start/end dates, and assigning the appropriate form templates for student and department head evaluators. It also handles the UI for duplicating, canceling, and restoring periods.
* **Key Interfaces**: A page at `/admin/period-management` that lists all periods and provides actions. A form, either on a separate page or in a dialog, is used for creating/editing a scheduled period.
* **Dependencies**: `Evaluation Period Service [Backend]`, `TanStack Query` for data management, `shadcn/ui` components.
* **Technology Stack**: React, TypeScript, TanStack Query, `shadcn/ui` (Table, Calendar, AlertDialog for confirmations).

***

#### **`[Frontend]` Registration Code Manager**

* **Responsibility**: Provides the UI for Admins to create, view, and manage role-specific registration codes for their university. This includes setting usage limits, viewing current usage, and deactivating or regenerating codes.
* **Key Interfaces**: A dedicated section within the `/admin/user-management` page that displays a table of registration codes and provides forms/dialogs for management actions.
* **Dependencies**: The backend API endpoints for managing registration codes.
* **Technology Stack**: React, TypeScript, TanStack Query, `shadcn/ui` (Table, Dialog, Form, Switch).

***

#### **`[Backend]` Form Template Service**

* **Responsibility**: Exposes the API for all CRUD operations on `EvaluationFormTemplates`, `EvaluationCriteria`, and `EvaluationQuestions`. It is responsible for enforcing all business logic (e.g., weights sum to 100). It **must implement optimistic locking using a `version` field** to prevent concurrent edit conflicts. Furthermore, every state-changing operation (`POST`, `PUT`, `DELETE`) handled by this service **must generate a detailed entry in the `AuditLog` table** to ensure full traceability of administrative actions.
* **Key Interfaces**: RESTful API endpoints under `/admin/form-templates/*`.
* **Dependencies**: Database, `Authentication Service`, `AuditLog` Service.
* **Technology Stack**: Python, FastAPI, SQLAlchemy, Pydantic.

***

#### **`[Backend]` Evaluation Period Service**

* **Responsibility**: Manages the lifecycle of evaluation periods. On every critical API call, it **must re-validate the period's `start_date_time` and `end_date_time` against the current server time**, acting as the definitive source of truth for a period's active status. It handles the API for scheduling, updating, and initiating the cancellation or restoration of a period. Every state-changing operation handled by this service **must also generate a detailed entry in the `AuditLog` table**.
* **Key Interfaces**: RESTful API endpoints under `/admin/evaluation-periods/*`.
* **Dependencies**: Database, `Authentication Service`, `Redis`, `AuditLog` Service.
* **Technology Stack**: Python, FastAPI, SQLAlchemy, Pydantic.

***

#### **`[Worker]` Period Cancellation Job Handler**

* **Responsibility**: An asynchronous task that executes the logic for the "soft" cancellation and restoration of an evaluation period. It handles the batch update of submission statuses and dispatches notifications to affected users, operating within the defined grace period logic.
* **Key Interfaces**: A Python function consumed from the Redis job queue; it does not expose any network APIs.
* **Dependencies**: Database, `Notification Service`.
* **Technology Stack**: Python, RQ, SQLAlchemy.

***

### **Group 4: Evaluation Submission & Integrity Engine**

This group defines the core user-facing evaluation workflow and the backend engine that ensures data quality through automated flagging and administrative review.

#### **`[Frontend]` Evaluation Form Component**

* **Responsibility**: Renders the dynamic evaluation form for students and department heads. It must enforce all client-side validation rules, such as minimum time on form and word counts, and implement the "Pre-Submission Nudge" for low-variance scores.
* **Key Interfaces**: A dynamic React component that takes a form structure (criteria, questions) as a prop and renders the appropriate inputs.
* **Dependencies**: `Evaluation Submission Service [Backend]`, `React Hook Form` & `Zod` for validation, `TanStack Query` for the submission mutation.
* **Technology Stack**: React, TypeScript, React Hook Form, Zod, `shadcn/ui` (Form, Input, Accordion, Button).

***

#### **`[Frontend]` Flagged Evaluation Module**

* **Responsibility**: Provides the administrative interface for reviewing and resolving flagged evaluations. It must display the submission data in a side-by-side comparison and dynamically highlight the specific text that triggered a flag, using metadata provided by the backend.
* **Key Interfaces**: A page at `/admin/flagged-evaluations` featuring a table of pending flags and a detailed review dialog or sheet.
* **Dependencies**: `Flagged Evaluation Service [Backend]`, `TanStack Query`, `shadcn/ui` components.
* **Technology Stack**: React, TypeScript, TanStack Query, `shadcn/ui` (Table, Dialog, Tabs).

***

#### **`[Backend]` Evaluation Submission Service**

* **Responsibility**: Ingests completed evaluation submissions. It performs initial validation, creates the core submission records in the database, and then orchestrates the **"Pluggable Flagging Engine."** It iterates through and executes all registered **synchronous** flagging strategies. Finally, it enqueues a single, generic `process_async_flags` job for the worker to handle the asynchronous strategies.
* **Key Interfaces**: A `POST /evaluations/submissions` endpoint.
* **Dependencies**: Database, `Redis`, `Authentication Service`, `Flagging Engine`.
* **Technology Stack**: Python, FastAPI, SQLAlchemy, Pydantic.

***

#### **`[Backend]` Flagged Evaluation Service**

* **Responsibility**: Manages the lifecycle of flagged evaluations. It provides APIs for listing pending flags and for an Admin to resolve a flag with one of the three actions: 'Approve', 'Archive', or 'Request Resubmission'. It must implement optimistic locking to prevent concurrent resolutions.
* **Key Interfaces**: RESTful API endpoints under `/admin/flagged-evaluations/*`.
* **Dependencies**: Database, `Notification Service`, `Authentication Service`.
* **Technology Stack**: Python, FastAPI, SQLAlchemy, Pydantic.

***

#### **`[Worker]` Asynchronous Flagging Worker (Replaces Data Integrity Job Handlers)**

* **Responsibility**: A generic worker that consumes the `process_async_flags` job from the Redis queue. Its sole responsibility is to orchestrate the **"Pluggable Flagging Engine"** by iterating through and executing all registered **asynchronous** flagging strategies for a given submission. For strategies that require configurable values (like the similarity threshold), this worker is responsible for querying the `UniversitySetting` table to retrieve them.
* **Key Interfaces**: A Python function consumed from the Redis job queue.
* **Dependencies**: Database (`UniversitySetting` table), `Flagging Engine`.
* **Technology Stack**: Python, RQ, SQLAlchemy.

***

#### **Flagging Engine (Conceptual Component / Strategy Pattern)**

* **Responsibility**: This is a conceptual component representing the implementation of a **Strategy Pattern**. It consists of a collection of individual "strategy" classes, each responsible for a single data integrity check (e.g., `LowConfidenceStrategy`, `RecycledContentStrategy`). Each strategy class implements a common interface and self-declares whether it should be executed synchronously or asynchronously. This design makes the system modular and highly extensible, fulfilling **NFR11**.
* **Key Interfaces**: An internal `FlaggingStrategy` interface (e.g., an abstract base class) and a central registry that holds all active strategies.
* **Dependencies**: Varies by strategy (e.g., Database, AI Models).
* **Technology Stack**: Python.

***

### **Group 5: Data Analysis & Visualization Pipeline**

This group covers the entire pipeline, from the raw data processing jobs to the final presentation layer. It includes the backend worker jobs that perform analysis and the frontend components that render the results.

#### `[Frontend]` Dashboard Shell

* **Responsibility**: Serves as the main container and orchestrator for all dashboard pages. It is responsible for rendering the overall layout, including the **tiered structure (KPIs, Actionable Insights, General Visualizations)**, the persistent filter bars, and the "mode-switcher" control for Department Heads and Admins. Critically, it must also **display the current data status** (e.g., a "Provisional Data" banner) based on API metadata to fulfill the requirements of FR8.
* **Key Interfaces**: A React component that fetches initial dashboard data and passes it down to its children. It listens for events from child components (like filters) to trigger targeted data refetches.
* **Dependencies**: `Dashboard Data Service [Backend]`, `Visualization Components`, `Comment Viewer Component`.
* **Technology Stack**: React, TypeScript, TanStack Query, `shadcn/ui` (Card, Select, Tabs, Banner/Alert).

***

#### `[Frontend]` Visualization Components

* **Responsibility**: A set of reusable client components that wrap the ECharts library to render the specific visualizations required by the PRD (Word Clouds, Bar Charts, and Performance Trend Line Charts). These components are responsible for accepting structured data, rendering the appropriate chart, and **emitting events when a user interacts with a data point** (e.g., clicking a bar segment) to trigger the `Comment Viewer`.
* **Key Interfaces**: Individual React components (`WordCloudChart`, `SentimentBarChart`, etc.) that accept ECharts-compatible data and configuration options as props, along with an `onDataPointClick` event handler.
* **Dependencies**: `Echarts` and `echarts-wordcloud` libraries.
* **Technology Stack**: React, TypeScript, ECharts.

***

#### `[Frontend]` Comment Viewer Component

* **Responsibility**: A dialog component that fetches and displays anonymized, raw open-ended comments for a specific data slice. It is critically responsible for **enforcing the anonymity threshold on the client-side**, showing a privacy message (e.g., "More responses are needed to view comments") instead of the comments if the underlying response count is too low, as required by PRD Story 5.5.
* **Key Interfaces**: A modal/dialog component that is triggered by an event from a `Visualization Component` and is passed the necessary filters to fetch the relevant comments from the `Comment Data Service`.
* **Dependencies**: `Comment Data Service [Backend]`, `shadcn/ui` components.
* **Technology Stack**: React, TypeScript, `shadcn/ui` (Dialog).

***

#### `[Backend]` Dashboard Data Service

* **Responsibility**: (Refactored) Exposes the API endpoints required to populate all dashboards. Its responsibility is now significantly simplified: it **efficiently reads from pre-calculated aggregate tables**—either the provisional aggregate table (for active periods) or the final snapshot tables (for closed periods). It no longer performs on-the-fly calculations or caching.
* **Key Interfaces**: A `GET /dashboard` endpoint that accepts various filters (term, period, view\_mode) and returns a complex JSON object structured for the frontend dashboards.
* **Dependencies**: Database (aggregate tables), `Authentication Service`.
* **Technology Stack**: Python, FastAPI, SQLAlchemy, Pydantic.

***

#### **`[Worker]` Provisional Data Micro-batching Job (New Component)**

* **Responsibility**: A scheduled worker that runs every few minutes (e.g., 5 minutes). Its sole purpose is to calculate aggregates for any *new*, successfully processed submissions that have arrived since its last run. It populates a dedicated `provisional_aggregates` table in the database, ensuring that the dashboard API has fast, pre-calculated data to read.
* **Key Interfaces**: This component is triggered by a system scheduler (e.g., cron), not by a direct API call.
* **Dependencies**: Database.
* **Technology Stack**: Python, RQ, SQLAlchemy.

***

#### **`[Worker]` Analysis Pipeline Cleanup Task (New Component)**

* **Responsibility**: A scheduled worker that runs periodically to ensure the self-healing of the analysis pipeline. It searches for submissions that have been stuck in an intermediate `analysis_status` (e.g., `quant_qual_complete`) for too long and automatically re-enqueues the appropriate failed job (e.g., the `Final Aggregation Job`).
* **Key Interfaces**: This component is triggered by a system scheduler.
* **Dependencies**: Database, Redis (to re-enqueue jobs).
* **Technology Stack**: Python, RQ, SQLAlchemy.

***

#### `[Backend]` Comment Data Service

* **Responsibility**: A dedicated, secure service that handles fetching raw open-ended comments. Its primary responsibility is to **enforce the anonymity threshold on the server-side**. It will reject any request for comments where the underlying response count for the requested data slice is below the configured minimum, returning a `403 Forbidden` error to protect user privacy.
* **Key Interfaces**: A `GET /comments` endpoint that accepts the same filters as the dashboard to define a specific data slice.
* **Dependencies**: Database (raw `evaluation_open_ended_answers` table), `Authentication Service`.
* **Technology Stack**: Python, FastAPI, SQLAlchemy, Pydantic.

***

#### `[Worker]` Quantitative Analysis Job

* **Responsibility**: An asynchronous task that processes the numerical Likert-scale answers from a submission. It executes the specific calculation flow defined in PRD Story 5.1: **first, it calculates the median score for each question; second, it calculates the mean of those medians for each criterion; and finally, it calculates the final weighted mean (`quant_score_raw`)**, saving the results to the `numerical_aggregates` table.
* **Key Interfaces**: A Python function consumed from the Redis job queue, managed by the `Analysis Orchestrator`.
* **Dependencies**: Database.
* **Technology Stack**: Python, RQ, SQLAlchemy, NumPy/SciPy (for statistical calculations).
* **Critical Requirements**:
  * All jobs **must be idempotent** to allow for safe, automatic retries.
  * The **`Final Aggregation Job`** must include **defensive logic to handle small cohort sizes** (e.g., n < 2) to prevent division-by-zero errors during Z-score calculation.

***

#### `[Worker]` Qualitative Analysis Job

* **Responsibility**: An asynchronous task that processes the open-ended feedback from a submission. It uses the local AI models (XLM-RoBERTa for sentiment, KeyBERT for keywords) to analyze the text and saves the structured results to the `open_ended_sentiments` and `open_ended_keywords` tables, as required by PRD Story 5.2.
* **Key Interfaces**: A Python function consumed from the Redis job queue, managed by the `Analysis Orchestrator`.
* **Dependencies**: Database, local AI models (Transformers, PyTorch, KeyBERT).
* **Technology Stack**: Python, RQ, SQLAlchemy, Transformers, PyTorch.
* **Critical Requirements**:
  * All jobs **must be idempotent** to allow for safe, automatic retries.
  * The **`Final Aggregation Job`** must include **defensive logic to handle small cohort sizes** (e.g., n < 2) to prevent division-by-zero errors during Z-score calculation.

***

#### `[Worker]` Final Aggregation Job

* **Responsibility**: The final job in the analysis pipeline, which is orchestrated to run only after the Quantitative and Qualitative analysis jobs are complete. It **fetches the score weighting from the `UniversitySetting` table** (e.g., `score_weight_quantitative`), calculates the cohort baselines, computes the normalized **Z-scores (`z_quant` and `z_qual`)**, and calculates the final weighted score (`final_score_60_40`). It also handles locking the data by setting the `is_final_snapshot` flag when a period is finalized, fulfilling PRD Story 5.3.
* **Key Interfaces**: A Python function consumed from the Redis job queue, triggered by the `Analysis Orchestrator`.
* **Dependencies**: Database (`UniversitySetting`, `NumericalAggregate`, `SentimentAggregate` tables).
* **Technology Stack**: Python, RQ, SQLAlchemy, NumPy/SciPy.
* **Critical Requirements**:
  * All jobs **must be idempotent** to allow for safe, automatic retries.
  * The **`Final Aggregation Job`** must include **defensive logic to handle small cohort sizes** (e.g., n < 2) to prevent division-by-zero errors during Z-score calculation.

***

### **Group 6: AI Intelligence & Reporting Services**

This group focuses on the advanced features that provide actionable insights, including the AI Assistant and the formal Report Center. It is designed with a strong emphasis on resilience, cost control, and maintainability.

#### `[Frontend]` AI Assistant Module

* **Responsibility**: Provides the dedicated user interface for Faculty and Department Heads to generate AI-powered suggestions. This module is responsible for rendering the necessary filters, displaying the predefined action buttons, and initiating the asynchronous generation process. It then monitors the job's progress via the WebSocket connection and displays the final results, along with options to save or export. \[cite\_start]It must also gracefully handle error states, such as when the service is temporarily unavailable. \[cite: 1472]
* **Key Interfaces**: A page at `/ai-assistant` that orchestrates filter components, action buttons, and a results display area. \[cite\_start]It includes a "History" tab for viewing saved suggestions. \[cite: 1435]
* **Dependencies**: `AI Suggestion Service [Backend]`, `Job Monitor Module [Frontend]`, `shadcn/ui` components.
* **Technology Stack**: React, TypeScript, TanStack Query, `shadcn/ui` (Select, Button, Card, Tabs).

***

#### `[Frontend]` Report Center Module

* \[cite\_start]**Responsibility**: Implements the UI for the formal "Report Center," featuring a two-tab layout for "Generate Report" and "My Reports." \[cite: 1445] It allows users to select a report type, apply filters, and initiate an asynchronous generation job. \[cite\_start]The "My Reports" tab acts as a real-time inbox, using the WebSocket connection to display the status of pending and completed reports, providing download links when ready. \[cite: 1445]
* **Key Interfaces**: A page at `/report-center` with a form for report generation and a table for tracking report history and status.
* **Dependencies**: `Report Generation Service [Backend]`, `Job Monitor Module [Frontend]`, `shadcn/ui` components.
* **Technology Stack**: React, TypeScript, TanStack Query, `shadcn/ui` (Tabs, Select, Button, Table).

***

#### `[Backend]` AI Suggestion Service

* **Responsibility**: Acts as a secure gateway for initiating AI suggestions. Its sole responsibilities are to validate the incoming user request, check it against the **configurable rate limits** defined in `UniversitySetting`, and, if valid, **enqueue an asynchronous job** in Redis. It does **not** call the external Gemini API directly. \[cite\_start]It is also responsible for all CRUD operations on the `AISuggestion` history table. \[cite: 1425]
* **Key Interfaces**: API endpoints under `/ai-assistant/*` and `/ai-suggestions/*`.
* **Dependencies**: Database (`AISuggestion`, `UniversitySetting` tables), `Redis`, `Authentication Service`.
* **Technology Stack**: Python, FastAPI, SQLAlchemy, Pydantic.

***

#### **`[Backend]` Report Generation Service**

* **Responsibility**: Manages the lifecycle of formal reports. Its primary responsibility is to perform a **pre-computation check** on every incoming request to estimate its size (e.g., by counting the number of database records involved). If the request exceeds a configurable threshold, it **must** be rejected immediately with a `413 Payload Too Large` error to protect system resources. If the request is valid, it then enqueues the appropriate job in Redis, manages the state of the `GeneratedReport` database table, and provides secure endpoints for downloading completed files.
* **Key Interfaces**: API endpoints under `/reports/*`.
* **Dependencies**: Database (`GeneratedReport`, `UniversitySetting` tables), `Redis`, `Authentication Service`, `File Storage`.
* **Technology Stack**: Python, FastAPI, SQLAlchemy, Pydantic.

***

#### **`[Worker]` AI Suggestion Job Handler**

* **Responsibility**: An asynchronous task that performs the actual AI suggestion generation. It is responsible for:
  1. Fetching the necessary processed evaluation data.
  2. Constructing a detailed prompt from an externalized template file.
  3. Prepending a **strong system prompt** to the request to define the AI's role and constraints, mitigating the risk of prompt injection.
  4. Making the external API call to the Gemini API, wrapped in a **Circuit Breaker** to handle external service failures gracefully.
  5. **Validating the incoming JSON response** from the Gemini API against a strict Pydantic model to defend against unexpected schema changes.
  6. Saving the validated result to the `AISuggestion` table.
* **Key Interfaces**: A Python function consumed from the Redis job queue.
* **Dependencies**: Database (`AISuggestion` table), External Gemini API.
* **Technology Stack**: Python, RQ, SQLAlchemy, `requests`, `httpx`.

***

#### `[Worker]` Report Generation Job Handlers

* **Responsibility**: A collection of asynchronous tasks that execute the file generation logic. These handlers are consumed from the Redis job queue. \[cite\_start]Each handler fetches the required data, uses the appropriate library (**WeasyPrint for PDF**, **Pandas for CSV/Excel**) to create the file, saves the final artifact to the `File Storage` volume, and updates the corresponding `GeneratedReport` record in the database with a `Ready` status and the file's storage path. \[cite: 1301]
* **Key Interfaces**: Python functions consumed from the Redis job queue.
* **Dependencies**: Database, `File Storage`.
* **Technology Stack**: Python, RQ, SQLAlchemy, WeasyPrint, Pandas.

***
