### **Section 1: Goals and Background Context**

#### **Goals**

* **Develop "Proficiency," a multi-tenant SaaS web platform** to modernize the faculty evaluation process for educational institutions, starting with the University of Cebu - Lapu-Lapu and Mandaue.
* **Implement an AI-powered analysis engine** that automatically processes qualitative feedback from students and department heads to provide sentiment analysis, keyword extraction, and generate actionable, data-driven suggestions for improvement.
* **Ensure high data quality and evaluation integrity** through automated, server-side checks that flag low-effort submissions and detect recycled content.
* **Provide highly dynamic and customizable evaluation forms** that allow administrators to tailor evaluation criteria, questions, and scoring to diverse institutional needs.
* **Deliver intuitive, role-based dashboards and visualizations** to make evaluation results easy to interpret for faculty, department heads, and administrators, supporting continuous faculty development and institutional decision-making.

#### **Background Context**

Existing faculty evaluation systems, particularly within the Philippines and at the target institution, suffer from significant limitations. These systems often rely on static forms that cannot adapt to changing criteria and over-emphasize quantitative Likert scores while failing to extract meaningful insights from valuable open-ended feedback. The analysis of this textual feedback is often a manual, time-consuming, and error-prone process, resulting in low-quality, unactionable results that do little to support genuine faculty growth.

"Proficiency" is designed to address these critical gaps. It is a modern SaaS platform that leverages an AI pipeline to automate the deep analysis of textual feedback, providing insights into sentiment and key themes. By combining this with robust integrity checks, customizable forms, and role-based data visualization, Proficiency aims to transform faculty evaluation from a burdensome administrative task into a powerful tool for continuous professional development and educational excellence.

#### **Change Log**

| Date           | Version | Description                                                                                                                                                        | Author        |
| :------------- | :------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------ |
| **2025-10-09** | **8.6** | **Added foundational technical stories (1.10, 1.11) for API middleware and frontend mocking to Epic 1, including dependency mapping.**                               | **John, PM**  |
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

***
