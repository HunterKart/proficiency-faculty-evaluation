# Proficiency Product Requirements Document (PRD)

---

### **Section 1: Goals and Background Context**

#### **Goals**

-   [cite_start]**Develop "Proficiency," a multi-tenant SaaS web platform** to modernize the faculty evaluation process for educational institutions, starting with the University of Cebu - Lapu-Lapu and Mandaue[cite: 57, 78].
-   [cite_start]**Implement an AI-powered analysis engine** that automatically processes qualitative feedback from students and department heads to provide sentiment analysis, keyword extraction, and generate actionable, data-driven suggestions for improvement[cite: 49, 57].
-   [cite_start]**Ensure high data quality and evaluation integrity** through automated, server-side checks that flag low-effort submissions and detect recycled content[cite: 94, 3377, 3385].
-   [cite_start]**Provide highly dynamic and customizable evaluation forms** that allow administrators to tailor evaluation criteria, questions, and scoring to diverse and changing institutional needs[cite: 50, 82].
-   [cite_start]**Deliver intuitive, role-based dashboards and visualizations** to make evaluation results easy to interpret for faculty, department heads, and administrators, supporting continuous faculty development and institutional decision-making[cite: 50, 336].

#### **Background Context**

[cite_start]Existing faculty evaluation systems, particularly within the Philippines and at the target institution, suffer from significant limitations[cite: 18, 22]. [cite_start]These systems often rely on static forms that cannot adapt to changing criteria and over-emphasize quantitative Likert scores while failing to extract meaningful insights from valuable open-ended feedback[cite: 13, 20]. [cite_start]The analysis of this textual feedback is often a manual, time-consuming, and error-prone process, resulting in low-quality, unactionable results that do little to support genuine faculty growth[cite: 24].

"Proficiency" is designed to address these critical gaps. [cite_start]It is a modern SaaS platform that leverages an AI pipeline to automate the deep analysis of textual feedback, providing insights into sentiment and key themes[cite: 49]. [cite_start]By combining this with robust integrity checks, customizable forms, and role-based data visualization, Proficiency aims to transform faculty evaluation from a burdensome administrative task into a powerful tool for continuous professional development and educational excellence[cite: 53].

#### **Change Log**

| Date       | Version | Description                                                       | Author   |
| :--------- | :------ | :---------------------------------------------------------------- | :------- |
| 2025-09-28 | 2.0     | Final PRD with all 5 epics and elicitation refinements.           | John, PM |
| 2025-09-28 | 1.0     | Initial PRD draft based on Project Brief and Capstone Manuscript. | John, PM |

---

### **Section 2: Requirements**

#### **Functional Requirements**

-   **FR1: User and University Management**
    -   [cite_start]The system shall support five user roles: **Students, Faculty, Department Heads, Admins, and Super Admins**[cite: 108, 110].
    -   [cite_start]For V1, user creation will be limited to two methods: 1) **Admin/Super Admin bulk import** via CSV/Excel and 2) **Self-registration using a valid, university-provided invitation token**[cite: 112, 2686]. The "evidence-based" manual sign-up is deferred to a post-V1 release.
    -   [cite_start]**Super Admins** shall manage the university registration and approval lifecycle[cite: 364, 808].
-   **FR2: Dynamic Evaluation Form & Period Management**
    -   [cite_start]Admins shall have the ability to **create, modify, and manage dynamic evaluation form templates**[cite: 83, 1118].
    -   [cite_start]Admins shall **assign form templates to specific evaluation periods**, defined by school year, semester (1st, 2nd, Summer), and assessment period (Midterm, Finals)[cite: 1141].
    -   The system shall enforce a business rule preventing the assignment of a new evaluation form template once an evaluation period is already ongoing.
-   **FR3: Evaluation Submission & Integrity**
    -   [cite_start]The system must implement a **"Pre-Submission Nudge,"** a non-blocking UI message to encourage users with low-variance Likert scores to provide written examples[cite: 4857].
    -   [cite_start]A submission must be automatically flagged with **"Low-Confidence"** if it contains both low-variance Likert scores AND short or empty open-ended answers[cite: 4858].
    -   [cite_start]The system shall run an asynchronous job to detect and flag **"Recycled Content"** that has over 95% similarity to previous submissions[cite: 4866, 4867].
-   **FR4: Flagged Evaluation Workflow**
    -   [cite_start]The system must automatically flag evaluations for data inconsistencies, such as a **sentiment-coherence mismatch**[cite: 94].
    -   [cite_start]Admins shall have a dedicated interface to review all flagged evaluations[cite: 318, 1324].
    -   Admins must be able to resolve a flagged evaluation by choosing one of three actions: **Approve**, **Reject**, or **Request Resubmission**.
    -   **FR4.1:** The notification sent to a Student for a rejected evaluation **must be anonymous** and clearly state the reason for rejection to guide them in providing a better resubmission.
    -   **FR4.2:** The Admin's review dashboard for flagged evaluations must provide a **side-by-side comparison** of the submission's numerical ratings and its open-ended text.
-   **FR5: Data Analysis Pipeline**
    -   [cite_start]All evaluation submissions shall be processed asynchronously via a **job queue (Redis+RQ)**[cite: 4865].
    -   [cite_start]The pipeline must separate analysis into a **Quantitative Layer** and a **Qualitative Layer**[cite: 4875].
    -   [cite_start]A final layer shall perform **Normalization and Aggregation** to combine scores and prepare data for visualization[cite: 269].
    -   **FR5.1:** Evaluation submissions with a status of 'rejected' or 'pending review' **must be excluded** from all aggregate calculations.
-   **FR6: AI-Powered Analysis and Insights**
    -   [cite_start]The system must perform automated **sentiment analysis** (Primary Model: XLM-ROBERTa) and **keyword extraction** (KeyBERT)[cite: 49, 96, 186].
    -   [cite_start]A dedicated **"AI Assistant" page** shall be available to Faculty and Department Heads to generate reports and suggestions from processed data using the Flan-T5 model[cite: 4883, 4885, 4886, 4887, 4888, 4889].
-   **FR7: Dashboards and Visualizations**
    -   The system shall present data using specific visualizations: **Word Clouds, Bar Charts, and Performance Trend Line Charts**. [cite_start]Admins will also have access to an **Evaluation Submission Behavior Line Chart**[cite: 91].
    -   [cite_start]Department Heads and Admins must be able to switch between different data views or **"modes"** (e.g., department-wide, specific faculty results)[cite: 1019, 1056].
-   **FR8: Provisional and Finalized Reporting Workflow**
    -   All reports for an active review period shall be marked as **"Provisional."**
    -   When an Admin approves a flagged evaluation, an asynchronous job must **recalculate the provisional aggregates** for the affected parties.
    -   [cite_start]Admins shall have a function to **"Finalize and Lock Period,"** which runs a final aggregation and sets the `is_final_snapshot` flag to `true`[cite: 2882, 2913].

#### **Non-Functional Requirements**

-   [cite_start]**NFR1: Architecture:** The system shall be a multi-tenant SaaS web platform with a modular, scalable, and asynchronous architecture[cite: 49, 127, 4865].
-   [cite_start]**NFR2: Data Integrity and Scoring:** The overall evaluation score must be calculated using a weighted scheme: 60% from Likert-scale data and 40% from textual feedback analysis[cite: 90].
-   [cite_start]**NFR3: Performance:** Access to AI-generated suggestions shall be restricted to Faculty and Department Heads to manage performance[cite: 103, 104, 105].
-   [cite_start]**NFR4: Security:** The system must implement robust user registration and authentication protocols[cite: 108].
-   **NFR5: Extensibility and Research:** The V1 production system will exclusively use the fine-tuned XLM-ROBERTa model. [cite_start]For academic comparison, a separate, non-production script or environment will be created to benchmark baseline models (VADER, Naïve Bayes, mBERT)[cite: 97, 98].
-   **NFR6: System Calibration:** The automated flagging algorithms must be calibrated to minimize false positives and ensure the volume of flagged evaluations is manageable for Admins.

---

### **Section 3: User Interface Design Goals**

#### **Overall UX Vision**

The user experience will embody **Modern, Data-Centric Professionalism**. The interface must feel clean, intuitive, and trustworthy, visually communicating a significant upgrade from traditional university systems. The design should prioritize clarity and ease-of-use, presenting complex evaluation data through simple, digestible visualizations. The design should actively avoid the cluttered, table-heavy, and visually dated aesthetic common in traditional enterprise portals. **Clarity and intuitive data visualization are the primary goals.**

#### **Core Screens and Views**

-   **Students:** Login, Dashboard (view teachers to evaluate), Evaluation History, Profile Management.
-   **Faculty:** Login, Dashboard (view personal results), Evaluation Insights, Performance Trends, Report Generation, AI Suggestion Page, Profile Management.
-   **Department Heads:** All Faculty views, plus department-level result views and the ability to evaluate faculty.
-   **Admins:** Similar views as Department Heads (institutional, department, and faculty level), but with no AI Suggestion Page. Plus: Review Flagged Evaluations, Form & Period Management, and Academic Structure Management.
-   **Super Admins:** Login, Dashboard (platform metrics), University Management, User Management, Profile Management.

#### **Key Interaction Paradigms**

-   **Card-Based Layout:** Content will be organized into distinct cards with rounded corners and subtle shadows.
-   **Data-First Dashboards:** The primary landing page for all roles will be a dashboard that immediately surfaces relevant data.
-   **Responsive Sidebar Navigation:** A consistent, collapsible sidebar will serve as the primary navigation method.
-   **Contextual Clarity & Consistency:** The UI must always provide clear indicators of the user's current view (e.g., "Viewing: Department of IT Results"). The modern design aesthetic must be applied consistently across all parts of the application.

---

### **Section 4: Technical Assumptions**

#### **Repository Structure**

A **Monorepo** is the assumed structure to simplify development and deployment. The Architect must ensure the monorepo has clear internal package boundaries and that the CI/CD pipeline is optimized to build only changed services.

#### **Service Architecture**

The architecture will be a **simple monolith** consisting of a single FastAPI backend API and a single RQ background worker process.

#### **Additional Technical Assumptions**

-   **Technology Stack:** The core stack is defined as **React/TypeScript**, **Python/FastAPI**, and **MySQL/MariaDB**.
-   **API Style:** The API will be primarily synchronous to maintain simplicity, with asynchronous methods used only where a clear benefit exists.
-   **Real-time Functionality:** Real-time updates will be implemented via **frontend polling**.
-   **AI/ML Models:** All AI models will be run via **local inference**.
-   **Deployment Target:** The application will be deployed to a **single VPS (Ubuntu)**, with all services managed via **Docker Compose**.
-   **Resource Management:** The Docker configuration must implement resource limits on the worker container to protect system stability.
-   **State Management:** Large-scale global state libraries are out of scope. React's **Context API** will be used for minimal global UI state.
-   **Disaster Recovery:** The Architect must define a clear disaster recovery plan for the single VPS deployment in the `architecture.md`.

---

### **Section 5: Epic List**

-   **Epic 1: Platform Foundation & University Onboarding**
    -   **Goal:** To establish the core technical infrastructure, multi-tenant foundation, and the complete administrative workflow for a Super Admin to onboard a new university, manage its lifecycle, and provision its user accounts via bulk import. This epic delivers the initial, foundational value of a ready-to-configure university tenant.
-   **Epic 2: Administrative Control Panel**
    -   **Goal:** To provide University Admins with the complete toolset to manage the evaluation process, including the dynamic form builder and evaluation period scheduling.
-   **Epic 3: The Core Evaluation & Data Integrity Loop**
    -   **Goal:** To enable students and department heads to submit high-quality evaluations, supported by robust, automated data integrity checks and a complete administrative review workflow.
-   **Epic 4: Data Processing & Insights Visualization**
    -   **Goal:** To implement the asynchronous data analysis pipeline and provide all user roles with intuitive, role-based dashboards featuring clear data visualizations of evaluation results.
-   **Epic 5: AI-Powered Actionable Intelligence**
    -   **Goal:** To empower faculty and department heads with advanced, AI-generated suggestions and downloadable reports that translate evaluation data into actionable insights for professional development.

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

**Story 1.2: Database and AI Environment Setup**

-   **As a** Super Admin/Developer, **I want** the database schema to be initialized and the AI model environment to be prepared, **so that** the core data structures are in place and future AI-related development is streamlined.
-   **Acceptance Criteria:**
    1.  A database migration tool is integrated into the backend service.
    2.  An initial migration script is created that generates all necessary tables as defined in the provided `Database-Schema-Data-Dictionary-of-Proficiency.pdf`.
    3.  The migration can be successfully run via a command within the local Docker environment.
    4.  A dedicated `Dockerfile` for the RQ worker is created, which installs all required Python libraries for the AI/ML models (XLM-ROBERTa, KeyBERT, Flan-T5, etc.) to prevent slow builds in later epics.

**Story 1.3: Super Admin Authentication**

-   **As a** Super Admin, **I want** to securely log in to a dedicated super admin dashboard, **so that** I can manage the platform.
-   **Acceptance Criteria:**
    1.  A login form is available for Super Admins.
    2.  The system authenticates credentials against the `super_admins` table.
    3.  After successful password validation, the system prompts the Super Admin to enter their 6-digit PIN code for multi-factor authentication.
    4.  Upon successful PIN verification, the user is redirected to the Super Admin dashboard.
    5.  Failed login attempts (either password or PIN) display a clear error message.
    6.  **Developer Note:** The initial Super Admin account will be created via a secure, one-time database seeding script that is run manually upon initial deployment.

**Story 1.4: University Registration Request Submission**

-   **As an** incoming University Admin, **I want** to submit a registration request with my university's details and supporting documents, **so that** our institution can be onboarded to the Proficiency platform.
-   **Acceptance Criteria:**
    1.  A public-facing registration form is available on the application's landing page.
    2.  The form must capture all required institutional and contact person details as specified in the `university_registration_requests` table.
    3.  The form allows for the upload of one or more supporting documents (e.g., accreditation proof).
    4.  Upon successful submission, a record is created in the `university_registration_requests` table with a status of 'submitted', and the Super Admin team is notified.

**Story 1.5: University Request Review Workflow**

-   **As a** Super Admin, **I want** to view and manage a queue of pending university registration requests, **so that** I can approve or reject new institutions.
-   **Acceptance Criteria:**
    1.  The initial Super Admin dashboard must display summary cards for 'Active Universities,' 'Total Users,' and 'Pending Requests'.
    2.  The main component of the dashboard is a table listing all pending university registration requests. Each row in the table is clickable, leading to a detailed view of the specific request.
    3.  Approving a request creates a new record in the `universities` table, creates an initial `Admin` account in the `users` table, and updates the request status to 'approved'.
    4.  Upon approval, an email is sent to the `contact_person_email` containing a confirmation message and a unique link to verify their new Admin account and set their password.
    5.  Rejecting a request prompts for a reason and triggers an email notification to the applicant with the reason for rejection.
    6.  The login page, when encountering an unverified Admin account, displays an error message and a 'Resend Verification Email' button that re-triggers the confirmation email.

**Story 1.6a: Bulk Import Validation & Feedback**

-   **As a** Super Admin, **I want** to upload a user CSV file and receive clear validation feedback, **so that** I know if my file is correctly formatted before processing.
-   **Acceptance Criteria:**
    1.  The Super Admin dashboard has an interface for uploading a user data file for a specific university.
    2.  A downloadable CSV/Excel template is provided to ensure correct data format.
    3.  The system validates the uploaded file for structural correctness.
    4.  The system provides clear, user-centric, row-specific error feedback for any invalid data (e.g., "_Row 15: Duplicate School ID - A user with this School ID already exists for this university. Each user must have a unique ID._").

**Story 1.6b: Asynchronous Import Processing**

-   **As a** Super Admin, **I want** a validated user CSV file to be processed as a background job, **so that** the import doesn't time out or degrade system performance.
-   **Acceptance Criteria:**
    1.  After a file is successfully validated, the Super Admin can initiate the import process.
    2.  The import runs as an asynchronous job using the RQ worker.
    3.  A successful import creates records in the `users` table and assigns appropriate roles via the `user_roles` table.
    4.  New users are created with a default password based on their university-issued ID.
    5.  The Super Admin receives a notification upon completion of the import.

**Story 1.7: Backup and Recovery Strategy**

-   **As a** Super Admin/DevOps Engineer, **I want** an automated backup and documented recovery procedure for the production database and user-uploaded files, **so that** we can recover from a disaster on the single VPS.
-   **Acceptance Criteria:**
    1.  An automated script performs nightly backups of the database.
    2.  An automated script performs nightly backups of the storage location for uploaded documents.
    3.  All backups are stored in a secure, off-server location.
    4.  A `RECOVERY.md` document in the project repository details the step-by-step procedure to restore the system from backups.

#### **Epic 2: Administrative Control Panel**

**Story 2.1: Evaluation Form Template Creation**

-   **As an** Admin, **I want** to create a new evaluation form template by providing a name, description, and core settings, **so that** I can begin building a new evaluation instrument.
-   **Acceptance Criteria:**
    1.  From the Admin dashboard, I can navigate to an "Evaluation Management" page that lists existing form templates.
    2.  This page has a "Create New Form Template" action.
    3.  Creating a new template requires a unique `name`.
    4.  I can optionally apply an "Intended for" label ('Students', 'Department Heads', or 'Both') to the template for organizational purposes.
    5.  I can select a predefined Likert scale (e.g., "Standard 1-5 Scale") to be used for all numerical questions on the form.
    6.  Upon saving, a new record is created in the `evaluation_form_templates` table with a default status of 'draft'.
    7.  **Developer Note:** For V1, the available Likert scales (4, 5, and 7-point) will be seeded directly into the `likert_scale_templates` table during initial deployment. This is not a feature for Admins to create their own scales.

**Story 2.2: Managing Form Criteria**

-   **As an** Admin, **I want** to add, edit, and reorder weighted criteria within a draft form template, **so that** I can structure the evaluation into logical sections.
-   **Acceptance Criteria:**
    1.  When editing a form template with a 'draft' status, I can add new criteria (e.g., "Teaching Methods," "Classroom Management").
    2.  Each criterion must have a `name` and a numerical `weight`.
    3.  The system must validate that the sum of all criteria weights for a single form template equals 100 before the form can be activated.
    4.  I can change the display order of criteria within the form.

**Story 2.3: Managing Form Questions**

-   **As an** Admin, **I want** to add Likert-scale and open-ended questions to the criteria within a draft form template, **so that** I can capture detailed feedback.
-   **Acceptance Criteria:**
    1.  Within a specific criterion, I can add multiple Likert-scale questions.
    2.  I can add open-ended questions to the form.
    3.  The system displays a warning if more than three open-ended questions are added but allows an override up to a maximum of eight.
    4.  I can set whether each question is required to be answered or optional.
    5.  At any point while editing a 'draft' template, I can select a "Preview" option that shows how the form will be rendered for evaluators.

**Story 2.4a: Form Template Activation & Duplication**

-   **As an** Admin, **I want** to activate a completed draft template and duplicate existing templates, **so that** I can finalize forms for assignment and iterate on new versions.
-   **Acceptance Criteria:**
    1.  I can "Activate" a 'draft' template only if all of the following conditions are met:
        -   It has a name, intended evaluator label, and a set Likert scale.
        -   It contains at least three criteria.
        -   Each criterion contains at least three Likert-scale questions.
        -   The sum of all criteria weights equals 100.
    2.  From the main list of templates, I can select a "Preview" option for any template (regardless of its status) to see how it is rendered.
    3.  An 'active' template cannot be edited. To create a new version, I must use a "Duplicate" function.
    4.  When an Admin duplicates an active template, the system creates a new template with '(Copy)' appended to its name, sets its status to 'draft', and immediately redirects the Admin to the edit page for this new copy.

**Story 2.4b: Form Template Archiving**

-   **As an** Admin, **I want** to archive templates that are no longer in use, **so that** I can keep my list of active templates clean and relevant.
-   **Acceptance Criteria:**
    1.  I can "Archive" an 'active' template. This changes its status to 'archived' and hides it from the main list.
    2.  A template with a status of 'assigned' cannot be archived. The option should be disabled or hidden.
    3.  An automated process will permanently delete any template that has remained in the 'archived' status for more than 30 days.

**Story 2.5: Assigning Forms to Evaluation Periods**

-   **As an** Admin, **I want** to assign an active form template to a specific academic term and assessment period, **so that** I can schedule and launch an evaluation.
-   **Acceptance Criteria:**
    1.  On the "Evaluation Management" page, I can create a new "Period Assignment."
    2.  I must select a `school_term` and an `assessment_period` ('midterm' or 'finals').
    3.  The form selection dropdown only shows templates with an 'active' status.
    4.  I must set a specific `start_date_time` and `end_date_time` for the evaluation window.
    5.  I can configure the "Minimum Submission Time" in seconds for this evaluation period, which defaults to 45.
    6.  If the selected form template includes open-ended questions, I can configure the 'Minimum' and 'Maximum' word count for responses, which will have sensible system defaults (e.g., 5 and 300).
    7.  The system prevents the creation of a duplicate assignment for the same university, term, period, and evaluator role.
    8.  Upon successful assignment, the status of the selected form template is updated from 'active' to 'assigned'.

#### **Epic 3: The Core Evaluation & Data Integrity Loop**

**Story 3.1: Evaluation Submission**

-   **As an** Evaluator (Student or Department Head), **I want** to select a faculty member and submit a complete evaluation during an active evaluation period, **so that** I can provide my feedback on their performance.
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

**Story 3.2: Pre-Submission Nudge for Low-Effort Ratings**

-   **As an** Evaluator, **I want** to be gently prompted if all my numerical ratings are the same, **so that** I am encouraged to provide more thoughtful and specific feedback.
-   **Acceptance Criteria:**
    1.  On the evaluation form, before the "Submit" button is clicked, the system performs a client-side check on all provided Likert-scale scores.
    2.  If the variance of all scores is zero (i.e., they are all the same number), a temporary, dismissible 'toast' notification appears.
    3.  The message text is concise, such as: "To provide the most helpful feedback, consider adding specific examples in the comments below."
    4.  The message does not prevent me from submitting the evaluation.

**Story 3.3: Automated "Low-Confidence" Flagging**

-   **As an** Admin, **I want** the system to automatically flag submissions that appear to be low-effort, **so that** I can review them for data quality.
-   **Acceptance Criteria:**
    1.  Immediately after a user submits an evaluation, a server-side check is performed.
    2.  A submission is flagged with a reason of "Low-Confidence" if it meets **both** of the following criteria: (A) the variance of all Likert-scale scores is zero, **AND** (B) the submission contains no meaningful qualitative feedback (i.e., all _optional_ open-ended questions were left blank).
    3.  If a submission is flagged, a new record is created in the `flagged_evals` table for administrative review.

**Story 3.4: Asynchronous "Recycled Content" Flagging**

-   **As an** Admin, **I want** the system to automatically detect and flag evaluations where an evaluator reuses their own text, **so that** I can ensure the originality of feedback.
-   **Acceptance Criteria:**
    1.  Upon a successful evaluation submission, a job is added to the asynchronous work queue.
    2.  The background job compares the submitted open-ended text against **that same evaluator's** previous submissions across all evaluation periods.
    3.  If the text has over 95% similarity to one of their previous submissions, a "Recycled Content" flag is created for the evaluation.
    4.  The notification sent to the student for recycled content must clearly explain that reused text was detected and state the importance of providing original feedback for each unique evaluation.

**Story 3.5a: Flagged Evaluation Dashboard (View Only)**

-   **As an** Admin, **I want** a dashboard to view a list of all flagged evaluations and see the detailed reasons for each flag, **so that** I can assess the queue and understand the issues.
-   **Acceptance Criteria:**
    1.  The Admin dashboard includes a page that lists all evaluations with a 'pending' flag.
    2.  The list displays the faculty member, the reason(s) for the flag (e.g., "Low-Confidence"), and the submission date.
    3.  Selecting a flagged evaluation shows a detailed view with a side-by-side comparison of the submission's numerical ratings and its open-ended text.

**Story 3.5b: Flagged Evaluation Processing**

-   **As an** Admin, while viewing a flagged evaluation, **I want** to be able to Approve, Reject, or Request Resubmission, **so that** I can process the queue and maintain data integrity.
-   **Acceptance Criteria:**
    1.  From the detailed view, I have three actions: **Approve**, **Reject**, or **Request Resubmission**.
    2.  Choosing **"Approve"** resolves the flag and ensures the submission data is included in all aggregate calculations.
    3.  Choosing **"Reject"** permanently deletes the evaluation submission and all its associated answers. The data will be excluded from all aggregate calculations, and an anonymous notification with the reason is sent to the student.
    4.  Choosing **"Request Resubmission"** marks the original submission as invalid (to be excluded from calculations) and triggers an anonymous notification for the student to submit a new evaluation.

**Story 3.6: Viewing Resolved Flags**

-   **As an** Admin, **I want** to be able to view a history of evaluations that I have already resolved, **so that** I can maintain an audit trail and reference past decisions.
-   **Acceptance Criteria:**
    1.  The flagged evaluations dashboard has a separate tab or filter to view 'Resolved' items.
    2.  The resolved list shows the submission details, the original flag reason, the action taken (Approved, Rejected, etc.), who resolved it, and the date of resolution.
    3.  This view is read-only.

#### **Epic 4: Data Processing & Insights Visualization**

**Story 4.1: Asynchronous Quantitative Analysis Job**

-   **As a** System, **I want** to process the numerical Likert-scale answers from a submitted evaluation in a background job, **so that** the raw scores are calculated and stored for aggregation without blocking the user.
-   **Acceptance Criteria:**
    1.  When a new, valid evaluation submission is ready for processing, a job is added to the asynchronous work queue (Redis+RQ).
    2.  **Question-Level Analysis:** The job must calculate the **median** score for each individual Likert-scale question in the submission.
    3.  **Criterion-Level Analysis:** The job must then calculate the **mean** of the question medians for each criterion, resulting in an average score for each section of the evaluation form.
    4.  **Overall Raw Score Calculation:** The job must apply the weights assigned to each criterion (from the `evaluation_criteria` table) to the criterion-level mean scores, calculating a final weighted mean. This result is the `quant_score_raw`.
    5.  The processed results, including per-question medians and per-criterion scores, are stored in the `numerical_aggregates` table, ready for the final normalization step in a subsequent story.
    6.  The job is marked as complete, and any errors during processing are logged.

**Story 4.2: Asynchronous Qualitative Analysis Job**

-   **As a** System, **I want** to process the open-ended feedback from a submitted evaluation in a background job, **so that** qualitative insights like sentiment and key themes are extracted and stored for aggregation.
-   **Acceptance Criteria:**
    1.  When a new, valid evaluation submission is processed, a job is added to the asynchronous work queue (Redis+RQ) to handle its open-ended answers.
    2.  The job retrieves the text from the `evaluation_open_ended_answers` table for the given submission.
    3.  **Sentiment Analysis:** The job must use the **XLM-ROBERTa** model to analyze the text. The results must be saved to the `open_ended_sentiments` table and must include:
        -   The final `predicted_sentiment_label` (e.g., 'positive', 'neutral', or 'negative').
        -   The `predicted_sentiment_label_score` (the probability of the predicted label).
        -   The full sentiment distribution: `positive_score`, `neutral_score`, and `negative_score`.
        -   The `accuracy` and `confidence` scores for the model's prediction.
    4.  **Keyword Extraction:** The job must use the **KeyBERT** model to extract relevant keywords and phrases. The results are saved to the `open_ended_keywords` table and must adhere to the following:
        -   Only keywords with a `relevance_score` above a configurable threshold are saved to prevent irrelevant results.
        -   The `relevance_score` itself must be stored with each keyword.
    5.  The processed qualitative results are now ready for the final aggregation and normalization step (Story 4.3).
    6.  The job is marked as complete, and any processing errors are logged.

**Story 4.3: Final Aggregation and Normalization Job**

-   **As a** System, **I want** to run a final aggregation and normalization job, **so that** the individual quantitative and qualitative analysis results are combined into standardized, comparable scores for reporting and visualization.
-   **Acceptance Criteria:**
    1.  The job is triggered after the prerequisite quantitative (4.1) and qualitative (4.2) analysis jobs for a submission or batch of submissions are successfully completed.
    2.  **Cohort Calculation:** The job must first calculate the cohort baseline statistics (**mean μ** and **standard deviation σ**) for the relevant comparison group (e.g., department-level) for both the `quant_score_raw` and `qual_score_raw` values.
    3.  **Z-Score Calculation:** Using the cohort baselines, the job must calculate the normalized **`z_quant`** and **`z_qual`** scores for each faculty evaluation, representing how many standard deviations they are from the cohort mean.
    4.  **Final Weighted Score:** The job must calculate the **`final_score_60_40`** by applying the 60/40 weighting to the z-scores as defined in the non-functional requirements.
    5.  **Data Persistence:** The job must update the `numerical_aggregates` and `sentiment_aggregates` tables with all calculated values, including z-scores, the final weighted score, and cohort details (e.g., `cohort_n`, μ, σ).
    6.  **Period Finalization:** The job must correctly handle period finalization. When an Admin triggers the "Finalize and Lock Period" function, this job runs a final time for that period and sets the `is_final_snapshot` flag to `true` for all relevant records, preventing them from being overwritten.
    7.  The job is marked as complete, and any errors are logged.

**Story 4.4: Dashboard Data Visualization**

-   **As a** User (Faculty, Department Head, or Admin), **I want** to view the processed and aggregated evaluation results on my role-specific dashboard, **so that** I can gain clear, visual insights into performance.
-   **Acceptance Criteria:**
    1.  The API must implement a **hybrid data retrieval strategy**:
        -   For finalized/locked evaluation periods (`is_final_snapshot` = true), data must be fetched directly from the aggregate tables for historical performance.
        -   For the current, provisional evaluation period, data must be calculated on-the-fly from the raw submission tables and the results must be cached (leveraging Redis) to provide near real-time dashboard updates.
    2.  The main dashboard must display a **word cloud** of keywords. By default, it shows a "combined" view. A user action (e.g., a toggle) must allow switching to a "detailed" view presenting three separate word clouds for **positive, neutral, and negative** keywords.
    3.  The dashboard must display **bar charts** for sentiment and numerical breakdowns. The default is a "side-by-side" layout. A user action must switch to a "detailed" vertical layout that includes specific KPIs:
        -   **Qualitative KPIs:** Display the count and percentage for each sentiment category, along with the top three keywords associated with each.
        -   **Quantitative KPIs:** Display the overall quantitative score, the highest and lowest rated criteria with their scores, and a comparison metric showing the change from the previous evaluation period.
    4.  The **Department Head and Admin dashboards** must implement the "mode-switching" functionality, allowing them to view aggregated data for a whole department or drill down to a specific faculty member's results.
    5.  All visualizations must clearly indicate when data is **"Provisional"** versus **"Final"**.

**Story 4.5: Evaluation Report Generation and Export**

-   **As a** User (Faculty, Department Head, or Admin), **I want** to access a dedicated reports page to generate and download comprehensive evaluation results, **so that** I can easily archive, share, and analyze data offline in a structured manner.
-   **Acceptance Criteria:**
    1.  A "Download Reports" link shall be present in the main side navigation panel, leading to a dedicated report generation page.
    2.  On the reports page, the user is presented with the same filter and view/mode controls available on their main dashboard.
    3.  After setting the desired filters, the user can select an export format: **PDF** or **CSV/Excel**.
    4.  For **PDF format**, the backend must use the **WeasyPrint** library to generate a professionally formatted document containing the key data visualizations and summary tables based on the selected filters.
    5.  For **CSV/Excel format**, the backend must use the **pandas** library to generate a well-structured file containing the detailed aggregated numerical and sentiment scores.
    6.  The generated file is returned to the user, initiating a download in their browser.

#### **Epic 5: AI-Powered Actionable Intelligence**

**Dev Note:** The implementation must include specific monitoring for the AI pipeline, tracking metrics like average suggestion generation time, model error rate, and Redis queue length to identify performance bottlenecks early.

**Story 5.1: AI Assistant Page and Controls**

-   **As a** Faculty or Department Head, **I want** to access a dedicated "AI Assistant" page with filters and pre-defined actions, **so that** I can easily set the context for generating performance suggestions.
-   **Acceptance Criteria:**
    1.  A new navigation link for the "AI Assistant" must be added to the main side panel, accessible **only** to users with 'Faculty' or 'Department Head' roles.
    2.  The page must include filter controls allowing the user to select the `school_term` and `assessment_period` for the data they wish to analyze.
    3.  For users with the 'Department Head' role, the page must also include the **mode-switching** component, allowing them to toggle between their own personal results, department-wide results, or the results of a specific faculty member in their department.
    4.  Instead of a single "generate" button, the page must feature a set of **pre-defined, button-based actions** (e.g., "Generate Strengths & Weaknesses Report," "Suggest Improvements for Lowest-Rated Criterion").
    5.  A small, permanent disclaimer must be visible on the page, with text like: _"This AI provides suggestions based on data patterns. Please use them as a starting point for reflection, not as a final judgment."_
    6.  The main content area is initially empty or displays a placeholder instructing the user to select their filters and choose a generation action.
    7.  Once a report is displayed, a "Start Over" or "Clear Results" button must become visible. Clicking this button will clear the results from the view and re-enable all action buttons.

**Story 5.2: AI Suggestion Generation**

-   **As a** Faculty or Department Head, **I want** to click a pre-defined action button and have the system generate relevant suggestions, **so that** I can receive AI-powered insights based on my selected data.
-   **Acceptance Criteria:**
    1.  When an action button is clicked, the frontend sends a request to a dedicated backend endpoint, including the selected filters (term, period, user/department mode).
    2.  The backend retrieves all necessary processed data for the given context, including records from `numerical_aggregates`, `sentiment_aggregates`, and the top 5 positive/negative `open_ended_keywords`.
    3.  A structured, context-rich prompt is constructed for the **Flan-T5 model**. This prompt must adhere to the **Persona-Context-Task-Format** framework and must instruct the model to adopt a constructive "academic coach" persona.
    4.  While the backend is processing the request, all action buttons on the 'AI Assistant' page **must be disabled** and display a loading indicator.
    5.  If the model fails to generate a response or times out, the API must return a specific error (e.g., 503 Service Unavailable), and the frontend must display a user-friendly message.
    6.  The generated suggestions are returned to the frontend and displayed clearly in the main content area of the "AI Assistant" page.

**Story 5.3: Saving and Viewing Suggestion History**

-   **As a** Faculty or Department Head, **I want** to save generated suggestions and view a history of my past requests, **so that** I can track insights and progress over time.
-   **Acceptance Criteria:**
    1.  Once suggestions are displayed, a "Save to History" button becomes available.
    2.  Clicking "Save" sends the generated text and its context to the backend, creating a new record in the `ai_suggestions` table.
    3.  After a suggestion is successfully saved, the "Save to History" button **must change to a 'Saved' state** (e.g., icon and text change) and become disabled for the current report.
    4.  The "AI Assistant" page must contain a "History" tab or section that displays a list of previously saved suggestions, showing the date, context, and a preview.
    5.  Selecting a historical item displays the full saved report.

**Story 5.4: Exporting AI Suggestions**

-   **As a** Faculty or Department Head, **I want** to download my generated AI suggestions as a professional-looking document, **so that** I can easily share, print, or archive these insights for my records.
-   **Acceptance Criteria:**
    1.  When AI suggestions are displayed, a "Download as PDF" button is visible.
    2.  Clicking the button sends the content of the currently displayed suggestion to a backend endpoint.
    3.  The backend uses the **WeasyPrint** library to render the text into a formatted PDF document.
    4.  The PDF includes a clear header, the date, the context (filters used), and the full text of the suggestions.
    5.  The generated PDF is returned to the user, initiating a file download in their browser.

---

### **Next Steps**

This document provides the complete requirements for the "Proficiency" application.

-   **For the Architect (`*agent architect`):** Please use this PRD as the primary input to create the `fullstack-architecture.md` document. Pay close attention to the technical assumptions in Section 4 and the detailed data flow implied by the stories in Epics 4 and 5.

-   **For the Product Owner (`*agent po`):** Please use the `po-master-checklist` to perform a final validation of this document for completeness and consistency before the Architect begins their work.
