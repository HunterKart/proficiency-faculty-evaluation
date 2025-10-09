## **API Specification**

This section provides the complete and definitive OpenAPI 3.0 specification for the Proficiency platform. It is the single source of truth for all API development, detailing every endpoint, data contract, and architectural principle that governs the communication between the frontend and backend.

### **Architectural Principles**

The following principles have been applied consistently across the entire API:

* **Versioning**: All endpoints are versioned under `/api/v1/` for stability and future compatibility.
* **Authentication**: Secure, stateless authentication is handled via JWT access and refresh tokens.
* **Authorization**: Strict role-based access control is enforced on all protected endpoints.
* **Concurrency**: Optimistic locking, enforced via a `version` field in relevant database models and validated in the API service layer, is used on all critical, shared resources to prevent data corruption from concurrent administrative actions. The API must return a `409 Conflict` status code when a stale version is detected.
* **Asynchronous Operations**: Long-running tasks (imports, reports, AI generation) are handled asynchronously via a job queue to ensure a responsive user experience.
* **Real-time Updates**: A WebSocket channel provides real-time progress and notification updates to the client, minimizing inefficient polling.
* **Idempotency**: Where possible, endpoints that trigger state changes (especially those initiating background jobs) should be designed to be idempotent to prevent duplicate actions on client retries.

### **OpenAPI 3.0 Specification (Complete)**

```yaml
openapi: 3.0.3
info:
    title: "Proficiency API"
    version: "1.0.0"
    description: "The official API for the Proficiency multi-tenant SaaS platform."
tags:
    - name: "Core"
    - name: "Public"
    - name: "Super Admin"
    - name: "Admin"
    - name: "Evaluations"
    - name: "Dashboards"
    - name: "Reports"
    - name: "AI Assistant"
    - name: "Shared Services"
servers:
    - url: "/api/v1"
      description: "API Server v1"
components:
    schemas:
        Error:
            type: object
            properties:
                error:
                    type: object
                    properties:
                        code:
                            type: string
                            description: "A unique, machine-readable error code."
                            example: "VALIDATION_ERROR"
                        message:
                            type: string
                            description: "A general, human-readable description of the error."
                            example: "The provided data was invalid."
                        details:
                            type: object
                            description: "(Optional) Field-specific validation errors."
                        requestId:
                            type: string
                            description: "A unique ID to correlate this request with server-side logs."
                            example: "abc123xyz789"
    securitySchemes:
        bearerAuth:
            type: http
            scheme: bearer
            bearerFormat: JWT
security:
    - bearerAuth: []

paths:
    # -----------------------------------------------------------------
    # Group 1: Core & Foundational APIs
    # -----------------------------------------------------------------
    /health:
        get:
            summary: "API Health Check"
            description: "A public endpoint to verify that the API service is running and healthy."
            tags: ["Core"]
            security: []
            responses:
                "200":
                    description: "Service is healthy"
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    status:
                                        type: string
                                        example: "ok"
    /university-requests:
        post:
            summary: "Submit a new university registration request"
            description: "A public endpoint for prospective universities to submit their registration application and supporting documents."
            tags: ["Public"]
            security: []
            requestBody:
                required: true
                content:
                    multipart/form-data:
                        schema:
                            type: object
                            properties:
                                details:
                                    type: object
                                    properties:
                                        universityName:
                                            type: string
                                        contactPersonName:
                                            type: string
                                        contactPersonEmail:
                                            type: string
                                            format: email
                                documents:
                                    type: array
                                    items:
                                        type: string
                                        format: binary
                                    description: "Allowed types: PDF, JPG, PNG. Max size: 5MB per file."
            responses:
                "202":
                    description: "Request accepted and is pending review."
                "400":
                    description: "Bad Request - Validation error or file constraint violation."
                    content:
                        application/json:
                            schema:
                                $ref: "#/components/schemas/Error"
    /register:
        post:
            summary: "Register a new user with a valid registration code"
            description: "Allows a new user to self-register for a specific university and role using a pre-issued code."
            tags: ["Public"]
            security: []
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            required:
                                - firstName
                                - lastName
                                - email
                                - password
                                - schoolId
                                - roleName
                                - registrationCode
                            properties:
                                firstName:
                                    type: string
                                lastName:
                                    type: string
                                email:
                                    type: string
                                    format: email
                                password:
                                    type: string
                                    format: password
                                    description: "Minimum 12 characters, with at least one uppercase, one lowercase, one number, and one special character."
                                    pattern: "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{12,}$"
                                schoolId:
                                    type: string
                                roleName:
                                    type: string
                                    enum:
                                        [
                                            "Student",
                                            "Faculty",
                                            "Department Head",
                                            "Admin",
                                        ]
                                registrationCode:
                                    type: string
            responses:
                "201":
                    description: "User created successfully. Returns user object and JWTs."
                "400":
                    description: "Validation error (e.g., password policy not met)."
                    content:
                        application/json:
                            schema:
                                $ref: "#/components/schemas/Error"
                "409":
                    description: "Conflict (e.g., email or schoolId already exists)."
                    content:
                        application/json:
                            schema:
                                $ref: "#/components/schemas/Error"
                "410":
                    description: "Gone (e.g., registration code is invalid, expired, or has reached its max uses)."
                    content:
                        application/json:
                            schema:
                                $ref: "#/components/schemas/Error"

    # -----------------------------------------------------------------
    # Group 2: Super Admin & University Management
    # -----------------------------------------------------------------
    /super-admin/login/password:
        post:
            summary: "Super Admin Login - Step 1: Password"
            description: "Authenticates a Super Admin's email and password. On success, returns a short-lived, single-use token required for the second MFA step (PIN)."
            tags: ["Super Admin"]
            security: []
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                email:
                                    type: string
                                    format: email
                                password:
                                    type: string
            responses:
                "200":
                    description: "Password validation successful. Proceed to PIN step."
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    mfaToken:
                                        type: string
                                        description: "A temporary token to be used in the PIN verification step."
                "401":
                    description: "Invalid credentials."
                    content:
                        application/json:
                            schema:
                                $ref: "#/components/schemas/Error"
    /super-admin/login/pin:
        post:
            summary: "Super Admin Login - Step 2: PIN (MFA)"
            description: "Verifies the temporary MFA token and the Super Admin's 6-digit PIN. On success, returns the final JWT access and refresh tokens."
            tags: ["Super Admin"]
            security: []
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                mfaToken:
                                    type: string
                                pin:
                                    type: string
                                    pattern: "^[0-9]{6}$"
            responses:
                "200":
                    description: "Authentication successful. Returns JWTs."
                "401":
                    description: "Invalid MFA token or PIN."
                    content:
                        application/json:
                            schema:
                                $ref: "#/components/schemas/Error"
    /super-admin/university-requests:
        get:
            summary: "List University Registration Requests"
            description: "Retrieves a list of university registration requests, used to populate the Kanban board. Can be filtered by status."
            tags: ["Super Admin"]
            parameters:
                - name: status
                  in: query
                  schema:
                      type: string
                      enum: [submitted, in_review, approved, rejected]
            responses:
                "200":
                    description: "A list of registration requests."
                "403":
                    description: "Forbidden. User is not a Super Admin."
    /super-admin/university-requests/{requestId}/validation-summary:
        get:
            summary: "Get Validation Summary for Uploaded Files"
            description: "Runs a non-destructive check on any files uploaded with a request and returns a simple validation summary."
            tags: ["Super Admin"]
            parameters:
                - name: requestId
                  in: path
                  required: true
                  schema:
                      type: integer
            responses:
                "200":
                    description: "Returns a validation summary for uploaded files."
                "404":
                    description: "Request not found."
    /super-admin/university-requests/{requestId}/status:
        put:
            summary: "Update a Request's Status (e.g., for Locking)"
            description: "Updates the status of a request, typically used to move it from 'submitted' to 'in_review'."
            tags: ["Super Admin"]
            parameters:
                - name: requestId
                  in: path
                  required: true
                  schema:
                      type: integer
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                status:
                                    type: string
                                    enum: [in_review]
                                version:
                                    type: integer
            responses:
                "200":
                    description: "Status updated successfully. Returns the full updated request object."
                "409":
                    description: "Conflict. The request has been modified by another user. Please refresh."
    /super-admin/university-requests/{requestId}/approve:
        post:
            summary: "Approve a University Registration Request"
            description: "Approves a request, triggering the creation of the university, the initial Admin account, and enqueuing a verification email."
            tags: ["Super Admin"]
            parameters:
                - name: requestId
                  in: path
                  required: true
                  schema:
                      type: integer
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                version:
                                    type: integer
                                confirm_data_ingestion:
                                    type: boolean
                                    description: "Must be true, confirming the Super Admin has seen the validation summary."
            responses:
                "200":
                    description: "University approval process initiated successfully."
                "409":
                    description: "Conflict. This request has been modified or already resolved."
    /super-admin/university-requests/{requestId}/reject:
        post:
            summary: "Reject a University Registration Request"
            description: "Rejects a request and enqueues a notification email to the applicant with the provided reason."
            tags: ["Super Admin"]
            parameters:
                - name: requestId
                  in: path
                  required: true
                  schema:
                      type: integer
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                reason:
                                    type: string
                                version:
                                    type: integer
            responses:
                "200":
                    description: "Request rejection process initiated successfully."
                "409":
                    description: "Conflict. This request has been modified or already resolved."
    /super-admin/universities:
        get:
            summary: "List All Universities"
            description: "Retrieves a list of all university tenants on the platform."
            tags: ["Super Admin"]
            parameters:
                - name: status
                  in: query
                  schema:
                      type: string
                      enum: [pending, active, inactive]
            responses:
                "200":
                    description: "A list of universities."
    /super-admin/universities/{universityId}/status:
        put:
            summary: "Update a University's Status"
            description: "Updates the lifecycle status of an existing university."
            tags: ["Super Admin"]
            parameters:
                - name: universityId
                  in: path
                  required: true
                  schema:
                      type: integer
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                status:
                                    type: string
                                    enum: [active, inactive]
            responses:
                "200":
                    description: "University status updated successfully."

    # -----------------------------------------------------------------
    # Group 3: Administrative Control Panel
    # -----------------------------------------------------------------
    /admin/form-templates:
        get:
            summary: "List Evaluation Form Templates"
            description: "Retrieves all form templates for the admin's university."
            tags: ["Admin"]
            responses:
                "200":
                    description: "A list of form templates."
        post:
            summary: "Create a New Form Template"
            description: "Creates a new evaluation form template in a 'draft' state."
            tags: ["Admin"]
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                name:
                                    type: string
                                intendedFor:
                                    type: string
                                    enum:
                                        ["Students", "Department Heads", "Both"]
                                likertScaleTemplateId:
                                    type: integer
            responses:
                "201":
                    description: "Template created successfully."
    /admin/form-templates/{templateId}:
        put:
            summary: "Update a Form Template's Metadata"
            description: "Updates the metadata of a 'draft' or 'active' form template."
            tags: ["Admin"]
            parameters:
                - name: templateId
                  in: path
                  required: true
                  schema:
                      type: integer
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                name:
                                    type: string
                                intendedFor:
                                    type: string
                                    enum:
                                        ["Students", "Department Heads", "Both"]
                                likertScaleTemplateId:
                                    type: integer
                                version:
                                    type: integer
            responses:
                "200":
                    description: "Template updated successfully."
                "409":
                    description: "Conflict. The template has been modified by another user."
    /admin/form-templates/{templateId}/structure:
        put:
            summary: "Batch Update a Form's Structure"
            description: "Updates the entire nested structure of a form template (criteria and questions) in a single transaction."
            tags: ["Admin"]
            parameters:
                - name: templateId
                  in: path
                  required: true
                  schema:
                      type: integer
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                version:
                                    type: integer
                                structure:
                                    type: array
                                    # The full schema for nested criteria and questions would be defined here.
            responses:
                "200":
                    description: "Form structure updated successfully."
                "400":
                    description: "Validation error (e.g., weights don't sum to 100)."
                "409":
                    description: "Conflict. The form has been modified by another user."
    /admin/form-templates/{templateId}/status:
        put:
            summary: "Update a Template's Status"
            description: "Changes the status of a form template (e.g., from 'draft' to 'active')."
            tags: ["Admin"]
            parameters:
                - name: templateId
                  in: path
                  required: true
                  schema:
                      type: integer
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                status:
                                    type: string
                                    enum: [active, archived]
                                version:
                                    type: integer
            responses:
                "200":
                    description: "Status updated successfully."
                "400":
                    description: "Bad Request. Template is invalid and cannot be activated."
                "409":
                    description: "Conflict. Cannot archive a template that is assigned to an active period."
    /admin/evaluation-periods:
        get:
            summary: "List Evaluation Periods"
            description: "Retrieves all scheduled, active, and past evaluation periods."
            tags: ["Admin"]
            responses:
                "200":
                    description: "A list of evaluation periods."
        post:
            summary: "Schedule a New Evaluation Period"
            description: "Creates and schedules a new evaluation period by assigning form templates."
            tags: ["Admin"]
            requestBody:
                # A complex body with term, dates, form template IDs, etc.
            responses:
                "201":
                    description: "Period scheduled successfully."
    /admin/evaluation-periods/{periodId}/duplicate:
        post:
            summary: "Duplicate an Evaluation Period"
            description: "Creates a new draft period assignment pre-filled with the configuration of an existing one."
            tags: ["Admin"]
            parameters:
                - name: periodId
                  in: path
                  required: true
                  schema:
                      type: integer
            responses:
                "201":
                    description: "Returns the data for a new, unsaved period assignment form."
    /admin/evaluation-periods/{periodId}/cancel:
        post:
            summary: "Initiate an Emergency Period Cancellation"
            description: "Enqueues a job to 'soft cancel' an active evaluation period."
            tags: ["Admin"]
            parameters:
                - name: periodId
                  in: path
                  required: true
                  schema:
                      type: integer
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                reason:
                                    type: string
                                internalNotes:
                                    type: string
            responses:
                "202":
                    description: "Cancellation job accepted."
        delete:
            summary: "Undo a Period Cancellation"
            description: "Attempts to dequeue the cancellation job if it's still within the 'undo' window."
            tags: ["Admin"]
            parameters:
                - name: periodId
                  in: path
                  required: true
                  schema:
                      type: integer
            responses:
                "204":
                    description: "Cancellation successfully aborted."
                "410":
                    description: "Gone. The 'undo' window has expired."
    /admin/evaluation-periods/{periodId}/restore:
        post:
            summary: "Restore a 'Soft Cancelled' Period"
            description: "Restores a period that was cancelled, but is still within the grace period."
            tags: ["Admin"] # This could be restricted to Super Admin if needed.
            parameters:
                - name: periodId
                  in: path
                  required: true
                  schema:
                      type: integer
            responses:
                "200":
                    description: "Period restored successfully."
                "410":
                    description: "Gone. The restoration grace period has expired."
    /admin/evaluation-periods/{periodId}/re-aggregate:
        post:
            summary: "[Admin] Re-run Final Aggregation for a Period"
            description: "Enqueues the Final Aggregation Job for all processed submissions within a given historical evaluation period. This is a powerful administrative tool for recalculating scores after a logic change or data correction."
            tags: ["Admin"]
            parameters:
                - name: periodId
                  in: path
                  required: true
                  schema:
                      type: integer
            responses:
                "202":
                    description: "Re-aggregation job has been successfully accepted and queued for all relevant submissions."
    /admin/registration-codes:
        get:
            summary: "List Registration Codes"
            description: "Retrieves all registration codes for the admin's university."
            tags: ["Admin"]
            responses:
                "200":
                    description: "A list of registration codes."
        post:
            summary: "Create a Registration Code"
            description: "Creates a new registration code for a specific role with a usage limit."
            tags: ["Admin"]
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                roleId:
                                    type: integer
                                maxUses:
                                    type: integer
                                    description: "A sensible maximum (e.g., 10,000) is enforced by the server."
                                expiresAt:
                                    type: string
                                    format: date-time
            responses:
                "201":
                    description: "Code created successfully."

    # -----------------------------------------------------------------
    # Group 4: Data Onboarding & Job Monitoring
    # -----------------------------------------------------------------
    /admin/academic-structure/departments:
        post:
            summary: "Create a Department"
            description: "Manually creates a new academic department."
            tags: ["Admin"]
            responses:
                "201":
                    description: "Department created successfully."
        # GET, PUT, DELETE endpoints for departments would follow a similar, standard RESTful pattern.
    /admin/academic-structure/programs:
        post:
            summary: "Create a Program"
            description: "Manually creates a new academic program within a department."
            tags: ["Admin"]
            responses:
                "201":
                    description: "Program created successfully."
        # GET, PUT, DELETE endpoints for programs would follow.
    /admin/academic-structure/subjects:
        post:
            summary: "Create a Subject"
            description: "Manually creates a new subject within a department."
            tags: ["Admin"]
            responses:
                "201":
                    description: "Subject created successfully."
        # GET, PUT, DELETE endpoints for subjects would follow.
    /admin/bulk-import/validate:
        post:
            summary: "Validate a Bulk Import File"
            description: "Uploads a CSV file for structural and content validation, including referential integrity checks against the database."
            tags: ["Admin"]
            requestBody:
                required: true
                content:
                    multipart/form-data:
                        schema:
                            type: object
                            properties:
                                importType:
                                    type: string
                                    enum:
                                        [
                                            "ACADEMIC_STRUCTURE",
                                            "USER_ENROLLMENT",
                                            "HISTORICAL_EVALUATION",
                                        ]
                                file:
                                    type: string
                                    format: binary
            responses:
                "200":
                    description: "File is valid and ready for processing. Returns a temporary ID for the validated file."
                "400":
                    description: "File has validation errors. The response body contains details."
    /admin/bulk-import/process:
        post:
            summary: "Process a Validated Bulk Import File"
            description: "Enqueues a background job to process a previously validated CSV file."
            tags: ["Admin"]
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                validatedFileId:
                                    type: string
            responses:
                "202":
                    description: "Import job has been accepted and is now queued for processing."
    /admin/job-monitor:
        get:
            summary: "List All Background Jobs"
            description: "Retrieves a paginated list of all background jobs for the admin's university."
            tags: ["Admin"]
            parameters:
                - name: status
                  in: query
                  schema:
                      type: string
                      enum:
                          [
                              queued,
                              processing,
                              cancellation_requested,
                              completed_success,
                              completed_partial_failure,
                              failed,
                              cancelled,
                          ]
            responses:
                "200":
                    description: "A list of background jobs."
    /admin/job-monitor/{jobId}:
        get:
            summary: "Get Job Details"
            description: "Retrieves the detailed status and metadata for a specific background job. For failed jobs, this includes a direct link to the error report."
            tags: ["Admin"]
            parameters:
                - name: jobId
                  in: path
                  required: true
                  schema:
                      type: string # Jobs are often identified by UUIDs
            responses:
                "200":
                    description: "Detailed information for the specified job."
                    content:
                        application/json:
                            schema:
                                # This would reference the full BackgroundTask model schema
                                properties:
                                    error_report_url:
                                        type: string
                                        format: uri
                                        description: "A direct download URL for the error report, present only if the job failed or partially failed."
    /admin/job-monitor/{jobId}/cancel:
        delete:
            summary: "Cancel a Queued Job"
            description: "Immediately cancels a job that is still in the 'queued' state."
            tags: ["Admin"]
            parameters:
                - name: jobId
                  in: path
                  required: true
                  schema:
                      type: string
            responses:
                "204":
                    description: "Job successfully cancelled."
                "409":
                    description: "Conflict. The job is not in the 'queued' state."
    /admin/job-monitor/{jobId}/request-cancellation:
        post:
            summary: "Request Cancellation of a Processing Job"
            description: "Sends a 'stop' signal to a job that is already in progress. The job will stop gracefully after its current batch."
            tags: ["Admin"]
            parameters:
                - name: jobId
                  in: path
                  required: true
                  schema:
                      type: string
            responses:
                "202":
                    description: "Cancellation has been requested. The job status is now 'cancellation_requested'."
                "409":
                    description: "Conflict. The job is not in a 'processing' state."
    /admin/job-monitor/{jobId}/force-fail:
        post:
            summary: "Force a Stuck Job to Fail"
            description: "Manually marks a job that appears to be stuck in 'processing' as 'failed' to unlock system resources."
            tags: ["Admin"]
            parameters:
                - name: jobId
                  in: path
                  required: true
                  schema:
                      type: string
            responses:
                "200":
                    description: "Job has been successfully marked as failed."
                "409":
                    description: "Conflict. The job is not in a 'processing' state."
    /ws/job-progress/{jobId}:
        # Note: OpenAPI 3.0 does not officially support WebSockets. This is a conceptual representation.
        get:
            summary: "Subscribe to Real-Time Job Progress"
            description: "Establishes a WebSocket connection to receive live progress updates for a specific job."
            tags: ["Admin"]
            parameters:
                - name: jobId
                  in: path
                  required: true
                  schema:
                      type: string
            responses:
                "101":
                    description: "Switching protocols to WebSocket."

    # -----------------------------------------------------------------
    # Group 5: Core Evaluation Workflow
    # -----------------------------------------------------------------
    /evaluations/pending:
        get:
            summary: "Get Pending Evaluations"
            description: "Retrieves a list of pending evaluations for the authenticated user based on their role and enrollments."
            tags: ["Evaluations"]
            responses:
                "200":
                    description: "A list of faculty and subjects awaiting evaluation."
    /evaluations/forms/{subjectOfferingId}:
        get:
            summary: "Get Evaluation Form for a Specific Offering"
            description: "Retrieves the specific evaluation form (questions, criteria, etc.) for a given subject offering."
            tags: ["Evaluations"]
            parameters:
                - name: subjectOfferingId
                  in: path
                  required: true
                  schema:
                      type: integer
            responses:
                "200":
                    description: "The structured evaluation form."
                "403":
                    description: "Forbidden. The user is not eligible to evaluate this offering."
    /evaluations/submissions:
        post:
            summary: "Submit a Completed Evaluation"
            description: "Submits all answers for a single evaluation. This endpoint is idempotent."
            tags: ["Evaluations"]
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                evaluateeId:
                                    type: integer
                                subjectOfferingId:
                                    type: integer
                                timeOnFormSeconds:
                                    type: integer
                                likertAnswers:
                                    type: array
                                    items:
                                        type: object
                                        properties:
                                            questionId:
                                                type: integer
                                            answerValue:
                                                type: integer
                                openEndedAnswers:
                                    type: array
                                    items:
                                        type: object
                                        properties:
                                            questionId:
                                                type: integer
                                            answerText:
                                                type: string
            responses:
                "201":
                    description: "Evaluation submitted successfully."
                "400":
                    description: "Bad Request. Validation failed (e.g., invalid question IDs, required answers missing)."
                "409":
                    description: "Conflict. An evaluation for this offering has already been submitted."
    /admin/flagged-evaluations:
        get:
            summary: "List Flagged Evaluations"
            description: "Retrieves a paginated list of flagged evaluations, filterable by status ('pending' or 'resolved')."
            tags: ["Admin"]
            parameters:
                - name: status
                  in: query
                  required: true
                  schema:
                      type: string
                      enum: [pending, resolved]
            responses:
                "200":
                    description: "A list of flagged evaluations."
    /admin/flagged-evaluations/{flagId}:
        get:
            summary: "Get Flagged Evaluation Details"
            description: "Retrieves a comprehensive 'hydrated' object for a single flagged evaluation, including submission data and highlight metadata."
            tags: ["Admin"]
            parameters:
                - name: flagId
                  in: path
                  required: true
                  schema:
                      type: integer
            responses:
                "200":
                    description: "Detailed information for the flagged evaluation."
    /admin/flagged-evaluations/{flagId}/resolve:
        post:
            summary: "Resolve a Flagged Evaluation"
            description: "Performs one of three actions on a pending flagged evaluation: 'approve', 'archive', or 'request_resubmission'. This endpoint uses optimistic locking."
            tags: ["Admin"]
            parameters:
                - name: flagId
                  in: path
                  required: true
                  schema:
                      type: integer
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                version:
                                    type: integer
                                    description: "The version number of the flagged evaluation record, for optimistic locking."
                                action:
                                    type: string
                                    enum:
                                        [approve, archive, request_resubmission]
                                reason:
                                    type: string
                                    description: "Required only when the action is 'archive' or 'request_resubmission'."
            responses:
                "200":
                    description: "The flagged evaluation was resolved successfully."
                "400":
                    description: "Bad Request. 'reason' is missing for an action that requires it."
                "409":
                    description: "Conflict. The flagged evaluation has been modified by another admin. Please refresh."

    # -----------------------------------------------------------------
    # Group 6: Dashboards, Results, and Reporting
    # -----------------------------------------------------------------
    /dashboard:
        get:
            summary: "Get All Dashboard Data"
            description: "Retrieves all data needed for the initial render of a user's dashboard. The response is a complex object tailored to the user's role and filters."
            tags: ["Dashboards"]
            parameters:
                - name: school_term_id
                  in: query
                  required: true
                  schema:
                      type: integer
                - name: assessment_period_id
                  in: query
                  required: true
                  schema:
                      type: integer
                - name: view_mode
                  in: query
                  schema:
                      type: string
                      enum: [university, department, faculty]
                - name: target_id
                  in: query
                  schema:
                      type: integer
            responses:
                "200":
                    description: "A complex JSON object containing all necessary data for the dashboard visualizations, structured to align with ECharts."
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    metadata:
                                        type: object
                                        properties:
                                            is_provisional:
                                                type: boolean
                                            data_source_type:
                                                type: string
                                                enum: [live, historical]
                                    # Fully defined schemas for summary_kpis, sentiment_breakdown, keywords, etc. would be included here.
                "403":
                    description: "Forbidden. User is not permitted to view the requested data slice due to row-level security."
    /comments:
        get:
            summary: "Get Anonymized Comments for a Data Point"
            description: "Retrieves the raw, anonymized open-ended comments associated with a specific slice of data. This endpoint is handled by a dedicated service that **strictly enforces the anonymity threshold server-side.** If the number of underlying responses is below the configured minimum, this endpoint will return a 403 Forbidden status to protect evaluator privacy."
            tags: ["Dashboards"]
            parameters:
                - name: school_term_id
                in: query
                required: true
                schema:
                    type: integer
                # ... other required filters to define the data slice
            responses:
                "200":
                    description: "A list of anonymized comments."
                    content:
                        application/json:
                            schema:
                                type: array
                                items:
                                    type: string
                "403":
                    description: "Forbidden. The number of responses for this data slice is below the anonymity threshold, and the data cannot be shown to protect privacy."
    /reports:
        get:
            summary: "List Generated Reports"
            description: "Retrieves a list of all reports the user has previously generated for the 'My Reports' inbox."
            tags: ["Reports"]
            responses:
                "200":
                    description: "A list of the user's report records."
                    content:
                        application/json:
                            schema:
                                type: array
                                items:
                                    {}
                                    # Schema for the GeneratedReport object
        post:
            summary: "Generate a New Report (Asynchronous)"
            description: "Performs a pre-computation check on the request. If valid, queues a background job to generate a new report and returns a '202 Accepted' response. If the request is too large, it returns a '413 Payload Too Large' error."
            tags: ["Reports"]
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                report_type:
                                    type: string
                                file_format:
                                    type: string
                                    enum: [PDF, CSV]
                                parameters:
                                    type: object
                                    description: "JSON object containing filters for the report."
            responses:
                "202":
                    description: "Report generation job accepted. The response body contains the details of the queued job."
                "413":
                    description: "Payload Too Large. The report request is too broad and would consume excessive resources. The user should apply more specific filters."
                    content:
                        application/json:
                            schema:
                                $ref: "#/components/schemas/Error"
    /reports/{reportId}/download:
        get:
            summary: "Download a Completed Report"
            description: "Downloads the file for a report that was generated asynchronously."
            tags: ["Reports"]
            parameters:
                - name: reportId
                  in: path
                  required: true
                  schema:
                      type: integer
            responses:
                "200":
                    description: "The response body is the file stream."
                    content:
                        application/pdf: {}
                        text/csv: {}
                "404":
                    description: "Not Found. The report has expired or does not exist."

    # -----------------------------------------------------------------
    # Group 7: AI Assistant & Intelligence
    # -----------------------------------------------------------------
    /ai-assistant/filters:
        get:
            summary: "Get Available Filters for AI Assistant"
            description: "Retrieves the filter options available to the user for generating suggestions."
            tags: ["AI Assistant"]
            responses:
                "200":
                    description: "A list of available filter options."
                "403":
                    description: "Forbidden. User's role is not 'Faculty' or 'Department Head'."
    /ai-assistant/generate:
        post:
            summary: "Generate AI-Powered Suggestions (Asynchronous)"
            description: "Queues a background job to generate actionable suggestions and returns a '202 Accepted' response with the job details."
            tags: ["AI Assistant"]
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                action_type:
                                    type: string
                                    enum:
                                        [
                                            STRENGTHS_WEAKNESSES,
                                            IMPROVEMENT_SUGGESTIONS,
                                        ]
                                school_term_id:
                                    type: integer
                                assessment_period_id:
                                    type: integer
                                view_mode:
                                    type: string
                                    enum: [department, faculty]
                                target_id:
                                    type: integer
            responses:
                "202":
                    description: "Suggestion generation job accepted. The response body contains the details of the queued job for monitoring."
                "403":
                    description: "Forbidden. User's role is not 'Faculty' or 'Department Head'."
                "429":
                    description: "Too Many Requests. The user has exceeded the generation rate limit."
    /ai-suggestions:
        get:
            summary: "List Saved AI Suggestions"
            description: "Retrieves the history of all AI suggestions previously saved by the user."
            tags: ["AI Assistant"]
            responses:
                "200":
                    description: "A list of saved AI suggestion records."
        post:
            summary: "Save a Generated AI Suggestion"
            description: "Saves a generated suggestion and its context to the user's history."
            tags: ["AI Assistant"]
            requestBody:
                # Schema would reference the AISuggestion model
            responses:
                "201":
                    description: "Suggestion saved successfully."
    /ai-suggestions/{suggestionId}:
        get:
            summary: "Get a Specific Saved Suggestion"
            description: "Retrieves the full content of a single saved AI suggestion from the user's history."
            tags: ["AI Assistant"]
            parameters:
                - name: suggestionId
                  in: path
                  required: true
                  schema:
                      type: integer
            responses:
                "200":
                    description: "The full content of the saved suggestion."
                "404":
                    description: "Not Found. The suggestion does not exist or does not belong to the user."
    /ai-suggestions/{suggestionId}/export:
        get:
            summary: "Export a Saved Suggestion as a PDF"
            description: "Generates and streams a professionally formatted PDF of a saved AI suggestion. This endpoint is rate-limited."
            tags: ["AI Assistant"]
            parameters:
                - name: suggestionId
                  in: path
                  required: true
                  schema:
                      type: integer
            responses:
                "200":
                    description: "The response body is the PDF file stream."
                    content:
                        application/pdf: {}
                "429":
                    description: "Too Many Requests. The user has exceeded the export rate limit."

    # -----------------------------------------------------------------
    # Group 8: Shared Services
    # -----------------------------------------------------------------
    /profile:
        get:
            summary: "Get My Profile"
            description: "Retrieves the complete profile information for the currently authenticated user."
            tags: ["Shared Services"]
            responses:
                "200":
                    description: "The user's profile data."
        put:
            summary: "Update My Profile"
            description: "Updates non-critical information for the authenticated user's profile."
            tags: ["Shared Services"]
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                firstName:
                                    type: string
                                lastName:
                                    type: string
            responses:
                "200":
                    description: "Profile updated successfully."
    /profile/password:
        put:
            summary: "Change My Password"
            description: "Allows the authenticated user to change their own password."
            tags: ["Shared Services"]
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                currentPassword:
                                    type: string
                                newPassword:
                                    type: string
                                    description: "Must meet the defined password policy."
            responses:
                "204":
                    description: "Password changed successfully."
                "400":
                    description: "Bad Request. Current password was incorrect or new password violates policy."
    /notifications:
        get:
            summary: "List My Notifications"
            description: "Retrieves a list of notifications for the authenticated user."
            tags: ["Shared Services"]
            parameters:
                - name: status
                  in: query
                  schema:
                      type: string
                      enum: [unread, read]
            responses:
                "200":
                    description: "A paginated list of notifications."
    /notifications/{notificationId}/status:
        put:
            summary: "Update a Single Notification's Status"
            description: "Updates the status of a single notification (e.g., to 'read')."
            tags: ["Shared Services"]
            parameters:
                - name: notificationId
                  in: path
                  required: true
                  schema:
                      type: integer
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                status:
                                    type: string
                                    enum: [read, archived]
            responses:
                "204":
                    description: "Notification status updated successfully."
    /notifications/bulk-update:
        post:
            summary: "Bulk Update Notifications"
            description: "Performs a batch action (e.g., 'mark_as_read') on a list of notification IDs."
            tags: ["Shared Services"]
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                action:
                                    type: string
                                    enum: [mark_as_read, archive]
                                notification_ids:
                                    type: array
                                    items:
                                        type: integer
            responses:
                "204":
                    description: "Notifications updated successfully."
    /super-admin/universities/{universityId}/users:
        get:
            summary: "[Super Admin] List Users in a University"
            description: "Retrieves a list of all user accounts for a specific university tenant."
            tags: ["Super Admin"]
            parameters:
                - name: universityId
                  in: path
                  required: true
                  schema:
                      type: integer
            responses:
                "200":
                    description: "A list of user accounts."
    /super-admin/universities/{universityId}/users/{userId}/status:
        put:
            summary: "[Super Admin] Update a Tenant User's Status"
            description: "Allows a Super Admin to activate or deactivate a user's account in an emergency."
            tags: ["Super Admin"]
            parameters:
                - name: universityId
                  in: path
                  required: true
                  schema:
                      type: integer
                - name: userId
                  in: path
                  required: true
                  schema:
                      type: integer
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                status:
                                    type: string
                                    enum: [active, inactive]
            responses:
                "204":
                    description: "User status updated successfully."
    /super-admin/universities/{universityId}/users/{userId}/send-password-reset:
        post:
            summary: "[Super Admin] Trigger Password Reset for a User"
            description: "Sends a password reset email to a specific user, for use when an Admin is locked out."
            tags: ["Super Admin"]
            parameters:
                - name: universityId
                  in: path
                  required: true
                  schema:
                      type: integer
                - name: userId
                  in: path
                  required: true
                  schema:
                      type: integer
            responses:
                "202":
                    description: "Password reset email has been queued for sending."
```

***
