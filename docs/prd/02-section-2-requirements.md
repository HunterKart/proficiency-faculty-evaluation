### **Section 2: Requirements**

#### **Functional Requirements**

* **FR1: User and University Management**
  * The system shall support five user roles: **Students, Faculty, Department Heads, Admins, and Super Admins**.
  * For V1, user creation will be limited to two methods: 1) **Admin/Super Admin bulk import** via CSV/Excel and 2) **Self-registration using a valid, university-provided invitation token**. The "evidence-based" manual sign-up is deferred to a post-V1 release.
  * **Super Admins** shall manage the university registration and approval lifecycle.
* **FR2: Dynamic Evaluation Form & Period Management**
  * Admins shall have the ability to **create, modify, and manage dynamic evaluation form templates** with the statuses: `draft`, `active`, `assigned`, and `archived`.
  * Admins shall **assign form templates to specific evaluation periods**, defined by school year, semester (1st, 2nd, Summer), and assessment period (Midterm, Finals).
  * An `'assigned'` form template is locked and cannot be edited. An `'active'` form template remains editable.
* **FR3: Evaluation Submission & Integrity**
  * The system must implement a **"Pre-Submission Nudge,"** a non-blocking UI message to encourage users with low-variance Likert scores to provide written examples.
  * A submission must be automatically flagged with **"Low-Confidence"** if it contains both low-variance Likert scores AND short or empty open-ended answers.
  * The system shall run an asynchronous job to detect and flag **"Recycled Content"** that has over 95% similarity to previous submissions.
* **FR4: Flagged Evaluation Workflow**
  * The system must automatically flag evaluations for data inconsistencies, such as a **sentiment-coherence mismatch**.
  * Admins shall have a dedicated interface to review all flagged evaluations.
  * Admins must be able to resolve a flagged evaluation by choosing one of three actions: **Approve**, **Archive**, or **Request Resubmission**.
  * **FR4.1:** The notification sent to a Student for a resubmission request or archived evaluation **must be anonymous** and clearly state the reason to guide them.
  * **FR4.2:** The Admin's review dashboard for flagged evaluations must provide a **side-by-side comparison** of the submission's numerical ratings and its open-ended text.
* **FR5: Data Analysis Pipeline**
  * All evaluation submissions shall be processed asynchronously via a **job queue (Redis+RQ)**.
  * The pipeline must separate analysis into a **Quantitative Layer** and a **Qualitative Layer**.
  * A final layer shall perform **Normalization and Aggregation** to combine scores and prepare data for visualization.
  * **FR5.1:** Evaluation submissions with a status of 'archived' or 'pending review' **must be excluded** from all aggregate calculations.
* **FR6: AI-Powered Analysis and Insights**
  * The system must perform automated **sentiment analysis** (Primary Model: XLM-ROBERTa) and **keyword extraction** (KeyBERT).
  * A dedicated **"AI Assistant" page** shall be available to Faculty and Department Heads to generate reports and suggestions from processed data using the external Gemini API.
* **FR7: Dashboards and Visualizations**
  * The system shall present data using specific visualizations: **Word Clouds, Bar Charts, and Performance Trend Line Charts**. Admins will also have access to an **Evaluation Submission Behavior Line Chart**.
  * Department Heads and Admins must be able to switch between different data views or **"modes"** (e.g., department-wide, specific faculty results).
* **FR8: Provisional and Finalized Reporting Workflow**
  * All reports for an active review period shall be marked as **"Provisional."**. When an Admin approves a flagged evaluation, an asynchronous job must **recalculate the provisional aggregates** for the affected parties. Admins shall have a function to **"Finalize and Lock Period,"** which runs a final aggregation and sets the `is_final_snapshot` flag to `true`. To ensure high performance and scalability for all users, data on provisional dashboards is updated via a near real-time process. As such, the displayed aggregates **may be up to 5 minutes out of date** and may not instantly reflect the most recent submissions.
* **FR9: Historical Data Import**
  * Admins shall have the ability to bulk import historical university data via CSV/Excel to prime the system.
  * The import process must support: **Academic Structure** (departments, programs, subjects), **User & Enrollment Records**, and **Past Evaluation Submissions** (including Likert and open-ended answers).
  * All imported historical evaluation records must be processed by the system's data analysis pipeline (as defined in FR5 and FR6).
* **FR10: Registration Code Management**: Admins shall be able to set, view, and update the maximum usage limit for their university's self-registration code.
* **FR11: Role-Based Registration Codes**: The system must support the generation of distinct self-registration codes for different user roles. The registration process must validate that the user's selected role matches the intended role of the code provided.
* **FR12: Resubmission Grace Period**: A "resubmission grace period" of 48 hours shall be granted to a student for a flagged evaluation, allowing them to resubmit their work even if the parent evaluation period is no longer active.
* **FR13: Duplicate Evaluation Period Assignment**: Admins shall have the ability to duplicate an existing evaluation period assignment to pre-fill the creation form with the same form template configuration, requiring only new scheduling details to be entered.
* **FR14: Proactive Period Setup Notification**: The system shall generate a notification for Admins when an evaluation period concludes, prompting them to schedule the next logical period and providing a one-click action to begin the duplication process.
* **FR15: In-Use Resource Protection**: The system must prevent the archival or deletion of any resource (e.g., Form Template) that is currently assigned to an active or scheduled Evaluation Period. An attempt to do so must result in a clear error message explaining the dependency.
* **FR16: Secure Account Verification**: To enhance security, account verification links sent to new users must automatically expire 24 hours after they are issued.
* **FR17: Administrative Re-aggregation**: The system must provide a secure, admin-only API endpoint to trigger a full recalculation of all final, normalized scores for a given historical evaluation period. This enables reprocessing of data if scoring logic or configuration (like score weighting) is updated. A UI for this feature is not required for V1.
* **FR18: Report Generation Limits**: To ensure system stability, the generation of reports is subject to a size limit. If a user's filter criteria would result in a report exceeding a configurable number of records, the request must be rejected, and the user must be prompted to narrow their search or apply more specific filters.
* **FR19: Centralized Notification System**
  * The system shall implement a centralized notification service to manage all user-facing alerts, backed by the `Notification` data model.
  * Notifications must be stored in the database, linked to the recipient user.
  * The system must support two primary delivery methods: **In-App** (viewable within the user's dashboard) and **Email**.
  * The in-app notification interface must allow users to distinguish between `unread` and `read` notifications.
  * Specific events that must trigger notifications include, but are not limited to: user account verification, completion of background jobs (e.g., imports), flagged evaluation resolution, and proactive administrative prompts.

#### **Non-Functional Requirements**

* **NFR1: Architecture:** The system shall be a multi-tenant SaaS web platform with a modular, scalable, and asynchronous architecture.
* **NFR2: Configurable Scoring Logic**
  * The final evaluation score for a faculty member is a weighted combination of the aggregated quantitative (e.g., Likert scale) and qualitative (e.g., sentiment analysis) scores.
  * The weighting must not be hard-coded. Instead, it must be stored as a configurable value within the `university_settings` table, allowing each university (tenant) to adjust the balance (e.g., 60/40, 70/30) as needed. The system will be seeded with a default of 60% quantitative and 40% qualitative.
* **NFR3: Performance:** Access to AI-generated suggestions shall be restricted to Faculty and Department Heads to manage performance.
* **NFR4: Security:** The system must implement robust user registration and authentication protocols.
* **NFR5: Extensibility and Research:** The V1 production system will exclusively use the fine-tuned XLM-ROBERTa model. For academic comparison, a separate, non-production script or environment will be created to benchmark baseline models (VADER, Naïve Bayes, mBERT).
* **NFR6: System Calibration:** The automated flagging algorithms must be calibrated to minimize false positives and ensure the volume of flagged evaluations is manageable for Admins.
* **NFR7: Data Privacy Compliance:** All processing of imported historical and live user data must be compliant with the Data Privacy Act of 2012 (RA 10173). The architecture must account for the secure handling and storage of Personally Identifiable Information (PII).
* **NFR8: Timezone Standardization:** The entire platform shall operate on a single, standardized timezone: **Philippine Standard Time (PST / Asia/Manila)**. All times displayed in the UI must be explicitly labeled as PST to prevent ambiguity.
* **NFR9: Concurrency Control:** To ensure data integrity in a multi-admin environment, the system must implement **Optimistic Locking** for all shared, editable resources (e.g., Form Templates). Concurrent actions (e.g., two admins resolving the same item) must be handled gracefully on the backend on a "first-come, first-served" basis.
* **NFR10: Transactional Integrity:** All critical, multi-step business processes that modify the database, such as university onboarding or evaluation period cancellation, must be executed as atomic transactions to prevent the system from entering an inconsistent state upon partial failure.
* **NFR11: Configurable Data Integrity Engine**
  * The system's data integrity checks (e.g., recycled content detection, low-effort submission flagging) must be designed in a modular fashion to allow for future expansion.
  * Crucially, the thresholds for these checks (e.g., similarity percentage for recycled content) must be configurable on a per-university basis via the `university_settings` table. This ensures that administrators can fine-tune the engine's sensitivity to match their institution's specific academic standards.
* **NFR12: Configurable Rate Limiting:** To ensure system stability and control operational costs, the system **must implement rate-limiting** for resource-intensive features, specifically the **AI Assistant (Story 6.2)** and **Report Generation (Story 5.6)**. The thresholds for these limits **must be stored as configurable values** in the `UniversitySetting` table and **must not be hardcoded**. Default values will be seeded for V1, and a UI for Admins to manage these settings is deferred to a post-V1 release.
* **NFR13: Administrative Auditing**: All critical, state-changing actions performed by an administrator related to the evaluation lifecycle (including creating, updating, activating, or archiving form templates, and scheduling or cancelling evaluation periods) must generate a detailed entry in the system's audit log. The log must record the administrator who performed the action, the action taken, the target entity, and a timestamp.
* **NFR14: Automated Accessibility Compliance Testing**: To ensure adherence to WCAG standards, the CI/CD pipeline must include an automated accessibility test using `cypress-axe` on every pull request. This test must be configured to prevent merging code that introduces accessibility violations.

***
