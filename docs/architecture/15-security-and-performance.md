## Security and Performance

### **Group 1: Comprehensive Security Requirements**

This group defines the complete security posture for the Proficiency platform. It establishes mandatory, non-negotiable rules and patterns for both frontend and backend development to protect against common vulnerabilities, ensure data integrity, and build user trust. These principles are a direct implementation of the security requirements outlined in the PRD.

#### **1.1. Frontend Security**

This section outlines our client-side, defense-in-depth strategy.

* **Content Security Policy (CSP)**: To mitigate Cross-Site Scripting (XSS) and other injection attacks, a strict Content Security Policy **must** be implemented. This policy will be set as an HTTP header by the **Caddy reverse proxy** in the production environment. The policy is as follows:

  ```
  default-src 'self';
  script-src 'self';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data:;
  connect-src 'self';
  font-src 'self';
  object-src 'none';
  frame-ancestors 'none';
  ```

  **Rationale**: This policy ensures that all executable code, styles, fonts, and images are loaded only from our own domain, severely restricting the attack surface for code injection. The `'unsafe-inline'` for styles is a necessary concession for some UI library patterns but should be reviewed post-V1 for potential tightening.

* **Cross-Site Scripting (XSS) Prevention**: While our CSP provides a strong defense, our primary prevention mechanism is React's native security feature. React automatically escapes any content rendered through JSX, preventing malicious scripts from being injected into the DOM.

  * **CRITICAL RULE**: The use of `dangerouslySetInnerHTML` is strictly prohibited throughout the application. Any exception to this rule requires a formal architectural review and must be paired with a robust, server-side sanitization library for the specific content.

* **Secure JWT Storage**: To protect user session tokens from XSS-based theft, we will implement a secure, cookie-based storage strategy:

  * **Refresh Token**: The long-lived refresh token **must** be stored in a secure, `HttpOnly` cookie set by the backend. This makes it completely inaccessible to client-side JavaScript. The cookie must also be configured with `SameSite=Strict` and the `Secure` flag.
  * **Access Token**: The short-lived access token will be returned in the body of the login/refresh response and **must** be stored only in the application's memory (e.g., in a React Context). It **must not** be persisted in `localStorage` or `sessionStorage`.

***

#### **1.2. Backend Security**

This section defines the mandatory security measures at the API layer.

* **Input Validation**: All data entering the API from an external source **must** be validated. This is enforced by our architecture: every API endpoint **must** use Pydantic models for request bodies, query parameters, and path parameters. This acts as a strict, centrally-managed whitelist for all incoming data, rejecting any request that does not conform to the expected schema.

* **Rate Limiting**: To ensure system stability and prevent abuse, rate limiting **must** be applied to sensitive or resource-intensive endpoints, as required by **NFR12**. This will be implemented using a FastAPI middleware (`slowapi`). The following endpoints are the initial targets, with limits configurable via the `UniversitySetting` model:

  * All authentication endpoints (`/auth/login`, `/register`, etc.).
  * The AI Assistant endpoint (`/ai-assistant/generate`).
  * The Report Generation endpoint (`/reports`).

* **Cross-Origin Resource Sharing (CORS)**: Because the frontend and backend are served from the same origin via the Caddy reverse proxy, our CORS policy can and **must** be highly restrictive. The FastAPI `CORSMiddleware` will be configured to allow requests **only** from the specific frontend domains for our production and staging environments. Wildcard (`*`) origins are strictly prohibited.

***

#### **1.3. Authentication & Session Security**

This section details the implementation of our secure authentication and session management system.

* **Token & Session Invalidation**: We will use the `token_version` integer field on the `users` and `super_admins` tables as the definitive mechanism for stateless session invalidation.

  * **Mandatory Action**: Any action that should invalidate a user's active sessions (e.g., a password change, an admin-triggered "log out all devices") **must** increment the `token_version` for that user in the database.
  * **Mandatory Check**: The primary security dependency (`get_current_user`) **must**, on every single authenticated request, compare the `tv` claim within the JWT access token against the user's current `token_version` from the database. If they do not match, the token is considered invalid, and the request **must** be rejected with a `401 Unauthorized` status.

* **Password Policy & Storage**:

  * **Storage**: All user and super admin passwords **must** be hashed using the **bcrypt** algorithm, as implemented by the `passlib` library. Plaintext passwords must never be logged or stored.
  * **Policy**: The password policy defined in the API Specification for the `/register` endpoint is the official standard for the platform: "Minimum 12 characters, with at least one uppercase, one lowercase, one number, and one special character". This **must** be enforced by the backend during registration and password change operations.

***

### **Group 2: Holistic Performance Optimization**

This group establishes the performance budgets, service level objectives (SLOs), and specific technical strategies we will implement to ensure the Proficiency application is fast, responsive, and scalable. These patterns are designed to provide an excellent user experience while maintaining a cost-effective and manageable infrastructure.

### **2.1. Frontend Performance**

This section defines our client-side performance strategy, focusing on a fast initial load and a responsive user interface.

* **Performance Budget (Bundle Size)**: The initial JavaScript bundle size is the single most critical factor for a fast "Time to Interactive."

  * **Mandatory Target**: The initial production JavaScript bundle for the application shell **must not exceed 250KB gzipped**.
  * **Monitoring**: The development team **must** integrate a bundle analysis tool (e.g., `vite-bundle-visualizer`) into the build pipeline to continuously monitor bundle size and identify optimization opportunities.

* **Loading Strategy (Code-Splitting & Lazy Loading)**: To meet our performance budget and ensure fast page loads, we will implement an aggressive code-splitting strategy.

  * **Route-Based Splitting**: As defined in our Frontend Architecture, every page-level component located in `src/pages/` **must** be loaded using `React.lazy`. This is the primary mechanism for ensuring users only download the code for the screen they are viewing.
  * **Component-Based Splitting**: Large, non-critical components that are not immediately visible (e.g., complex dialogs, charts within inactive tabs) **must** also be loaded using `React.lazy`. The `CommentViewerDialog` is a prime candidate for this pattern.

* **Client-Side Caching Strategy**: We will leverage browser caching to minimize re-downloads for returning users.
  * **Hashed Assets**: The Vite build process automatically generates filenames with content hashes (e.g., `main.[hash].js`). Our Caddy server **must** be configured to serve all hashed assets (JS, CSS, images) with an aggressive, long-term caching header: `Cache-Control: public, max-age=31536000, immutable`.
  * **Entry Point**: The main `index.html` file **must** be served with a `Cache-Control: no-cache` header to ensure users always fetch the latest version of the application shell, which in turn will reference the latest hashed assets.

* **Asset Optimization Strategy**: To ensure a fast and efficient production build, the Vite build process will be configured for standard production optimizations. This includes:
  * **Tree-Shaking:** Automatically eliminates unused code from the final production bundles.
  * **Minification:** Minifies all JavaScript and CSS assets to reduce file size and improve network transfer times.
  * **Code-Splitting:** As detailed in the Loading Strategy, code is automatically split on a per-route basis.

### **2.2. Backend Performance**

This section defines our server-side performance targets and optimization strategies.

* **API Response Time Targets (SLOs)**: To ensure a responsive user experience, the following Service Level Objectives (SLOs) are established for our API:

  * **P95 (95th percentile) < 200ms** for all standard data retrieval and CRUD endpoints.
  * **P99 (99th percentile) < 500ms** for the same endpoints.
  * **Note**: These targets apply to synchronous API operations and exclude the time taken by asynchronous background jobs. The API endpoints that enqueue jobs should respond in **< 50ms**.
  * **Monitoring**: These metrics **must** be tracked using our Prometheus and Grafana monitoring stack.

* **Database Optimization Strategy**: Efficient database interaction is paramount for backend performance.

  * **Mandatory Indexing**: All foreign key columns and any columns frequently used in `WHERE`, `JOIN`, or `ORDER BY` clauses **must** be indexed. The complex queries required for dashboard data aggregation are a primary focus for this requirement.
  * **Query Analysis**: Developers **must** use the `EXPLAIN` command to analyze the query plan for any complex or slow-running database query to ensure proper index utilization and to identify and eliminate full table scans.
  * **Connection Pooling**: The application **must** use a properly configured connection pool (managed by SQLAlchemy) to efficiently manage and reuse database connections, minimizing the overhead of establishing new connections for each request.

* **Server-Side Caching Strategy**: We will leverage our Redis instance to reduce database load and improve response times for frequently accessed data.
  * **Provisional Data**: The primary caching mechanism for dashboard data is our "micro-batching" pattern, where the `Provisional Data Micro-batching Job` pre-calculates and stores results in a dedicated `provisional_aggregates` table. This acts as a materialized view, which is the most effective form of caching for this use case and a direct implementation of FR8.
  * **Cache-Aside Pattern**: For other potentially expensive and frequently read, non-critical data (e.g., university settings, available filter options), a standard cache-aside pattern will be implemented. Data will be fetched from Redis; on a cache miss, it will be retrieved from the database and then stored in Redis with a short, defined Time To Live (TTL) of **1 to 5 minutes**.

***
