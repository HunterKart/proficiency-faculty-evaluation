# Proficiency Product Requirements Document (PRD)

---

### **Section 1: Goals and Background Context**

#### **Goals**

-   **Develop "Proficiency," a multi-tenant SaaS web platform** to modernize the faculty evaluation process for educational institutions, starting with the University of Cebu - Lapu-Lapu and Mandaue.
-   **Implement an AI-powered analysis engine** that automatically processes qualitative feedback from students and department heads to provide sentiment analysis, keyword extraction, and generate actionable, data-driven suggestions for improvement.
-   **Ensure high data quality and evaluation integrity** through automated, server-side checks that flag low-effort submissions and detect recycled content.
-   **Provide highly dynamic and customizable evaluation forms** that allow administrators to tailor evaluation criteria, questions, and scoring to diverse institutional needs.
-   **Deliver intuitive, role-based dashboards and visualizations** to make evaluation results easy to interpret for faculty, department heads, and administrators, supporting continuous faculty development and institutional decision-making.

#### **Background Context**

Existing faculty evaluation systems, particularly within the Philippines and at the target institution, suffer from significant limitations. These systems often rely on static forms that cannot adapt to changing criteria and over-emphasize quantitative Likert scores while failing to extract meaningful insights from valuable open-ended feedback. The analysis of this textual feedback is often a manual, time-consuming, and error-prone process, resulting in low-quality, unactionable results that do little to support genuine faculty growth.

"Proficiency" is designed to address these critical gaps. It is a modern SaaS platform that leverages an AI pipeline to automate the deep analysis of textual feedback, providing insights into sentiment and key themes. By combining this with robust integrity checks, customizable forms, and role-based data visualization, Proficiency aims to transform faculty evaluation from a burdensome administrative task into a powerful tool for continuous professional development and educational excellence.

#### **Change Log**

| Date           | Version | Description                                                                                                                                                        | Author        |
| :------------- | :------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------ |
| **2025-10-09** | **8.6** | **Added foundational technical stories (1.10, 1.11) for API middleware and frontend mocking to Epic 1, including dependency mapping.**                             | **John, PM**  |
| **2025-10-09** | **8.5** | **Added Story 1.9 to track the critical task of provisioning and configuring external services.**                                                                  | **Sarah, PO** |
| **2025-10-09** | **8.4** | **Added Story 7.1 for user-facing help documentation to ensure end-user support materials are created.**                                                           | **John, PM**  |
| **2025-10-09** | **8.3** | **Aligned real-time functionality with architecture spec, adopting a hybrid WebSocket/polling model.**                                                             | **John, PM**  |
| **2025-10-09** | **8.2** | **Added NFR14 to formalize automated WCAG accessibility testing on every pull request, as defined in the final architecture.**                                     | **John, PM**  |
| **2025-10-08** | **8.1** | **Refined Story 3.1 to include an admin interface for managing new university-specific settings, aligning with the `UniversitySetting` data model.**               | **John, PM**  |
| **2025-10-08** | **8.0** | **Updated NFR2 and NFR11 to explicitly state that score weights and integrity thresholds are now configurable via the `UniversitySetting` model, not hard-coded.** | **John, PM**  |
| 2025-10-08     | 7.9     | Refined Story 2.2 and 5.6 to align with the finalized `BackgroundTask` and `GeneratedReport` data models from the architectural specification.                     | John, PM      |
| 2025-10-08     | 7.8     | Added FR19 to centralize and formalize the system-wide notification requirement, aligning with the new `Notification` model from the architectural specification.  | John, PM      |
| 2025-10-08     | 7.7     | Added FR18 to require a pre-computation check and size limit for report generation to protect system stability, per architectural review.                          | John, PM      |
| 2025-10-08     | 7.6     | Refined FR8 to specify data latency (e.g., 5 mins) due to micro-batching architecture. Added FR17 for an admin API to re-aggregate historical data.                | John, PM      |
| 2025-10-08     | 7.5     | Refined NFR11 to explicitly require that integrity check thresholds (e.g., similarity percentage) must be configurable per university, per architectural review.   | John, PM      |
| 2025-10-08     | 7.4     | Added NFR13 to mandate detailed audit logging for all administrative actions on forms and periods, per architectural review.                                       | John, PM      |
| 2025-10-07     | 7.3     | Added FR16 to mandate a 24-hour expiration on new user verification links per architectural review to enhance security.                                            | John, PM      |
| 2025-10-07     | 7.2     | Added NFR12 to make AI Assistant and Report Generation rate limits configurable as per architectural recommendation for operational control.                       | John, PM      |
| 2025-10-07     | 7.1     | Updated NFR2 to make the 60/40 score weighting a configurable, database-seeded value per architectural recommendation for future flexibility.                      | John, PM      |
| 2025-10-07     | 7.0     | Added NFR11 for modular design of the data integrity engine to ensure future extensibility.                                                                        | John, PM      |
| 2025-10-07     | 6.9     | Added auto-save functionality as an acceptance criterion for the form builder (Story 3.3) to prevent data loss during edits.                                       | John, PM      |
| 2025-10-07     | 6.8     | Added `Completed_Partial_Failure` status for bulk imports and defined partial failure report behavior to improve data import resilience.                           | John, PM      |
| 2025-10-07     | 6.7     | Added NFR10 for Transactional Integrity to ensure critical business processes are atomic.                                                                          | John, PM      |
| 2025-10-07     | 6.6     | Added Story 1.7 for Super Admin user account management and renumbered backup story to 1.8.                                                                        | John, PM      |
| 2025-10-07     | 6.5     | Added FR15 to prevent deletion of in-use resources. Refactored Period Cancellation (Story 3.6, 3.8) to a 72-hour restorable soft cancellation.                     | John, PM      |
| 2025-10-06     | 6.4     | Aligned Story 1.5 with architectural safety measures regarding data file validation during university approval.                                                    | John, PM      |
| 2025-10-06     | 6.3     | Added "Duplicate Period" (FR13, Story 3.9) and "Proactive Notification" (FR14, Story 3.10) features to improve admin workflow.                                     | John, PM      |
| 2025-10-02     | 6.2     | Final version with complete Acceptance Criteria for all new stories, refined through elicitation. PRD is finalized.                                                | John, PM      |
| 2025-10-02     | 6.1     | Applied structural changes and new requirements based on alignment with front-end-spec v2.0.                                                                       | John, PM      |
| 2025-10-02     | 6.0     | Final PRD incorporating all refinements from the completed elicitation process. PRD is now locked and ready for architecture.                                      | John, PM      |
| 2025-10-02     | 5.0     | Final PRD incorporating all elicitation refinements and multi-admin concurrency controls. Ready for architecture.                                                  | John, PM      |
| 2025-10-02     | 4.0     | Final version incorporating all elicitation refinements. Removed overrides, added safeguards (Cancel Period, Timezone), and improved UX flows.                     | John, PM      |
| 2025-10-02     | 3.1     | Removed department-level form overrides to reduce complexity. Aligned PRD with product decisions from front-end-spec-1.7.                                          | John, PM      |
| 2025-09-30     | 3.0     | Added Epic 2 for historical data import & refined stories based on elicitation. Updated UI goals.                                                                  | John, PM      |
| 2025-09-29     | 2.1     | Added support for department-level form overrides to enhance customization and data quality.                                                                       | John, PM      |
| 2025-09-28     | 2.0     | Final PRD with all 5 epics and elicitation refinements.                                                                                                            | John, PM      |
| 2025-09-28     | 1.0     | Initial PRD draft based on Project Brief and Capstone Manuscript.                                                                                                  | John, PM      |

---

### **Section 2: Requirements**

#### **Functional Requirements**

-   **FR1: User and University Management**
    -   The system shall support five user roles: **Students, Faculty, Department Heads, Admins, and Super Admins**.
    -   For V1, user creation will be limited to two methods: 1) **Admin/Super Admin bulk import** via CSV/Excel and 2) **Self-registration using a valid, university-provided invitation token**. The "evidence-based" manual sign-up is deferred to a post-V1 release.
    -   **Super Admins** shall manage the university registration and approval lifecycle.
-   **FR2: Dynamic Evaluation Form & Period Management**
    -   Admins shall have the ability to **create, modify, and manage dynamic evaluation form templates** with the statuses: `draft`, `active`, `assigned`, and `archived`.
    -   Admins shall **assign form templates to specific evaluation periods**, defined by school year, semester (1st, 2nd, Summer), and assessment period (Midterm, Finals).
    -   An `'assigned'` form template is locked and cannot be edited. An `'active'` form template remains editable.
-   **FR3: Evaluation Submission & Integrity**
    -   The system must implement a **"Pre-Submission Nudge,"** a non-blocking UI message to encourage users with low-variance Likert scores to provide written examples.
    -   A submission must be automatically flagged with **"Low-Confidence"** if it contains both low-variance Likert scores AND short or empty open-ended answers.
    -   The system shall run an asynchronous job to detect and flag **"Recycled Content"** that has over 95% similarity to previous submissions.
-   **FR4: Flagged Evaluation Workflow**
    -   The system must automatically flag evaluations for data inconsistencies, such as a **sentiment-coherence mismatch**.
    -   Admins shall have a dedicated interface to review all flagged evaluations.
    -   Admins must be able to resolve a flagged evaluation by choosing one of three actions: **Approve**, **Archive**, or **Request Resubmission**.
    -   **FR4.1:** The notification sent to a Student for a resubmission request or archived evaluation **must be anonymous** and clearly state the reason to guide them.
    -   **FR4.2:** The Admin's review dashboard for flagged evaluations must provide a **side-by-side comparison** of the submission's numerical ratings and its open-ended text.
-   **FR5: Data Analysis Pipeline**
    -   All evaluation submissions shall be processed asynchronously via a **job queue (Redis+RQ)**.
    -   The pipeline must separate analysis into a **Quantitative Layer** and a **Qualitative Layer**.
    -   A final layer shall perform **Normalization and Aggregation** to combine scores and prepare data for visualization.
    -   **FR5.1:** Evaluation submissions with a status of 'archived' or 'pending review' **must be excluded** from all aggregate calculations.
-   **FR6: AI-Powered Analysis and Insights**
    -   The system must perform automated **sentiment analysis** (Primary Model: XLM-ROBERTa) and **keyword extraction** (KeyBERT).
    -   A dedicated **"AI Assistant" page** shall be available to Faculty and Department Heads to generate reports and suggestions from processed data using the external Gemini API.
-   **FR7: Dashboards and Visualizations**
    -   The system shall present data using specific visualizations: **Word Clouds, Bar Charts, and Performance Trend Line Charts**. Admins will also have access to an **Evaluation Submission Behavior Line Chart**.
    -   Department Heads and Admins must be able to switch between different data views or **"modes"** (e.g., department-wide, specific faculty results).
-   **FR8: Provisional and Finalized Reporting Workflow**
    -   All reports for an active review period shall be marked as **"Provisional."**. When an Admin approves a flagged evaluation, an asynchronous job must **recalculate the provisional aggregates** for the affected parties. Admins shall have a function to **"Finalize and Lock Period,"** which runs a final aggregation and sets the `is_final_snapshot` flag to `true`. To ensure high performance and scalability for all users, data on provisional dashboards is updated via a near real-time process. As such, the displayed aggregates **may be up to 5 minutes out of date** and may not instantly reflect the most recent submissions.
-   **FR9: Historical Data Import**
    -   Admins shall have the ability to bulk import historical university data via CSV/Excel to prime the system.
    -   The import process must support: **Academic Structure** (departments, programs, subjects), **User & Enrollment Records**, and **Past Evaluation Submissions** (including Likert and open-ended answers).
    -   All imported historical evaluation records must be processed by the system's data analysis pipeline (as defined in FR5 and FR6).
-   **FR10: Registration Code Management**: Admins shall be able to set, view, and update the maximum usage limit for their university's self-registration code.
-   **FR11: Role-Based Registration Codes**: The system must support the generation of distinct self-registration codes for different user roles. The registration process must validate that the user's selected role matches the intended role of the code provided.
-   **FR12: Resubmission Grace Period**: A "resubmission grace period" of 48 hours shall be granted to a student for a flagged evaluation, allowing them to resubmit their work even if the parent evaluation period is no longer active.
-   **FR13: Duplicate Evaluation Period Assignment**: Admins shall have the ability to duplicate an existing evaluation period assignment to pre-fill the creation form with the same form template configuration, requiring only new scheduling details to be entered.
-   **FR14: Proactive Period Setup Notification**: The system shall generate a notification for Admins when an evaluation period concludes, prompting them to schedule the next logical period and providing a one-click action to begin the duplication process.
-   **FR15: In-Use Resource Protection**: The system must prevent the archival or deletion of any resource (e.g., Form Template) that is currently assigned to an active or scheduled Evaluation Period. An attempt to do so must result in a clear error message explaining the dependency.
-   **FR16: Secure Account Verification**: To enhance security, account verification links sent to new users must automatically expire 24 hours after they are issued.
-   **FR17: Administrative Re-aggregation**: The system must provide a secure, admin-only API endpoint to trigger a full recalculation of all final, normalized scores for a given historical evaluation period. This enables reprocessing of data if scoring logic or configuration (like score weighting) is updated. A UI for this feature is not required for V1.
-   **FR18: Report Generation Limits**: To ensure system stability, the generation of reports is subject to a size limit. If a user's filter criteria would result in a report exceeding a configurable number of records, the request must be rejected, and the user must be prompted to narrow their search or apply more specific filters.
-   **FR19: Centralized Notification System**
    -   The system shall implement a centralized notification service to manage all user-facing alerts, backed by the `Notification` data model.
    -   Notifications must be stored in the database, linked to the recipient user.
    -   The system must support two primary delivery methods: **In-App** (viewable within the user's dashboard) and **Email**.
    -   The in-app notification interface must allow users to distinguish between `unread` and `read` notifications.
    -   Specific events that must trigger notifications include, but are not limited to: user account verification, completion of background jobs (e.g., imports), flagged evaluation resolution, and proactive administrative prompts.

#### **Non-Functional Requirements**

-   **NFR1: Architecture:** The system shall be a multi-tenant SaaS web platform with a modular, scalable, and asynchronous architecture.
-   **NFR2: Configurable Scoring Logic**
    -   The final evaluation score for a faculty member is a weighted combination of the aggregated quantitative (e.g., Likert scale) and qualitative (e.g., sentiment analysis) scores.
    -   The weighting must not be hard-coded. Instead, it must be stored as a configurable value within the `university_settings` table, allowing each university (tenant) to adjust the balance (e.g., 60/40, 70/30) as needed. The system will be seeded with a default of 60% quantitative and 40% qualitative.
-   **NFR3: Performance:** Access to AI-generated suggestions shall be restricted to Faculty and Department Heads to manage performance.
-   **NFR4: Security:** The system must implement robust user registration and authentication protocols.
-   **NFR5: Extensibility and Research:** The V1 production system will exclusively use the fine-tuned XLM-ROBERTa model. For academic comparison, a separate, non-production script or environment will be created to benchmark baseline models (VADER, Naïve Bayes, mBERT).
-   **NFR6: System Calibration:** The automated flagging algorithms must be calibrated to minimize false positives and ensure the volume of flagged evaluations is manageable for Admins.
-   **NFR7: Data Privacy Compliance:** All processing of imported historical and live user data must be compliant with the Data Privacy Act of 2012 (RA 10173). The architecture must account for the secure handling and storage of Personally Identifiable Information (PII).
-   **NFR8: Timezone Standardization:** The entire platform shall operate on a single, standardized timezone: **Philippine Standard Time (PST / Asia/Manila)**. All times displayed in the UI must be explicitly labeled as PST to prevent ambiguity.
-   **NFR9: Concurrency Control:** To ensure data integrity in a multi-admin environment, the system must implement **Optimistic Locking** for all shared, editable resources (e.g., Form Templates). Concurrent actions (e.g., two admins resolving the same item) must be handled gracefully on the backend on a "first-come, first-served" basis.
-   **NFR10: Transactional Integrity:** All critical, multi-step business processes that modify the database, such as university onboarding or evaluation period cancellation, must be executed as atomic transactions to prevent the system from entering an inconsistent state upon partial failure.
-   **NFR11: Configurable Data Integrity Engine**
    -   The system's data integrity checks (e.g., recycled content detection, low-effort submission flagging) must be designed in a modular fashion to allow for future expansion.
    -   Crucially, the thresholds for these checks (e.g., similarity percentage for recycled content) must be configurable on a per-university basis via the `university_settings` table. This ensures that administrators can fine-tune the engine's sensitivity to match their institution's specific academic standards.
-   **NFR12: Configurable Rate Limiting:** To ensure system stability and control operational costs, the system **must implement rate-limiting** for resource-intensive features, specifically the **AI Assistant (Story 6.2)** and **Report Generation (Story 5.6)**. The thresholds for these limits **must be stored as configurable values** in the `UniversitySetting` table and **must not be hardcoded**. Default values will be seeded for V1, and a UI for Admins to manage these settings is deferred to a post-V1 release.
-   **NFR13: Administrative Auditing**: All critical, state-changing actions performed by an administrator related to the evaluation lifecycle (including creating, updating, activating, or archiving form templates, and scheduling or cancelling evaluation periods) must generate a detailed entry in the system's audit log. The log must record the administrator who performed the action, the action taken, the target entity, and a timestamp.
-   **NFR14: Automated Accessibility Compliance Testing**: To ensure adherence to WCAG standards, the CI/CD pipeline must include an automated accessibility test using `cypress-axe` on every pull request. This test must be configured to prevent merging code that introduces accessibility violations.

---

### **Section 3: User Interface Design Goals**

#### **Overall UX Vision**

The user experience will embody **Modern, Data-Centric Professionalism**. The interface must feel clean, intuitive, and trustworthy, visually communicating a significant upgrade from traditional university systems. The design should prioritize clarity and ease-of-use, presenting complex evaluation data through simple, digestible visualizations. The design should actively avoid the cluttered, table-heavy, and visually dated aesthetic common in traditional enterprise portals. **Clarity and intuitive data visualization are the primary goals**.

#### **Core Screens and Views**

-   **Students:** Login, Dashboard, Evaluation History, Profile Management.
    -   The Student Dashboard will feature two tabs: "Pending Evaluations" (default) and "Completed Evaluations" for the current, active period. The "Pending Evaluations" view will default to a clear **matrix or table format**, with a user-selectable control to switch to a **card-based view**.
-   **Faculty:** Login, Dashboard (view personal results), Evaluation Insights, Performance Trends, Report Generation, AI Suggestion Page, Profile Management.
-   **Department Heads:** All Faculty views, plus a tabbed dashboard ("Overview" and "Explore Data") for department-level results, the ability to evaluate faculty, and Evaluation History (for their own submissions).
-   **Admins:** Similar views as Department Heads (a tabbed "Overview" and "Explore Data" dashboard for institutional, department, and faculty levels), but with no AI Suggestion Page. Plus: Review Flagged Evaluations, Form & Period Management, Academic Structure Management, and User Management (Bulk Import).
-   **Super Admins:** Login, Dashboard (platform metrics), University Management, User Management, Profile Management.

#### **Key Interaction Paradigms**

-   **Card-Based Layout:** Content will be organized into distinct cards with rounded corners and subtle shadows.
-   **Data-First Dashboards:** The primary landing page for all roles will be a dashboard that immediately surfaces relevant data.
-   **Responsive Sidebar Navigation:** A consistent, collapsible sidebar will serve as the primary navigation method.
-   **Tab-Switching & View Modes:** Dashboards may use tabs to separate key data contexts (e.g., Overview vs. Explore Data) and offer view-switching controls where appropriate.
-   **Contextual Clarity & Consistency:** The UI must always provide clear indicators of the user's current view (e.g., "Viewing: Department of IT Results"). The modern design aesthetic must be applied consistently across all parts of the application.

---

### **Section 4: Technical Assumptions**

#### **Repository Structure**

A **Monorepo** is the assumed structure to simplify development and deployment. The Architect must ensure the monorepo has clear internal package boundaries and that the CI/CD pipeline is optimized to build only changed services.

#### **Service Architecture**

The architecture will be a **simple monolith** consisting of a single FastAPI backend API and a single RQ background worker process.

#### **Additional Technical Assumptions**

-   **Technology Stack:** The core stack is defined as **React 19 / TypeScript 5.6**, **Python 3.12 with FastAPI 0.112**, and **MariaDB 11**.
-   **API Style:** The API will be primarily synchronous to maintain simplicity, with asynchronous methods used only where a clear benefit exists.
-   **Real-time Functionality:** The system will use a hybrid approach. Real-time updates for job monitoring and notifications will be implemented via WebSockets, while dashboard data refreshes will use frontend polling.
-   **AI/ML Models:** All AI models will be run via **local inference**.
-   **Deployment Target:** The application will be deployed to a **single VPS (Ubuntu)**, with all services managed via **Docker Compose**.
-   **Resource Management:** The Docker configuration must implement resource limits on the worker container to protect system stability.
-   **State Management:** Large-scale global state libraries are out of scope. React's **Context API** will be used for minimal global UI state.
-   **Disaster Recovery:** The Architect must define a clear disaster recovery plan for the single VPS deployment in the `architecture.md`.

---

### **Section 5: Epic List**

-   **Epic 1: Platform Foundation & University Onboarding**
    -   **Goal:** To establish the core technical infrastructure, multi-tenant foundation, and the complete administrative workflow for a Super Admin to onboard a new university, manage its lifecycle, and provision its user accounts via bulk import. This epic delivers the initial, foundational value of a ready-to-configure university tenant.
-   **Epic 2: Historical Data Onboarding & System Priming**
    -   **Goal:** To provide University Admins with a robust toolset to manually manage and bulk import historical academic data, including institutional structure, user enrollments, and past evaluation records. This epic concludes by fine-tuning the AI sentiment model using this imported data, making both the data and the model **analysis-ready** for a later epic.
-   **Epic 3: Administrative Control Panel**
    -   **Goal:** To provide University Admins with the complete toolset to manage the evaluation process, including the dynamic form builder and the flexible scheduling of evaluation periods.
-   **Epic 4: The Core Evaluation & Data Integrity Loop**
    -   **Goal:** To enable students and department heads to submit high-quality evaluations, supported by robust, automated data integrity checks and a complete administrative review workflow.
-   **Epic 5: Data Processing & Insights Visualization**
    -   **Goal:** To implement the asynchronous data analysis pipeline and provide all user roles with intuitive, role-based dashboards featuring clear, comparable data visualizations of evaluation results.
-   **Epic 6: AI-Powered Actionable Intelligence**
    -   **Goal:** To empower faculty and department heads with advanced, AI-generated suggestions and downloadable reports that translate evaluation data into actionable insights for professional development.
-   **Epic 7: Support & Documentation**
    -   **Goal:** To provide users with the necessary resources to understand and independently use the platform.

---

### **Section 6: Epic Details**

#### **Epic 1: Platform Foundation & University Onboarding**

**Story 1.1: Project Initialization**

-   **As a** Super Admin/Developer, **I want** the project monorepo and core service scaffolding to be initialized, **so that** a consistent development environment is established for the team.
-   **Acceptance Criteria:**
    1.  A monorepo structure is created and configured.
    2.  A placeholder FastAPI application for the backend is created within the monorepo.
    3.  A placeholder React/TypeScript application for the frontend is created within the monorepo.
    4.  A `docker-compose.yml` file is created to run the API, frontend, worker, and database services for local development.
    5.  A basic CI/CD pipeline is configured in the repository to run linters and placeholder tests on commit.
    6.  A comprehensive `README.md` file is created at the project root, containing the project title, a brief description, and clear instructions on how to run the local development environment.

**Story 1.2: Database and AI Environment Setup**

-   **As a** Super Admin/Developer, **I want** the database schema to be initialized and the AI model environment to be prepared, **so that** the core data structures are in place and future AI-related development is streamlined.
-   **Depends on:** Story 1.1
-   **Acceptance Criteria:**
    1.  A database migration tool is integrated into the backend service.
    2.  An initial migration script is created that generates all necessary tables as defined/referenced in the `architecture.md` within the Data Model and Database Schema sections.
    3.  The migration can be successfully run via a command within the local Docker environment.
    4.  A dedicated `Dockerfile` for the RQ worker is created, which installs the pinned Python 3.12 AI/ML dependencies (`transformers` 4.44.x, `torch` 2.8.x, `scikit-learn` 1.5.x, `keybert` 0.8.x, `google-generativeai` 0.6.x, etc.) to prevent slow builds in later epics.

**Story 1.3: Super Admin Authentication**

-   **As a** Super Admin, **I want** to securely log in to a dedicated super admin dashboard, **so that** I can manage the platform.
-   **Depends on:** Story 1.2
-   **Acceptance Criteria:**
    1.  A login form is available for Super Admins.
    2.  The system authenticates credentials against the `super_admins` table.
    3.  After successful password validation, the system prompts the Super Admin to enter their 6-digit PIN code for multi-factor authentication.
    4.  Upon successful PIN verification, the user is redirected to the Super Admin dashboard.
    5.  Failed login attempts (either password or PIN) display a clear error message.
    6.  **Developer Note:** The initial Super Admin account will be created via a secure, one-time database seeding script that is run manually upon initial deployment.

**Story 1.4: University Registration Request Submission**

-   **As an** incoming University Admin, **I want** to submit a registration request with my university's details and supporting documents, **so that** our institution can be onboarded to the Proficiency platform.
-   **Depends on:** Story 1.1
-   **Acceptance Criteria:**
    1.  A public-facing registration form is available on the application's landing page.
    2.  The form must capture all required institutional and contact person details as specified in the `university_registration_requests` table.
    3.  The form allows for the upload of one or more supporting documents (e.g., accreditation proof).
    4.  Upon successful submission, a record is created in the `university_registration_requests` table with a status of 'submitted', and the Super Admin team is notified.

**Story 1.5: University Request Review Workflow**

-   **As a** Super Admin, **I want** to view and manage a queue of pending university registration requests, **so that** I can approve or reject new institutions.
-   **Depends on:** Story 1.4
-   **Acceptance Criteria:**
    1.  The initial Super Admin dashboard must display summary cards for 'Active Universities,' 'Total Users,' and 'Pending Requests'.
    2.  The main component of the dashboard is an interface for managing requests through distinct stages: 'New', 'In Review', and 'Resolved'.
    3.  Approving a request creates a new record in the `universities` table, creates an initial `Admin` account in the `users` table, and updates the request status to 'approved'.
    4.  Upon approval, an email is sent to the `contact_person_email` containing a confirmation message and a unique, time-limited link to verify their new Admin account and set their password.
    5.  Rejecting a request requires a reason and triggers an email notification to the applicant with the reason for rejection, moving the request to the 'Resolved' stage.
    6.  The login page, when encountering an unverified Admin account, displays an error message and a 'Resend Verification Email' button that re-triggers the confirmation email. This function must also handle cases where the user's original verification link has expired.
    7.  The approval process must include a final confirmation step where the Super Admin acknowledges the validation status of any optionally uploaded data files before the approval can be finalized.

**Story 1.6a: Bulk Import Validation & Feedback**

-   **As an** Admin or Super Admin, **I want** to upload a user CSV file and receive clear validation feedback, **so that** I know if my file is correctly formatted before processing.
-   **Depends on:** Story 1.3, Story 1.5
-   **Acceptance Criteria:**
    1.  The **Admin dashboard** and the **Super Admin dashboard** must have an interface for uploading a user data file for a specific university.
    2.  A downloadable CSV/Excel template is provided to ensure correct data format.
    3.  The system validates the uploaded file for structural correctness.
    4.  The system provides clear, user-centric, row-specific error feedback for any invalid data (e.g., "_Row 15: Duplicate School ID - A user with this School ID already exists for this university. Each user must have a unique ID._").

**Story 1.6b: Asynchronous Import Processing**

-   **As an** Admin or Super Admin, **I want** a validated user CSV file to be processed as a background job, **so that** the import doesn't time out or degrade system performance.
-   **Depends on:** Story 1.6a
-   **Acceptance Criteria:**
    1.  After a file is successfully validated, the Admin or Super Admin can initiate the import process.
    2.  The import runs as an asynchronous job using the RQ worker.
    3.  A successful import creates records in the `users` table and assigns appropriate roles via the `user_roles` table.
    4.  New users are created with a default password based on their university-issued ID.
    5.  The **user who initiated the import** (either Admin or Super Admin) receives a notification upon completion of the import.

**Story 1.7: Super Admin User Management**

-   **As a** Super Admin, **I want** to be able to view, manage the status of, and trigger password resets for user accounts within a specific university, **so that** I can perform essential administrative actions in an emergency.
-   **Depends on:** Story 1.3, Story 1.5
-   **Acceptance Criteria:**
    1.  The Super Admin dashboard must include a "University Management" section listing all active universities.
    2.  Selecting a university navigates to a detailed management page for that institution.
    3.  This page must contain a "User Accounts" tab that lists all users associated with the university, with search and filter capabilities.
    4.  For each user, the Super Admin can view their current status (e.g., 'Active', 'Pending Verification', 'Locked').
    5.  The Super Admin must have an action to trigger a password reset for any user, which sends an email to the user with a secure, one-time password reset link.
    6.  The Super Admin must be able to manually change a user's status (e.g., from 'Active' to 'Locked').
    7.  All administrative actions taken on a user account must be recorded in an audit log for security and traceability.

**Story 1.8: Backup and Recovery Strategy**

-   **As a** Super Admin/DevOps Engineer, **I want** an automated backup and documented recovery procedure for the production database and user-uploaded files, **so that** we can recover from a disaster on the single VPS.
-   **Acceptance Criteria:**
    1.  An automated script performs nightly backups of the database.
    2.  An automated script performs nightly backups of the storage location for uploaded documents.
    3.  All backups are stored in a secure, off-server location.
    4.  A `RECOVERY.md` document in the project repository details the step-by-step procedure to restore the system from backups.

**Story 1.9: Provision and Configure External Services**

-   **Blocks:** Story 6.2
-   **As a** Project Lead, **I want** a designated human user to provision and configure all necessary external services, **so that** the development team has the required credentials to build and integrate dependent features.
-   **Acceptance Criteria:**
    1.  A human user (e.g., the Project Lead or a client representative) is explicitly assigned this responsibility.
    2.  Accounts for all required third-party services (e.g., Gemini API) are created.
    3.  All necessary API keys and credentials have been acquired.
    4.  Credentials are to be securely documented and provided to the development team.
-   **Dev Note:** This is a critical-path project management task, not a software development task. It blocks development on multiple features.

**Story 1.10: Implement Core API Middleware**

-   **Depends on:** Story 1.1, Story 1.2
-   **Blocks:** Story 1.3, Story 1.6a, Story 1.7
-   **As a** Developer, **I want** a set of shared API middleware to be implemented, **so that** all API requests have consistent logging, error handling, and database session management.
-   **Acceptance Criteria:**
    1.  A request logging middleware is created that logs key information (request ID, method, path, duration) in a structured JSON format.
    2.  A global error handling middleware is created that catches unhandled exceptions and returns a standardized JSON error response, including a `requestId`.
    3.  A middleware or dependency is created to manage the database session lifecycle per request.
    4.  A middleware adds a unique `X-Request-ID` to every request and response for log tracing.

**Story 1.11: Establish Frontend Mocking Infrastructure**

-   **Depends on:** Story 1.1
-   **Blocks:** Story 1.3, Story 1.4, Story 1.5, Story 1.6a
-   **As a** Frontend Developer, **I want** a mock server infrastructure to be established, **so that** I can develop and test UI components without a dependency on the live backend API.
-   **Acceptance Criteria:**
    1.  `msw` (Mock Service Worker) is integrated into the frontend (`apps/web`) development environment.
    2.  The mock server is enabled by default during local development (`pnpm dev`) and for all unit/integration tests (`vitest`).
    3.  Initial mock handlers are created for core authentication and user profile endpoints.
    4.  The frontend `README.md` is updated with instructions on how to create and manage mock handlers.

#### **Epic 2: Historical Data Onboarding & System Priming**

-   **Guiding Principle for this Epic:** "All import functionality—including the UI, APIs, and background jobs—must be built as a generic, multi-tenant feature from the ground up. The code should not contain any hardcoded logic specific to a single university. Every operation must be strictly scoped to the `university_id` of the authenticated Admin. We are building a reusable platform feature, not a one-time migration script."

**Stories:**

**Story 2.1: Manual Academic Structure Management**

-   **As an** Admin, **I want** a dedicated interface to manually create, view, update, and manage individual academic structure items, **so that** I can make granular additions or corrections without needing to perform a bulk import.
-   **Depends on:** Story 1.5
-   **Acceptance Criteria:**
    1.  The Admin dashboard contains a new "Academic Structure" management area.
    2.  Within this area, the Admin can perform full CRUD operations for **Departments, Programs, and Subjects.**
    3.  The UI enforces all relationships and constraints defined in the database schema.
    4.  All changes are logged for auditing purposes.

**Story 2.2: Background Job Monitoring Dashboard**

-   **As an** Admin, **I want** a centralized dashboard to view the status of all my background jobs (including data imports, report generation, and period cancellations), **so that** I can track progress and diagnose failures.
-   **Depends on:** Story 1.6b, Story 2.3, Story 2.4, Story 2.5, Story 3.6, Story 5.6
-   **Acceptance Criteria:**
    1.  A new "Job Monitor" page is added to the Admin dashboard.
    2.  The page provides a user-facing view of records from the `background_tasks` table that are associated with the Admin's university.
    3.  The list must display: **Job Type** (mapping the `job_type` enum, e.g., 'User Import'), **Source Filename** (if applicable, from `job_parameters`), **Submitted At** (`created_at`), **Status** (mapping the `status` enum), and a **Details/Download** link.
    4.  The table must support pagination and filtering by status.
    5.  For a job with status `failed` or `completed_partial_failure`, the 'Details/Download' link must trigger the download of an error report from the location specified in the job's `result_storage_path`.
    6.  A 'Cancel' button is available for any job that has a `queued` status.
-   **Dev Note:** The job lifecycle must include the statuses: `Queued`, `Processing`, `Completed_Success`, **`Completed_Partial_Failure`**, `Failed`, and `Cancelled`, which map to the `background_tasks` status enum.

**Story 2.3: Academic Structure Bulk Import**

-   **As an** Admin, **I want** to bulk import the university's entire academic structure from a CSV file, **so that** I can rapidly set up the foundational hierarchy.
-   **Depends on:** Story 2.1
-   **Acceptance Criteria:**
    1.  The "Academic Structure" management area includes a "Bulk Import" feature.
    2.  A downloadable CSV template is provided.
    3.  The asynchronous job validates the uploaded CSV, returning a comprehensive error report if issues are found, and does not proceed until errors are resolved.
    4.  A successful import correctly populates all relevant academic structure tables and is idempotent.
    5.  The admin receives a notification and the job status is updated on the "Job Monitor" page.
    6.  **A partially successful import (where only some batches fail) must result in a `Completed_Partial_Failure` status. The downloadable error report for such a job must contain only the rows from the failed batches, allowing the Admin to correct and re-upload only the problematic data.**
-   **Dev/QA Notes:** The Architect must define the precise CSV format. The asynchronous validation must prevent web server timeouts. QA will require 'bad' CSV files for testing.

**Story 2.4: Historical User & Enrollment Bulk Import**

-   **As an** Admin, **I want** to bulk import historical user and enrollment data from CSV files, **so that** past academic records are accurately reflected in the system.
-   **Depends on:** Story 2.1
-   **Acceptance Criteria & Notes:** Follows the same structure as Story 2.3 for importing users and enrollments.
-   **Acceptance Criteria:**
    1.  (All criteria from 2.3 apply)
    2.  ...
    3.  **A partially successful import (where only some batches fail) must result in a `Completed_Partial_Failure` status. The downloadable error report for such a job must contain only the rows from the failed batches, allowing the Admin to correct and re-upload only the problematic data.**

**Story 2.5: Historical Evaluation Records Bulk Import**

-   **As an** Admin, **I want** to bulk import past evaluation records (both numerical and open-ended) from a CSV file, **so that** historical feedback is available for analysis.
-   **Depends on:** Story 2.1
-   **Acceptance Criteria & Notes:** Follows the same structure as Story 2.3 for importing historical evaluations.
-   **Acceptance Criteria:**
    1.  (All criteria from 2.3 apply)
    2.  ...
    3.  **A partially successful import (where only some batches fail) must result in a `Completed_Partial_Failure` status. The downloadable error report for such a job must contain only the rows from the failed batches, allowing the Admin to correct and re-upload only the problematic data.**

**Story 2.6: Fine-Tune Sentiment Analysis Model for Cebuano & Code-Switching**

-   **As a** System/Data Scientist, **I want** the primary sentiment analysis model (XLM-RoBERTa) to be fine-tuned on Cebuano and code-switched language, **so that** its predictions are accurate and reliable.
-   **Depends on:** Story 2.5
-   **Acceptance Criteria:**
    1.  The fine-tuning script must be designed to consume a **pre-curated and labeled dataset** of evaluation records. The manual task of curating this dataset is a prerequisite.
    2.  The script can be executed via a CLI command.
    3.  The fine-tuned model must achieve its target accuracy metric on a held-out test set.
    4.  The final, versioned model artifact is integrated into the RQ worker environment.
-   **Dev/QA Notes:** The Architect must define the storage location for model artifacts. QA must have access to logs to verify accuracy. A post-import validation script must be created to check for data integrity (e.g., orphaned records) before this epic is considered complete.

**Story 2.7: Stuck Job Intervention**

-   **As an** Admin, **I want** to be able to 'Force Fail' a job that appears to be stuck in a 'Processing' state, **so that** I can resolve a system deadlock and investigate the issue.
-   **Depends on:** Story 2.2
-   **Dev Notes:**
    -   **Implementation Pattern:** The implementation should aim to create a generic, reusable pattern for the 'Force Fail' cleanup logic to avoid bespoke code for each job type.
    -   **Process Recommendation:** A technical spike is highly recommended for the riskiest parts of this feature (e.g., process termination and transaction rollbacks) to de-risk the main implementation.
-   **Acceptance Criteria:**
    -   **User Interaction**
        1.  The 'Force Fail' button on the 'Job Monitor' dashboard shall only become visible for a job in the 'Processing' state after a minimum configurable duration (e.g., 5 minutes) has passed.
        2.  Clicking 'Force Fail' must trigger a confirmation dialog explaining the action's consequences.
        3.  The UI on the "Job Monitor" page must update in near real-time to reflect the job's final 'Failed' status after the action is complete.
    -   **Core Backend Logic** 4. Upon confirmation, the backend must update the job's status to 'Failed'. The audit log for this event must be highly detailed, recording: the job ID, the admin who initiated the action, the job's runtime duration before termination, and the last known step or progress of the job if available. 5. The implementation must guarantee that forcing a job to fail also safely terminates the underlying worker process executing that job, preventing 'zombie' processes.
    -   **Safety & Resilience** 6. The 'Force Fail' mechanism must ensure that the job's operations are handled transactionally where possible. The backend logic must attempt to gracefully terminate and roll back any active database transaction to prevent data corruption. 7. If the force-failed job was managing a primary entity's status (e.g., a `period_cancellation_job`), the entity's status must be automatically reverted to its last known stable state (e.g., from 'Cancelling...' back to 'Active'). 8. After a 'Force Fail' is executed, the backend must perform a verification check to confirm that associated resources have been successfully reverted to a stable state. If this verification fails, the job must be moved to a special 'Cleanup Failed' state and flagged for immediate Super Admin review.
    -   **Testability** 9. In a non-production environment, a debug mechanism or test-only API endpoint must be created to allow a QA agent to simulate a stuck job, enabling verification of the entire 'Force Fail' workflow.

#### **Epic 3: Administrative Control Panel**

UX Note: To improve the first-time user experience, the "Evaluation Management" page should consider a guided wizard or checklist for new Admins, walking them through the `Create -> Activate -> Assign` sequence.

**Story 3.1: University Profile and Settings Management**

-   **As an** Admin, **I want** a settings page to manage my university's profile and key operational parameters, **so that** I can control core business logic without needing technical support.
-   **Depends on:** Story 1.5
-   **Acceptance Criteria:**
    1.  An "Institution Settings" page is available in the Admin dashboard.
    2.  The page displays the university's core profile information (Name, Address) in a read-only format.
    3.  The page provides an interface to view and edit values stored in the `university_settings` table that are associated with the Admin's university.
    4.  The following settings must be editable through this interface:
        -   **Quantitative Score Weight** (e.g., `score_weight_quantitative`)
        -   **Qualitative Score Weight** (e.g., `score_weight_qualitative`)
        -   **Recycled Content Similarity Threshold**
    5.  Input fields must be validated (e.g., score weights must sum to 1.0, threshold must be a percentage).
    6.  Saving the changes updates the corresponding records in the `university_settings` table and logs the action in the audit trail.
-   **Dev Note:** This interface is the primary mechanism for admins to control the newly architected configurable business rules. The front-end will fetch these settings upon login and use them to inform calculations and validation logic throughout the application.

**Story 3.2: Managing Form Criteria**

-   **As an** Admin, **I want** to add, edit, and reorder weighted criteria within a draft form template, **so that** I can structure the evaluation into logical sections.
-   **Depends on:** Story 3.1
-   **Acceptance Criteria:**
    1.  When editing a form template with a 'draft' status, I can add new criteria (e.g., "Teaching Methods," "Classroom Management").
    2.  Each criterion must have a `name` and a numerical `weight`.
    3.  The system must validate that the sum of all criteria weights for a single form template equals 100 before the form can be activated.
    4.  I can change the display order of criteria within the form.

**Story 3.3: Managing Form Questions**

-   **As an** Admin, **I want** to add Likert-scale and open-ended questions to the criteria within a draft form template, **so that** I can capture detailed feedback.
-   **Depends on:** Story 3.2
-   **Acceptance Criteria:**
    1.  Within a specific criterion, I can add multiple Likert-scale questions.
    2.  I can add open-ended questions to the form.
    3.  The system displays a warning if more than three open-ended questions are added but allows an override up to a maximum of eight.
    4.  I can set whether each question is required to be answered or optional.
    5.  At any point while editing a 'draft' template, I can select a "Preview" option that shows how the form will be rendered for evaluators.
    6.  While a form template is in a `draft` state, the system must automatically save any changes made by the Admin on a periodic basis (e.g., every 60 seconds) to prevent data loss.

**Story 3.4a: Form Template Activation & Duplication**

-   **As an** Admin, **I want** to activate, edit, and duplicate form templates, **so that** I can manage my forms efficiently.
-   **Depends on:** Story 3.3
-   **Acceptance Criteria:**
    1.  I can "Activate" a 'draft' template only if all validation rules are met (e.g., has name, criteria, questions, and weights sum to 100).
    2.  An **'active'** template remains **editable**. Editing an active form temporarily places it in an 'editing' state; if an edit is saved that causes the template to fail validation, its status must automatically revert to 'draft'.
    3.  The **"Duplicate"** function is available for any template to create a new 'draft' copy. When a new version is activated from a duplicate, the system may prompt the user to optionally archive the older version.
    4.  A form template with an **'assigned'** status **cannot be edited or archived**. Its status reverts to 'active' only after the `end_date_time` of the period it was assigned to has passed.
    5.  From the main list of templates, each 'active' template must have an **'Assign to Period'** action button that takes me directly to the 'Period Assignment' creation page with that template pre-selected.

**Story 3.5: Assigning Forms to Evaluation Periods**

-   **As an** Admin, **I want** to create and edit a scheduled evaluation period by assigning forms to evaluator groups, **so that** I can launch a clear and controlled evaluation.
-   **Depends on:** Story 3.4a
-   **Acceptance Criteria:**
    1.  On the "Evaluation Management" page, I can create or edit a Period Assignment. Any attempt to delete a dependent resource for an assigned period must be prevented.
    2.  The UI must gracefully handle cases where no 'active' forms are available by showing a helpful message and a link to the form creation page.
    3.  I must select a `school_term`, `assessment_period`, `start_date_time`, and `end_date_time`.
    4.  The system **must prevent** saving if the `start_date_time` is in the past or if the `end_date_time` is not after the `start_date_time`.
    5.  I must select a primary, **active form template** for **Student** evaluators using a clearly labeled dropdown ("Select Primary Form (for Students)").
    6.  Optionally, I can assign a second, different active form template for **Department Head** evaluators using a clearly labeled dropdown.
    7.  Before finalizing, the system must display a **visually explicit confirmation summary** of the assignment details. A "Share Read-Only Preview Link" button will be available on this summary for optional, external stakeholder sign-off.
    8.  I can edit any details of a Period Assignment at any time **before** its `start_date_time`. If I am editing a period when its start time passes, the system must prevent the save and inform me that the period is now active and locked.
    9.  Any "Delete" action on a planned period must trigger a confirmation dialog.
    10. Upon successful assignment, the status of the selected form template(s) is updated to 'assigned'.

**Story 3.6: Frontend - Initiate Soft Period Cancellation & Restoration**

-   **As an** Admin, **I want** to initiate a "soft" period cancellation that is restorable for 72 hours, **so that** I can safely correct a critical error with a clear window for reversal.
-   **Depends on:** Story 3.5
-   **Acceptance Criteria:**
    1.  A 'Cancel Period' action button is visible and enabled on the "Form & Period Management" page for any evaluation period that has an 'Active' status.
    2.  Clicking the 'Cancel Period' action must open a confirmation dialog designed for destructive actions.
    3.  The dialog must require the Admin to select a reason from a pre-defined dropdown list. If the 'Other (requires internal note)' option is selected, a text area for internal notes must become visible and mandatory.
    4.  The final 'Confirm Cancellation' button in the dialog must remain disabled until the Admin types the exact word 'CANCEL' into a confirmation text field.
    5.  Upon successful confirmation, an API call is made to the backend to initiate the soft cancellation.
    6.  Immediately after the API call, the status of the corresponding period in the UI list must change to a transitional 'Pending Cancellation' state, displaying a prominent countdown timer indicating the time remaining in the 72-hour restoration window.
    7.  While in the 'Pending Cancellation' state, a 'Restore Period' button must be visible and enabled for that row. All other actions (like 'Edit' or 'Cancel') must be disabled.
    8.  Clicking 'Restore Period' will trigger a confirmation dialog. Upon confirmation, a separate API call is made to the backend. On success, the UI updates to show the period's status has reverted to 'Active'.
    9.  Once the 72-hour grace period expires, the UI should automatically update the period's status to the permanent 'Cancelled' state, and the 'Restore Period' button must be removed.

**Story 3.7: Admin Management of Role-Specific Registration Codes**

-   **As an** Admin, **I want** to create, view, and manage role-specific registration codes, including setting and updating their maximum usage limits, **so that** I can control the user onboarding process.
-   **Depends on:** Story 1.5
-   **Developer Notes:**
    -   **Implementation Pattern:** The implementation should aim to create a generic, reusable pattern for the 'Force Fail' cleanup logic to avoid bespoke code for each job type.
    -   **Process Recommendation:** A technical spike is highly recommended for the riskiest parts of this feature (e.g., race condition handling) to de-risk the main implementation.
-   **Acceptance Criteria:**
    -   **Admin Interface & Functionality**
        1.  A "Registration Code Management" interface is available within the Admin's "User Management" page.
        2.  The interface displays a list of all registration codes, showing the code, its intended role, its usage count (`Current Uses / Max Uses`), and a status toggle (Active/Inactive).
        3.  An Admin can activate or deactivate a code using the status toggle.
        4.  An Admin can create a new code by selecting a role, setting a 'Max Uses' limit, and optionally setting an expiration date.
        5.  An Admin can regenerate an existing code, which archives the old one and creates a new one with the same role and limits.
        6.  An Admin can update the "Max Uses" limit for an existing code.
    -   **Security & Validation** 7. Registration codes must be generated as non-sequential, random, and sufficiently complex strings (e.g., `UNIV-ROLE-A4B8-C1D9`) to prevent guessing. 8. The API endpoints for code validation and user registration must be protected by a rate limiter to prevent rapid, automated account creation attempts. 9. When an admin attempts to update the 'Max Uses' for a code, the system must validate that the new value is not less than the 'Current Uses' and show an error if it is. 10. A deactivated or expired code cannot be used for new registrations.
    -   **Data Integrity & Traceability** 11. When a user successfully registers, the system must store a reference to the `registration_code_id` in the new user's record, creating a permanent, traceable link. 12. The process for checking and incrementing the 'Current Uses' of a code must be atomic to prevent race conditions from breaching the 'Max Uses' limit.

**Story 3.8: Backend - Process Soft Cancellation, Restoration, and Finalization**

-   **As a** System, **I want** to process a soft period cancellation by changing its state, provide a mechanism for restoration, and have a scheduled job to finalize the cancellation after the grace period expires, **so that** the process is safe, reversible, and eventually consistent.
-   **Depends on:** Story 3.6
-   **Dev Notes & QA Notes:**
    -   **Idempotency:** The developer must implement idempotency for all state-changing operations and background jobs.
    -   **Testing:** QA must create automated integration tests for the entire lifecycle: soft cancel, restore within the window, and automated finalization after the window expires.
-   **Acceptance Criteria:**
    1.  The backend API endpoint for cancellation must immediately update the `evaluation_periods` record's status to `pending_cancellation` and set a `cancellation_grace_period_ends_at` timestamp to 72 hours in the future.
    2.  Upon this state change, an asynchronous, idempotent job is enqueued to update all associated `evaluation_submissions` to an 'invalidated_pending_cancellation' state and to notify affected users.
    3.  A dedicated API endpoint for `POST /periods/{id}/restore` is created. This endpoint must validate that the current time is before the `cancellation_grace_period_ends_at`.
    4.  A successful restoration request reverts the period's status to `Active` and enqueues a second idempotent job to revert the status of associated submissions and notify users that the period is active again.
    5.  A separate, scheduled cron job (or equivalent) must run periodically (e.g., every hour). This job's responsibility is to query for `evaluation_periods` where the status is `pending_cancellation` AND the `cancellation_grace_period_ends_at` timestamp is in the past.
    6.  For each period found by the scheduled job, it will perform the final, permanent cancellation. This includes:
        -   Updating the period's status to `Cancelled`.
        -   Updating all associated submissions' status to `cancelled`.
        -   Performing any final data cleanup.
    7.  All state-changing operations (initial cancellation, restoration, and finalization) must be idempotent to ensure that if a job is retried, it does not cause errors or duplicate actions.

**Story 3.9: Duplicate an Existing Period Assignment**

-   **As an** Admin, **I want** to duplicate an existing evaluation period assignment, **so that** I can quickly schedule a new period using the same form configuration.
-   **Depends on:** Story 3.5
-   **Acceptance Criteria:**
    1.  An action to "Duplicate" is available for every entry in the list of Evaluation Periods.
    2.  Activating the "Duplicate" action navigates the user to the "Create Period Assignment" screen.
    3.  The form template selections (for both Students and Department Heads) are pre-populated with the values from the source period.
    4.  All date and time fields (`start_date_time`, `end_date_time`) are empty and must be filled by the user.
    5.  Saving the form successfully creates a new, independent `evaluation_periods` record in the database.
    6.  The original evaluation period that was duplicated remains completely unchanged.

**Story 3.10: Proactive Period Setup Notification**

-   **As an** Admin, **I want** to be notified when an evaluation period ends and be prompted to set up the next one, **so that** I don't forget and can efficiently roll over the configuration.
-   **Depends on:** Story 3.5
-   **Acceptance Criteria:**
    1.  Within 24 hours of an evaluation period's `end_date_time` passing, a notification is created for all Admins of that university.
    2.  The notification clearly states which period has ended and suggests the next logical period to set up (e.g., Midterm -> Finals).
    3.  The notification contains an action that takes the Admin directly to the pre-filled "Duplicate Period" creation screen.
    4.  The system correctly determines the next logical academic period based on the university's calendar structure.

#### **Epic 4: The Core Evaluation & Data Integrity Loop**

**Story 4.1: Evaluation Submission**

-   **As an** Evaluator (Student or Department Head), **I want** to select a faculty member and submit a complete evaluation during an active evaluation period, **so that** I can provide my feedback on their performance.
-   **Depends on:** Story 3.5
-   **Acceptance Criteria:**
    1.  **For a user with the 'Student' role:** My dashboard displays a list of faculty members based on the `subject_offerings` I am enrolled in for the current evaluation period.
    2.  **For a user with the 'Department Head' role:** My dashboard displays a list of all faculty members who are assigned to the department I lead.
    3.  Selecting a faculty member displays the correct, assigned evaluation form.
    4.  At the top of the evaluation form, a message and a visible countdown timer are displayed, indicating the minimum time required before submission.
    5.  For each open-ended question, a real-time word count is displayed as I type.
    6.  The UI provides a visual cue if the word count for a response is below the configured minimum or above the maximum.
    7.  The "Submit" button remains disabled until the countdown timer reaches zero and all _required_ questions meet their respective validation rules (including minimum word count).
    8.  Upon clicking "Submit," the system saves my answers, linked to a new record in the `evaluation_submissions` table.
    9.  Once an evaluation is submitted, it is removed from my list of pending evaluations for that period.

**Story 4.2: Pre-Submission Nudge for Low-Effort Ratings**

-   **As an** Evaluator, **I want** to be gently prompted if all my numerical ratings are the same, **so that** I am encouraged to provide more thoughtful and specific feedback.
-   **Depends on:** Story 4.1
-   **Acceptance Criteria:**
    1.  On the evaluation form, before the "Submit" button is clicked, the system performs a client-side check on all provided Likert-scale scores.
    2.  If the variance of all scores is zero (i.e., they are all the same number), a temporary, dismissible 'toast' notification appears.
    3.  The message text is concise, such as: "To provide the most helpful feedback, consider adding specific examples in the comments below."
    4.  The message does not prevent me from submitting the evaluation.

**Story 4.3: Automated "Low-Confidence" Flagging**

-   **As an** Admin, **I want** the system to automatically flag submissions that appear to be low-effort, **so that** I can review them for data quality.
-   **Depends on:** Story 4.1
-   **Acceptance Criteria:**
    1.  Immediately after a user submits an evaluation, a server-side check is performed.
    2.  A submission is flagged with a reason of "Low-Confidence" if it meets **both** of the following criteria: (A) the variance of all Likert-scale scores is zero, **AND** (B) the submission contains no meaningful qualitative feedback (i.e., all _optional_ open-ended questions were left blank).
    3.  If a submission is flagged, a new record is created in the `flagged_evals` table for administrative review.

**Story 4.4: Asynchronous "Recycled Content" Flagging**

-   **As an** Admin, **I want** the system to automatically detect and flag evaluations where an evaluator reuses their own text, **so that** I can ensure the originality of feedback.
-   **Depends on:** Story 4.1
-   **Acceptance Criteria:**
    1.  Upon a successful evaluation submission, a job is added to the asynchronous work queue.
    2.  The background job compares the submitted open-ended text against **that same evaluator's** previous submissions across all evaluation periods.
    3.  If the text has over 95% similarity to one of their previous submissions, a "Recycled Content" flag is created for the evaluation.
    4.  The notification sent to the student for recycled content must clearly explain that reused text was detected and state the importance of providing original feedback for each unique evaluation.
-   **`Dev Note:`** The integrity report endpoint must return a `highlights` array where each element includes the originating `question_id`, optional `text_answer_id`, zero-based `start_index`/`end_index`, and an anonymized `snippet`. Multiple fragments per question must be supported so the resubmission screen can render distinct spans without re-fetching worker data.

**Story 4.5a: Flagged Evaluation Dashboard (View Only)**

-   **As an** Admin, **I want** a dashboard to view a list of all flagged evaluations and see the detailed reasons for each flag, **so that** I can assess the queue and understand the issues.
-   **Depends on:** Story 4.3, Story 4.4
-   **Acceptance Criteria:**
    1.  The Admin dashboard includes a page that lists all evaluations with a 'pending' flag.
    2.  The list displays the faculty member, the reason(s) for the flag (e.g., "Low-Confidence"), and the submission date.
    3.  Selecting a flagged evaluation shows a detailed view with a side-by-side comparison of the submission's numerical ratings and its open-ended text.

**Story 4.5b: Flagged Evaluation Processing**

-   **As an** Admin, while viewing a flagged evaluation, **I want** to be able to Approve, Archive, or Request Resubmission, **so that** I can process the queue and maintain data integrity.
-   **Depends on:** Story 4.5a
-   **Acceptance Criteria:**
    1.  From the detailed view, I have three actions: **Approve**, **Archive**, or **Request Resubmission**.
    2.  Choosing **"Approve"** resolves the flag and ensures the submission data is included in all aggregate calculations.
    3.  Choosing **"Archive"** marks the submission as 'archived' and excludes it from all aggregate calculations. The submission is soft-deleted and recoverable for 30 days.
    4.  Archiving a submission requires the Admin to provide a reason, which is included in the anonymous notification sent to the student.
    5.  Choosing **"Request Resubmission"** marks the original submission as invalid (to be excluded from calculations) and triggers an anonymous notification for the student to submit a new evaluation.
    6.  _Dev Note:_ All actions on a flagged evaluation must gracefully handle concurrent requests from multiple admins.
    7.  The system must prevent a 'Request Resubmission' action on an evaluation that has already been resubmitted once. If a second submission is still unsatisfactory, the Admin's only options are 'Approve' or 'Archive'.
    8.  A resubmission can be completed by the student within the 48-hour grace period defined in FR12.

**Story 4.6: Viewing Resolved Flags**

-   **As an** Admin, **I want** to be able to view a history of evaluations that I have already resolved, **so that** I can maintain an audit trail and reference past decisions.
-   **Depends on:** Story 4.5b
-   **Acceptance Criteria:**
    1.  The flagged evaluations dashboard has a separate tab or filter to view 'Resolved' items.
    2.  The resolved list shows the submission details, the original flag reason, the action taken (Approved, Archived, etc.), who resolved it, and the date of resolution.
    3.  This view is read-only.

#### **Epic 5: Data Processing & Insights Visualization**

**Story 5.1: Asynchronous Quantitative Analysis Job**

-   **As a** System, **I want** to process the numerical Likert-scale answers from a submitted evaluation in a background job, **so that** the raw scores are calculated and stored for aggregation without blocking the user.
-   **Depends on:** Story 4.1
-   **Acceptance Criteria:**
    1.  When a new, valid evaluation submission is ready for processing, a job is added to the asynchronous work queue (Redis+RQ).
    2.  **Question-Level Analysis:** The job must calculate the **median** score for each individual Likert-scale question in the submission.
    3.  **Criterion-Level Analysis:** The job must then calculate the **mean** of the question medians for each criterion, resulting in an average score for each section of the evaluation form.
    4.  **Overall Raw Score Calculation:** The job must apply the weights assigned to each criterion (from the `evaluation_criteria` table) to the criterion-level mean scores, calculating a final weighted mean. This result is the `quant_score_raw`.
    5.  The processed results, including per-question medians and per-criterion scores, are stored in the `numerical_aggregates` table, ready for the final normalization step in a subsequent story.
    6.  The job is marked as complete, and any errors during processing are logged.

**Story 5.2: Asynchronous Qualitative Analysis Job**

-   **As a** System, **I want** to process the open-ended feedback from a submitted evaluation in a background job, **so that** qualitative insights like sentiment and key themes are extracted and stored for aggregation.
-   **Depends on:** Story 4.1
-   **Acceptance Criteria:**
    1.  When a new, valid evaluation submission is processed, a job is added to the asynchronous work queue (Redis+RQ) to handle its open-ended answers.
    2.  The job retrieves the text from the `evaluation_open_ended_answers` table for the given submission.
    3.  **Sentiment Analysis:** The job must use the **fine-tuned XLM-ROBERTa** model to analyze the text. The results must be saved to the `open_ended_sentiments` table and must include:
        -   The final `predicted_sentiment_label` (e.g., 'positive', 'neutral', or 'negative').
        -   The `predicted_sentiment_label_score` (the probability of the predicted label).
        -   The full sentiment distribution: `positive_score`, `neutral_score`, and `negative_score`.
        -   The `accuracy` and `confidence` scores for the model's prediction.
    4.  **Keyword Extraction:** The job must use the **KeyBERT** model to extract relevant keywords and phrases. The results are saved to the `open_ended_keywords` table and must adhere to the following:
        -   Only keywords with a `relevance_score` above a configurable threshold are saved to prevent irrelevant results.
        -   The `relevance_score` itself must be stored with each keyword.
    5.  The processed qualitative results are now ready for the final aggregation and normalization step (Story 5.3).
    6.  The job is marked as complete, and any processing errors are logged.

**Story 5.3: Final Aggregation and Normalization Job**

-   **As a** System, **I want** to run a final aggregation and normalization job, **so that** the individual quantitative and qualitative analysis results are combined into standardized, comparable scores for reporting and visualization.
-   **Depends on:** Story 5.1, Story 5.2
-   **Acceptance Criteria:**
    1.  The job is triggered after the prerequisite quantitative (5.1) and qualitative (5.2) analysis jobs for a submission or batch of submissions are successfully completed.
    2.  **Cohort Calculation:** The job must first calculate the cohort baseline statistics (**mean μ** and **standard deviation σ**) for the relevant comparison group (e.g., department-level) for both the `quant_score_raw` and `qual_score_raw` values.
    3.  **Z-Score Calculation:** Using the cohort baselines, the job must calculate the normalized **`z_quant`** and **`z_qual`** scores for each faculty evaluation, representing how many standard deviations they are from the cohort mean.
    4.  **Final Weighted Score:** The job must calculate the **`final_score_60_40`** by applying the 60/40 weighting to the z-scores as defined in the non-functional requirements.
    5.  **Data Persistence:** The job must update the `numerical_aggregates` and `sentiment_aggregates` tables with all calculated values, including z-scores, the final weighted score, and cohort details (e.g., `cohort_n`, μ, σ).
    6.  **Period Finalization:** The job must correctly handle period finalization. When an Admin triggers the "Finalize and Lock Period" function, this job runs a final time for that period and sets the `is_final_snapshot` flag to `true` for all relevant records, preventing them from being overwritten.
    7.  The job is marked as complete, and any errors are logged.

**Story 5.4: Initial Batch Processing of Historical Data**

-   **As an** Admin, **I want** to trigger a one-time batch job to process all imported historical evaluation data using the newly built analysis pipeline, **so that** the system's dashboards are populated with a rich, longitudinal dataset.
-   **Depends on:** Story 2.5, Story 5.1, Story 5.2, Story 5.3
-   **Acceptance Criteria:**
    1.  The Admin dashboard provides an action to start the historical data processing job.
    2.  The job correctly identifies and queues all records imported via Epic 2 for processing.
    3.  The job uses the analysis engines built in stories 5.1, 5.2, and 5.3 to process the historical data.
    4.  Upon completion, the `numerical_aggregates` and `sentiment_aggregates` tables are populated with the historical results.
    5.  The Admin who initiated the job receives a notification upon completion.

**Story 5.5: Dashboard Data Visualization**

-   **As a** User (Faculty, Department Head, or Admin), **I want** to view the processed and aggregated evaluation results on my role-specific dashboard, **so that** I can gain clear, visual insights into performance.
-   **Depends on:** Story 5.3, Story 5.4
-   **Acceptance Criteria:**
    1.  The API must implement a **hybrid data retrieval strategy**: For finalized/locked evaluation periods, data is fetched from aggregate tables; for the current, provisional period, data is calculated on-the-fly and cached.
    2.  The main dashboard must display a **word cloud** of keywords, with a user action to switch between a "combined" view and separate views for **positive, neutral, and negative** keywords.
    3.  The dashboard must display **bar charts** for sentiment and numerical breakdowns, with a user action to switch between a "side-by-side" layout and a "detailed" vertical layout with specific KPIs.
    4.  The **Department Head and Admin dashboards** must implement the "mode-switching" functionality, allowing them to view aggregated data for a whole department or drill down to a specific faculty member's results.
    5.  To protect evaluator anonymity, the UI must prevent the viewing of raw open-ended comments associated with a chart or data point unless the total number of underlying responses meets a defined minimum threshold of 3 or more.
    6.  All visualizations must clearly indicate when data is **"Provisional"** versus **"Final."**.
    7.  All dashboards must clearly label and visually distinguish between analytics derived from **'Imported Historical Data'** versus **'Live Proficiency Data'**.

**Story 5.6: Evaluation Report Generation and Export**

-   **As a** User (Faculty, Department Head, or Admin), **I want** to use a "Report Center" to generate, track, and download comprehensive evaluation results, **so that** I can easily archive and analyze data offline.
-   **Depends on:** Story 5.5
-   **Acceptance Criteria:**
    1.  A "Report Center" link in the side navigation leads to a dedicated page with two main areas: "Generate Report" and "My Reports".
    2.  The "Generate Report" area allows a user to select a predefined report type and apply relevant filters.
    3.  The system will use smart logic to either generate simple reports synchronously (immediate download) or enqueue complex reports as an asynchronous background job, creating a corresponding record in the `background_tasks` table.
    4.  The "My Reports" area acts as an inbox, providing a user-facing view of their records in the `generated_reports` table. It must list all initiated reports with their current `status` (e.g., 'Generating', 'Ready', 'Failed').
    5.  Users receive a notification (via the centralized notification system) when an asynchronous report's status changes to 'Ready', and they can download the file from the `storage_path` via the "My Reports" list.
    6.  The system supports exporting reports in both **PDF** (via WeasyPrint) and **CSV/Excel** (via pandas) formats, as specified in the `file_format` field of the report record.

#### **Epic 6: AI-Powered Actionable Intelligence**

**Dev Note:** The implementation must include specific monitoring for the AI pipeline, tracking metrics like average suggestion generation time, model error rate, and Redis queue length to identify performance bottlenecks early.

**Story 6.1: AI Assistant Page and Controls**

-   **As a** Faculty or Department Head, **I want** to access a dedicated "AI Assistant" page with filters and pre-defined actions, **so that** I can easily set the context for generating performance suggestions.
-   **Depends on:** Story 5.5
-   **Acceptance Criteria:**
    1.  A new navigation link for the "AI Assistant" must be added to the main side panel, accessible **only** to users with 'Faculty' or 'Department Head' roles.
    2.  The page must include filter controls allowing the user to select the `school_term` and `assessment_period` for the data they wish to analyze.
    3.  For users with the 'Department Head' role, the page must also include the **mode-switching** component, allowing them to toggle between their own personal results, department-wide results, or the results of a specific faculty member in their department.
    4.  Instead of a single "generate" button, the page must feature a set of **pre-defined, button-based actions** (e.g., "Generate Strengths & Weaknesses Report," "Suggest Improvements for Lowest-Rated Criterion").
    5.  A small, permanent disclaimer must be visible on the page, with text like: _"This AI provides suggestions based on data patterns. Please use them as a starting point for reflection, not as a final judgment."_
    6.  The main content area is initially empty or displays a placeholder instructing the user to select their filters and choose a generation action.
    7.  Once a report is displayed, a "Start Over" or "Clear Results" button must become visible. Clicking this button will clear the results from the view and re-enable all action buttons.

**Story 6.2: AI Suggestion Generation**

-   **As a** Faculty or Department Head, **I want** to click a pre-defined action button and have the system generate relevant suggestions, **so that** I can receive AI-powered insights based on my selected data.
-   **Depends on:** Story 1.9, Story 6.1
-   **Acceptance Criteria:**
    1.  When an action button is clicked, the frontend sends a request to a dedicated backend endpoint, including the selected filters (term, period, user/department mode).
    2.  The backend retrieves all necessary processed data for the given context, including records from `numerical_aggregates`, `sentiment_aggregates`, and the top 5 positive/negative `open_ended_keywords`.
    3.  A structured, context-rich prompt is constructed for the **Gemini API**. This prompt must adhere to the **Persona-Context-Task-Format** framework and must instruct the model to adopt a constructive "academic coach" persona.
    4.  While the backend is processing the request, all action buttons on the 'AI Assistant' page **must be disabled** and display a loading indicator.
    5.  If the model fails to generate a response or times out, the API must return a specific error (e.g., 503 Service Unavailable), and the frontend must display a user-friendly message.
    6.  The generated suggestions are returned to the frontend and displayed clearly in the main content area of the "AI Assistant" page.

**Story 6.3: Saving and Viewing Suggestion History**

-   **As a** Faculty or Department Head, **I want** to save generated suggestions and view a history of my past requests, **so that** I can track insights and progress over time.
-   **Depends on:** Story 6.2
-   **Acceptance Criteria:**
    1.  Once suggestions are displayed, a "Save to History" button becomes available.
    2.  Clicking "Save" sends the generated text and its context to the backend, creating a new record in the `ai_suggestions` table.
    3.  After a suggestion is successfully saved, the "Save to History" button **must change to a 'Saved' state** (e.g., icon and text change) and become disabled for the current report.
    4.  The "AI Assistant" page must contain a "History" tab or section that displays a list of previously saved suggestions, showing the date, context, and a preview.
    5.  Selecting a historical item displays the full saved report.

**Story 6.4: Exporting AI Suggestions**

-   **As a** Faculty or Department Head, **I want** to download my generated AI suggestions as a professional-looking document, **so that** I can easily share, print, or archive these insights for my records.
-   **Depends on:** Story 6.2
-   **Acceptance Criteria:**
    1.  When AI suggestions are displayed, a "Download as PDF" button is visible.
    2.  Clicking the button calls `POST /api/v1/ai/suggestions/{id}/export`, sending the rendered `content_markdown` plus a `context` payload that includes the suggestion title, generated timestamp, and any active filters (term, department, faculty, course, and assessment period).
    3.  The backend uses the **WeasyPrint** library to render the content into a formatted PDF document that places the title and timestamp in the header and prints the filter summary ahead of the full suggestion text.
    4.  The response streams the PDF back to the browser with `Content-Type: application/pdf` and an `attachment` `Content-Disposition` filename such as `ai-suggestion-<timestamp>.pdf` so standard download prompts appear.
    5.  Each export request is rate limited to 5 attempts per user per 15 minutes to protect the shared WeasyPrint worker pool and match the AI run throttles.
    6.  Successful exports append an `AI_SUGGESTION_EXPORTED` entry to the audit log, linking to the originating suggestion so history views show the export trail.

#### **Epic 7: Support & Documentation**

**Story 7.1: User-Facing Help Documentation**

-   **As a** new User (Admin, Faculty, or Student), **I want** access to clear and simple help documentation, **so that** I can independently learn how to use the platform's key features without needing direct support.
-   **Acceptance Criteria:**

    1.  A searchable help guide or FAQ section is accessible within the application.
    2.  The documentation covers core user flows for each major role.
    3.  The documentation is written in clear, non-technical language.
