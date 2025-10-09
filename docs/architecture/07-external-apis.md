## **External APIs**

This section details the external services that the Proficiency platform relies on, the components that interact with them, and the architectural patterns used to ensure resilient and maintainable integrations.

### **Gemini API**

* **Purpose**: To provide the advanced Large Language Model (LLM) capabilities required for the "AI Assistant" feature, specifically for generating actionable suggestions based on processed evaluation data. This fulfills the requirement for an advanced AI feature as outlined in the PRD.
* **Interacting Component**: The `[Worker] AI Suggestion Job Handler` is the sole component responsible for making outbound requests to the Gemini API. This interaction is intentionally isolated within an asynchronous worker to prevent blocking the main API and to manage the integration's potential latency and cost.
* **Architectural Considerations**:
  * **Circuit Breaker Pattern**: The external API call within the job handler **must** be wrapped in a Circuit Breaker pattern. If the Gemini API becomes unresponsive or returns repeated failures, the circuit will open, causing subsequent jobs to fail fast without waiting for a timeout. This protects our system from cascading failures and resource exhaustion caused by an external dependency. The frontend must handle a resulting `503 Service Unavailable` error gracefully.
  * **Externalized Prompt Templates**: The prompts sent to the Gemini API **must not** be hardcoded within the application logic. They will be constructed from templates stored in an externalized configuration file (e.g., `prompts.json`). This allows for prompt engineering and refinement without requiring a code deployment.
  * **Mandatory Mocking Layer**: For all non-production environments (development, testing, staging), a mocking layer for the Gemini API call is a mandatory requirement. This enables cost-effective, predictable, and reliable testing of the AI Assistant feature without incurring API costs or being dependent on the external service's availability.

### **External SMTP Relay**

* **Purpose**: To handle the delivery of all transactional emails sent by the platform. This includes university verification emails, user notifications for import completions, flag resolutions, and password resets.
* **Interacting Component**: The `[Backend] Notification Service` is responsible for creating notification records. It then enqueues a job for a generic `[Worker] Email Dispatch Job Handler` to process. This handler makes the outbound request to the SMTP relay.
* **Architectural Considerations**:
  * **Asynchronous & Idempotent Jobs**: All email dispatch operations are handled asynchronously via the RQ job queue. The worker jobs **must be designed to be idempotent**. This ensures that if a job is retried due to a transient failure with the SMTP provider, a duplicate email will not be sent to the user.
  * **Provider Abstraction**: The specific SMTP provider (e.g., SendGrid, Mailgun) will be abstracted behind a simple interface. Connection details and API keys will be stored in environment variables, allowing the provider to be swapped with minimal code changes.

***
