## **Coding Standards**

This section defines the mandatory, project-specific coding standards for the **Proficiency** platform. These are not exhaustive style guides; instead, they represent the minimal set of critical rules required to maintain architectural integrity, ensure consistency, and enable effective collaboration between human and AI developers.

We rely on automated formatters and linters (`Prettier`, `ESLint`, `Ruff`) to handle stylistic concerns. The standards documented here are architectural and procedural, and adherence is **mandatory** for all code committed to the repository.

### **Group 1: Guiding Principles & Philosophy**

The philosophy behind our coding standards is rooted in the project's core value of **balanced and effective simplicity**. Our goal is to provide clear, high-leverage guardrails that prevent common errors and architectural drift, not to micromanage implementation details.

1. **Architectural Enforcement:** These standards exist to enforce the key decisions outlined in this document, ensuring the implemented code accurately reflects the intended architecture.
2. **Pragmatism over Dogma:** Every rule is designed to solve a specific, anticipated problem within our technology stack and monorepo structure. We prioritize rules that have a high impact on quality and maintainability.
3. **Consistency is Key:** A consistent codebase is easier to read, understand, and maintain. These rules ensure that core patterns—such as data flow, error handling, and state management—are implemented uniformly across the entire application.
4. **Enabling Collaboration:** By establishing a clear and shared set of expectations, we reduce cognitive overhead for all developers and streamline the code review process, enabling both human and AI agents to contribute effectively and safely.

***

### **Group 2: Critical Fullstack & Monorepo Rules**

These rules are the cornerstone of our full-stack strategy, designed to ensure type safety, consistency, and maintainability at the boundary between the frontend and backend.

#### **2.1. Type Sharing & Data Contracts**

* **Single Source of Truth:** All data transfer objects (DTOs), API request/response schemas, and other shared types **must** be defined in the `packages/shared-types` workspace. This is the single source of truth for data contracts.
* **No Type Duplication:** Frontend and backend applications **must** import types directly from `@prof_monorepo/shared-types`. Redefining or duplicating these types in either the `apps/web` or `apps/api` codebase is strictly prohibited.
* **Technology:** All shared types will be defined using `Zod`. This allows us to derive TypeScript types automatically while also providing runtime validation on the backend, ensuring data integrity at the API boundary.

#### **2.2. API Interaction Patterns**

* **Frontend:** All API interactions **must** be managed through the dedicated service layer defined in **`apps/web/src/services/`**. Components **must not** make direct `fetch` or `axios` calls. Server state, caching, and re-fetching **must** be handled exclusively by `TanStack Query` hooks that wrap these service layer functions.
* **Backend:** API endpoints defined with FastAPI **must** use the Pydantic models (derived from Zod schemas in the shared package) for request body validation and response serialization. This enforces the data contract at runtime.

#### **2.3. Environment Variable Management**

* **Centralized Access:** Environment variables **must** be accessed through a centralized configuration module (**`apps/web/src/lib/config.ts`** for the frontend, **`apps/api/src/core/config.py`** for the backend).
* **No Direct `process.env`:** Direct calls to `process.env` (or its equivalent in Python) from within components, services, or application logic are strictly prohibited. This practice ensures that all configuration is managed in a single, predictable location, simplifying environment management and preventing configuration drift.

#### **2.4. Error Handling Consistency**

* **Standardized Error Responses:** The backend **must** return standardized JSON error responses, following the structure defined in `packages/shared-types`. This includes a unique error code, a human-readable message, and optional contextual details.
* **Frontend Error Propagation:** The frontend's API service layer **must** intercept all non-2xx responses and propagate a standardized error object. UI components will use the `error` state from `TanStack Query` to display user-friendly error messages (e.g., toast notifications, inline errors) based on the received error code.

#### **2.5. Commit Message Conventions**

* **Conventional Commits:** All git commits **must** adhere to the **Conventional Commits** specification. This provides a clear and automated way to track features, fixes, and breaking changes, which is essential for managing the project's version history and automating release notes.
* **Format:** The basic format is `<type>(<scope>): <subject>`. For example: `feat(api): add endpoint for user profile update`.

***

### **Group 3: Frontend Coding Standards (React & TypeScript)**

These standards ensure our React and TypeScript codebase is clean, consistent, and adheres to the architectural patterns established for the **Proficiency** frontend.

#### **3.1. Component Structure & Logic**

* **Atomic Design Principle:** Components **should** follow the principles of Atomic Design. Reusable, generic components (e.g., buttons, inputs) belong in **`apps/web/src/components/ui`**, while feature-specific, composite components belong in a co-located `components` directory within their feature folder (e.g., **`apps/web/src/components/features/dashboard/`**).
* **Separation of Concerns:** Component files **must** contain only UI-rendering logic (JSX) and local UI state management (`useState`). All business logic, data fetching, and state manipulation **must** be extracted into custom hooks (`use...`) or API service functions.
* **Strict Prop Typing:** All component props **must** be explicitly typed using TypeScript interfaces.
* **Hooks for Logic:** Custom hooks are the primary mechanism for encapsulating and reusing non-UI logic. A hook should have a single, clear responsibility (e.g., `useUserProfile`, `useEvaluationFormState`).
* **Performance-First Rendering:** For performance-critical components or long lists, employ code-splitting with `React.lazy` and `Suspense`, and virtualize long lists using a library like `@tanstack/react-virtual`.

#### **3.2. State Management Rules**

* **Server State:** All state originating from the server (e.g., user data, evaluation forms, dashboard metrics) **must** be managed exclusively by `TanStack Query`. This is the single source of truth for asynchronous data. The use of other libraries for managing server state is prohibited.
  * **Centralized Query Keys (New):** All query keys **must** be managed in a single, centralized file (`apps/web/src/services/queryKeys.ts`). This is the single source of truth for query identifiers, preventing the use of "magic strings" and simplifying cache invalidation. Keys **must** be structured as arrays with a clear hierarchy (e.g., `['users', 'detail', userId]`).
  * **Intentional Caching Defaults (New):** The global `QueryClient` instance **must** be configured with project-wide defaults for caching behavior. A `staleTime` of at least `60_000` (60 seconds) is required to prevent overly aggressive refetching, with `gcTime` (garbage collection) set to a longer duration (e.g., `5 * 60 * 1000`). Individual queries can override these defaults where necessary.
  * **Exclusive Use:** `TanStack Query` **must** be used exclusively for managing all state originating from the server.
* **Client State:**
  * **Local Component State:** `useState` and `useReducer` **must** be used for managing state that is local to a single component (e.g., form input values, modal visibility).
  * **Shared Client State:** For state that needs to be shared across multiple components without being passed down through many layers of props (e.g., theme, authenticated user object), the React `Context` API is the approved solution.
* **No Other Global State Managers:** The use of other global state management libraries (e.g., Redux, Zustand, MobX) is strictly prohibited. Our state management strategy is intentionally lean to align with the project's principle of effective simplicity.

#### **3.3. Styling Conventions (Tailwind CSS)**

* **Mobile-First:** All styles **must** be developed for small viewports first, then enhanced for larger screens using Tailwind's responsive prefixes (`sm:`, `md:`, etc.).
* **Utility-First:** Components **must** be styled primarily using **Tailwind CSS** utility classes directly in the JSX. This is our standard for applying styles.
* **Component-Specific CSS:** For complex, state-dependent, or reusable style patterns that are difficult to manage with inline utilities, a co-located `.css` or `.module.css` file can be used, leveraging Tailwind's `@apply` directive. This should be the exception, not the rule.
* **`clsx` for Conditional Classes:** The `clsx` utility **must** be used to conditionally apply classes to elements, ensuring a clean and readable approach to dynamic styling.
* **Design Tokens:** All colors, fonts, and spacing **must** be defined as design tokens in `tailwind.config.ts`.

#### **3.4. Frontend Testing Rules**

* **Co-location of Tests:** `Vitest` unit and integration tests **must** be co-located with the components or hooks they are testing in a `__tests__` subdirectory (e.g., **`apps/web/src/components/features/dashboard/__tests__/DashboardCard.test.tsx`**).
* **User-Centric Testing:** Tests **should** prioritize simulating user interactions and verifying the resulting output, rather than testing implementation details. Use the **`@testing-library/react`** package for querying the DOM in a way that is accessible to users.
* **Mocking:** API calls made via `TanStack Query` and our service layer **must** be mocked at the test level using **`msw` (Mock Service Worker)** to ensure tests are fast, reliable, and independent of the live backend.
* **Accessibility Testing:** Automated accessibility checks using `axe-core` **must** be integrated into our component test suite.

***

### **Group 4: Backend Coding Standards (Python & FastAPI)**

These standards enforce the layered architecture and best practices for our Python backend, ensuring the codebase is robust, scalable, and maintainable.

#### **4.1. Layered Architecture Adherence**

* **Strict Separation of Concerns:** Code **must** be strictly organized into the three defined layers:
  1. **Endpoints (`/routers`):** This layer is responsible *only* for handling HTTP requests and responses. It defines API routes, handles request validation using Pydantic models, and calls the appropriate service layer function. No business logic is permitted in this layer.
  2. **Services (`/services`):** This layer contains all core business logic. It orchestrates operations, performs calculations, enforces business rules, and coordinates calls to one or more repositories.
  3. **Repositories (`/repositories`):** This layer is the sole intermediary with the database. It contains all SQLAlchemy queries and logic for data persistence and retrieval. Services **must not** contain raw SQL or SQLAlchemy queries.
* **Data Flow:** The flow of control **must** be unidirectional: `Endpoint` -> `Service` -> `Repository`. A lower layer (like a repository) **must never** call an upper layer (like a service).

#### **4.2. Asynchronous Code (async/await)**

* **Async Everywhere:** All I/O-bound operations (database calls, external API requests) **must** be asynchronous. Therefore, all endpoint, service, and repository methods that perform I/O **must** be defined with `async def`.
* **Consistent `await`:** Ensure that every `async` function call is properly awaited. The `Ruff` linter is configured to detect and flag missing `await` statements.

#### **4.3. Pydantic & SQLAlchemy Patterns**

* **Pydantic for Validation:** Pydantic models (derived from the Zod schemas in `packages/shared-types`) **must** be used in the endpoint layer for all request body validation and response serialization. This is our primary mechanism for enforcing data contracts.
* **SQLAlchemy for Data Model:** SQLAlchemy models (`/models`) define the database table structures. These are distinct from Pydantic schemas and should only be used within the repository layer.
* **Repository Pattern:** All database interactions **must** be encapsulated within repository classes. Services **must** depend on repository abstractions (not SQLAlchemy sessions directly) to fetch and persist data.

#### **4.4. Background Job Standards**

* **`RQ` for Asynchronous Tasks:** Any long-running or non-critical task (e.g., sending emails, generating reports, AI processing) **must** be executed as a background job using the **`RQ` (Redis Queue)** library.
* **Enqueue in Services:** The enqueuing of jobs (e.g., `queue.enqueue(...)`) **must** be performed from the service layer, as this is part of the business logic.

#### **4.5. Backend Testing Rules**

* **`Pytest` as the Standard:** All backend tests **must** be written using the `Pytest` framework.
* **Test Separation:**
  * **Unit Tests:** Tests for the service layer **must** be unit tests. They **must** mock repository dependencies to isolate the business logic and ensure speed.
  * **Integration Tests:** Tests for the repository and endpoint layers **must** be integration tests that run against a real, but separate, test database. This validates SQL queries and the full request/response cycle.
* **Co-location of Tests:** Tests **must** be located in the `/tests` directory, mirroring the application's package structure (e.g., `tests/services/test_evaluation_service.py`).

***

### **Group 5: Consolidated Naming Conventions**

A single, consistent naming strategy is crucial for a project's long-term readability and maintainability. The following conventions are mandatory for all code, database schemas, and file structures.

| Element Category              | Convention            | Example                                                  |
| :---------------------------- | :-------------------- | :------------------------------------------------------- |
| **General & Monorepo**        |                       |                                                          |
| Directories                   | `kebab-case`          | **`apps/web/src/components/features/user-dashboard`**    |
| **Frontend (React/TS)**       |                       |                                                          |
| Component Files & Names       | `PascalCase.tsx`      | `EvaluationForm.tsx` -> `<EvaluationForm />`             |
| Custom Hook Files & Functions | `useCamelCase.ts`     | `useEvaluationState.ts` -> `useEvaluationState()`        |
| Service & API Files           | `camelCase.ts`        | `apiService.ts`, `evaluationService.ts`                  |
| Service Functions             | `camelCase`           | `getUserProfile(id)`, `submitEvaluation(data)`           |
| Type Interfaces/Zod Schemas   | `PascalCase`          | `interface UserProfile`, `const UserProfileSchema = ...` |
| Test Files                    | `PascalCase.test.tsx` | `EvaluationForm.test.tsx`                                |
| **Backend (Python/FastAPI)**  |                       |                                                          |
| Python Files (Modules)        | `snake_case.py`       | `evaluation_service.py`, `user_repository.py`            |
| Classes (Services, Repos)     | `PascalCase`          | `EvaluationService`, `UserRepository`                    |
| Functions & Methods           | `snake_case`          | `async def get_user_profile(user_id: int):`              |
| Variables                     | `snake_case`          | `current_user`, `form_data`                              |
| API Router Files & Variables  | `snake_case.py`       | `users_router.py` -> `router = APIRouter()`              |
| Pydantic Schemas              | `PascalCase`          | `UserCreate`, `EvaluationRead`, `FormUpdate`             |
| SQLAlchemy Models             | `PascalCase`          | `class User(Base):`, `class Evaluation(Base):`           |
| Test Files                    | `test_snake_case.py`  | `test_evaluation_service.py`                             |
| Test Functions                | `test_...`            | `def test_submit_evaluation_success():`                  |
| **Database (MySQL/MariaDB)**  |                       |                                                          |
| Tables                        | `plural_snake_case`   | `users`, `evaluation_forms`, `assessment_periods`        |
| Columns                       | `snake_case`          | `first_name`, `is_active`, `created_at`                  |
| Primary Keys                  | `id`                  | `id`                                                     |
| Foreign Keys                  | `singular_name_id`    | `user_id`, `form_id`, `period_id`                        |
| Indexes                       | `ix_table_column`     | `ix_users_email`, `ix_evaluations_status`                |

***
