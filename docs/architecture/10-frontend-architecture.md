## **Frontend Architecture**

This section details the architecture of the React-based frontend application. It establishes the foundational patterns, structures, and strategies to ensure the user interface is scalable, maintainable, performant, and testable. The architecture is divided into six core groups, covering all aspects from component structure to error handling.

***

### **Group 1: Component Architecture & Organization**

This group establishes the foundational rules for how React components are structured, organized, and created. A consistent and logical component architecture is paramount for long-term maintainability, developer efficiency, and scalability of the user interface.

#### **1.1. Component Organization (Directory Structure)**

All frontend components will reside within the `src/components` directory, organized according to a hybrid Atomic Design and feature-based methodology. This structure provides a clear separation of concerns, enhances reusability, and simplifies navigation of the codebase.

The primary structure is as follows:

```
/src/components/
├── /ui/               # Reusable, unstyled base components from shadcn/ui
├── /layouts/          # Structural components defining page layouts (e.g., AppLayout, AuthLayout)
├── /shared/           # Custom, project-specific, reusable components (e.g., PageHeader, StatCard)
└── /features/         # Components tied to a specific feature or domain
    ├── /forms/        # Components for the dynamic form builder (e.g., FormCanvas, QuestionEditor)
    ├── /dashboard/    # Components for the main dashboard views (e.g., OverallScoreChart, FeedbackTrendGraph)
    └── /evaluations/  # Components for submitting and viewing evaluations (e.g., EvaluationForm, SubmissionStatus)
```

**Rationale:**

* **/ui/:** This directory is exclusively for the low-level, headless components provided by `shadcn/ui` (e.g., Button, Input, Card). We do not modify these directly; they are the primitive building blocks.
* **/layouts/:** These components define the main structural containers of the application, such as sidebars, headers, and content areas. They manage the overall page structure that other components are placed into.
* **/shared/:** This is for custom components that are used across multiple features but are specific to the "Proficiency" application's design system. A `PageHeader` with a specific title and breadcrumb style is a perfect example. This promotes a DRY (Don't Repeat Yourself) approach.
* **/features/:** This is the most critical directory for domain-specific logic. By grouping components by feature (e.g., `forms`, `dashboard`), we co-locate related UI elements, making it intuitive to find and modify all parts of a specific application area.

#### **1.2. Component Template & Best Practices**

To ensure consistency, readability, and adherence to best practices, all new components must follow a standardized structure and set of conventions.

**Standard Component File Structure (using TypeScript):**

```typescript
// src/components/features/forms/FormCanvas.tsx

// 1. Import Dependencies (React, libraries, then local modules)
import React from "react";
import { useDrop } from "react-dnd";
import { FormElement } from "@/types"; // Assuming a types directory
import { QuestionBlock } from "./QuestionBlock";

// 2. Define Component Props Interface
interface FormCanvasProps {
    elements: FormElement[];
    onDropElement: (element: FormElement) => void;
    onUpdateElement: (id: string, newContent: string) => void;
}

// 3. The Component Function
const FormCanvas: React.FC<FormCanvasProps> = ({
    elements,
    onDropElement,
    onUpdateElement,
}) => {
    // 4. Hooks (useDrop, useState, useEffect, etc.)
    const [{ isOver }, drop] = useDrop(() => ({
        accept: "form-element",
        drop: (item: FormElement) => onDropElement(item),
        collect: (monitor) => ({
            isOver: !!monitor.isOver(),
        }),
    }));

    // 5. Event Handlers & Logic
    const handleElementUpdate = (id: string, content: string) => {
        // Business logic for updating an element
        onUpdateElement(id, content);
    };

    // 6. JSX Return
    return (
        <div
            ref={drop}
            className={`p-4 border-2 border-dashed rounded-md min-h-[500px] ${
                isOver
                    ? "border-primary bg-primary-foreground"
                    : "border-border"
            }`}
            aria-label="Form editor canvas"
        >
            {elements.length === 0 ? (
                <p className="text-center text-muted-foreground">
                    Drop form elements here to begin.
                </p>
            ) : (
                elements.map((element) => (
                    <QuestionBlock
                        key={element.id}
                        element={element}
                        onUpdate={handleElementUpdate}
                    />
                ))
            )}
        </div>
    );
};

// 7. Export the Component
export default FormCanvas;
```

**Core Best Practices:**

* **TypeScript:** All components **must** be written in TypeScript (`.tsx`) with strongly typed props to ensure type safety and improve developer experience.
* **Props Destructuring:** Always destructure props in the function signature for clarity.
* **Functional Components & Hooks:** Exclusively use functional components with React Hooks. Class components are prohibited.
* **Styling:** Use **Tailwind CSS** for all styling via the `className` prop. Avoid inline styles (`style={{}}`) unless absolutely necessary for dynamic properties that cannot be handled by class toggling.
* **Accessibility (`aria-*`)**: Include appropriate ARIA attributes to ensure the application is accessible to users with disabilities, as demonstrated with `aria-label` in the example.
* **Separation of Concerns:** Keep components focused on presentation. Complex business logic, state management, and API calls should be handled by custom hooks or the services layer (to be defined in later groups), not directly within UI components.

#### Tailwind CSS v4 Configuration

Tailwind CSS is delivered through the CSS-first workflow introduced in v4. The global stylesheet `apps/web/src/index.css` must:

* `@import "tailwindcss";` as the first statement so the framework utilities are available.
* Declare project design tokens with the `@theme` directive (colors, spacing, typography) instead of editing a `tailwind.config.js` file. Tailwind Labs highlights this workflow in the v4.0 release notes (context7: Tailwind CSS v4 – “Define Tailwind CSS configuration directly in CSS with @theme”).
* Define any project-specific utilities with the new `@utility` directive when the standard primitives are insufficient.

Legacy files such as `tailwind.config.js` or `postcss.config.js` must not be added unless Tailwind Labs reintroduces them; customization lives entirely in CSS under this approach.

***

### **Group 2: State Management Architecture**

This group defines the strategy for managing state within the frontend application. A clear distinction between different types of state is crucial for building a performant and predictable UI. Our architecture formally separates **Server State** (data originating from the backend) from **Client State** (UI-specific state), employing the best-suited tool for each job.

#### **2.1. State Management Strategy (Server vs. Client State)**

The core of our strategy is the explicit separation of state into two categories:

1. **Server State:** Data that is persisted on the server and is not owned by the client. This includes user data, evaluation forms, submissions, etc. This data is fetched asynchronously, can become "stale," and can be shared across different parts of the application.

   * **Tool:** **TanStack Query (formerly React Query)** will be used exclusively for managing all server state.

2. **Client State:** Data that is local to the client and owned by the UI. This includes form input values, modal visibility, UI themes, and other ephemeral state that is not persisted in the database.

   * **Tool:** **React Context and Hooks (`useState`, `useReducer`)** will be used for managing client state.

**Rationale:** Using a specialized server state library like TanStack Query eliminates the need to manage complex logic for caching, refetching, and background updates in a global client state manager (like Redux or Zustand), which dramatically simplifies the codebase and improves performance.

#### **2.2. Server State Management (TanStack Query Patterns)**

TanStack Query will be the sole authority for fetching, caching, and updating server data. We will standardize its use through custom hooks to encapsulate query logic and promote reusability.

**Key Conventions:**

* **Custom Hooks:** All TanStack Query logic (`useQuery`, `useMutation`) **must** be wrapped in a custom hook co-located with the feature it belongs to (e.g., `useFetchEvaluationForm`, `useUpdateUserProfile`).
* **Query Keys:** Query keys will be structured as an array, starting with the domain/feature name and followed by any unique identifiers. Example: `['forms', 'detail', formId]`.
* **Query Invalidation:** To ensure data freshness after a mutation, we will use query invalidation rather than manually updating the cache. This is the simplest and most reliable approach. This pattern is critical for handling scenarios like the `409 Conflict` error, where we must refetch the latest data.

**Example: `useQuery` Custom Hook**

```typescript
// src/features/forms/hooks/useFetchForm.ts
import { useQuery } from "@tanstack/react-query";
import { formsService } from "@/services/formsService"; // Assumes a service layer

export const useFetchForm = (formId: string) => {
    return useQuery({
        queryKey: ["forms", "detail", formId],
        queryFn: () => formsService.getFormById(formId),
        // stale-while-revalidate is the default, which is ideal for our use case
        // Add other options like `enabled` if the query depends on other state
        enabled: !!formId,
    });
};
```

**Example: `useMutation` Custom Hook**

```typescript
// src/features/profile/hooks/useUpdateProfile.ts
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { profileService } from "@/services/profileService";
import { UserProfile } from "@/types";

export const useUpdateProfile = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (profileData: Partial<UserProfile>) =>
            profileService.update(profileData),
        onSuccess: (data) => {
            // Invalidate all queries related to the user's profile to refetch fresh data
            queryClient.invalidateQueries({ queryKey: ["profile", data.id] });
            // Optionally show a success notification
        },
        onError: (error) => {
            // Handle error, e.g., show an error notification
        },
    });
};
```

#### **2.3. Client/UI State Management (React Context & Hooks)**

For state that is purely client-side, we will use React's built-in capabilities to avoid adding unnecessary library dependencies.

* **`useState` / `useReducer`:** This is the default choice for all component-local state (e.g., input values, toggles, component-specific loading states).
* **React Context:** Context will be used sparingly for global UI state that needs to be shared across deeply nested components without prop drilling. Potential use cases include:
  * `AuthContext`: Storing the current authenticated user object and authentication status.
  * `ThemeContext`: Managing the application's light/dark mode.

**Example: `AuthContext`**

```typescript
// src/context/AuthContext.tsx
import React, { createContext, useContext, useState, ReactNode } from "react";
import { User } from "@/types";

interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
    login: (userData: User) => void;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);

    const login = (userData: User) => setUser(userData);
    const logout = () => setUser(null);

    const value = { user, isAuthenticated: !!user, login, logout };

    return (
        <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
};
```

***

### **Group 3: Routing & Navigation Architecture**

This section lays out the application's navigation structure and defines the security model for protecting routes. It leverages **React Router** to manage user flows and ensures a clear separation between public-facing pages, authenticated user layouts, and role-specific access control.

***

#### **3.1. Route Organization & Structure**

To ensure clarity and maintainability, all routing logic will be centralized. The application will use a layout-based strategy to distinguish between different user experiences: a simple layout for authentication pages (`AuthLayout`) and a full application shell with a sidebar for authenticated users (`AppLayout`), as specified in the UI/UX document.

**Directory Structure:**

All routing configuration will be located in the `src/routes/` directory.

```
/src/routes/
├── index.tsx         # Main router configuration using React Router
├── paths.ts          # Centralized path constants to avoid magic strings
└── RouteGuard.tsx    # Component for handling protected routes and authorization
```

**Route Definitions (`index.tsx`):**

The main router will use `React.lazy` for code-splitting page-level components. This is a critical performance optimization that ensures users only download the code necessary for the view they are accessing.

```typescript
// src/routes/index.tsx
import React, { Suspense, lazy } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AppLayout } from "@/components/layouts/AppLayout";
import { AuthLayout } from "@/components/layouts/AuthLayout";
import { RouteGuard } from "./RouteGuard";
import { PATHS } from "./paths";

// Lazy-loaded page components for performance
const LoginPage = lazy(() => import("@/pages/Login"));
const RegisterPage = lazy(() => import("@/pages/Register"));
const DashboardPage = lazy(() => import("@/pages/Dashboard"));
const AiAssistantPage = lazy(() => import("@/pages/AiAssistant"));
const UnauthorizedPage = lazy(() => import("@/pages/Unauthorized"));
// ... other lazy-loaded pages

const AppRouter: React.FC = () => {
    return (
        <BrowserRouter>
            <Suspense fallback={<div>Loading...</div>}>
                <Routes>
                    {/* Public routes with a simple layout */}
                    <Route element={<AuthLayout />}>
                        <Route path={PATHS.LOGIN} element={<LoginPage />} />
                        <Route
                            path={PATHS.REGISTER}
                            element={<RegisterPage />}
                        />
                        {/* Super Admin login route will also be placed here */}
                    </Route>

                    {/* All authenticated routes are nested within the main AppLayout */}
                    <Route path={PATHS.HOME} element={<AppLayout />}>
                        <Route
                            index
                            element={
                                <RouteGuard
                                    roles={[
                                        "Student",
                                        "Faculty",
                                        "Department Head",
                                        "Admin",
                                        "Super Admin",
                                    ]}
                                >
                                    <DashboardPage />
                                </RouteGuard>
                            }
                        />
                        <Route
                            path={PATHS.AI_ASSISTANT}
                            element={
                                <RouteGuard
                                    roles={["Faculty", "Department Head"]}
                                >
                                    <AiAssistantPage />
                                </RouteGuard>
                            }
                        />
                        {/* Additional routes for Admin, Super Admin, etc. will be nested here, each wrapped in a RouteGuard */}
                        <Route
                            path="/403-unauthorized"
                            element={<UnauthorizedPage />}
                        />
                    </Route>
                </Routes>
            </Suspense>
        </BrowserRouter>
    );
};

export default AppRouter;
```

**Path Constants (`paths.ts`):**

To prevent hardcoded URL strings and simplify maintenance, all application paths will be defined in a central constants file.

```typescript
// src/routes/paths.ts
export const PATHS = {
    HOME: "/",
    LOGIN: "/login",
    REGISTER: "/register",
    DASHBOARD: "/dashboard",
    AI_ASSISTANT: "/ai-assistant",
    FORM_MANAGEMENT: "/admin/forms",
    // ... all other application paths
};
```

***

#### **3.2. Protected Route & Authentication Handling**

Route protection is the central mechanism for enforcing the role-based access control defined in the PRD. This will be handled by a dedicated `RouteGuard` component that acts as a wrapper, checking the user's authentication state and role before granting access.

**Strategy:**

The `RouteGuard` will consume the `AuthContext` (defined in the State Management section) to access the current user's authentication status and roles. It performs the following checks:

1. **Authentication:** Is the user logged in? If not, redirect to the login page.
2. **Authorization:** If logged in, does the user's role match one of the roles permitted for the route? If not, redirect to an "Unauthorized" page.
3. **Access Granted:** If both checks pass, render the requested page.

**Implementation (`RouteGuard.tsx`):**

```typescript
// src/routes/RouteGuard.tsx
import React from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import { RoleName } from "@/types";
import { PATHS } from "./paths";

interface RouteGuardProps {
    roles: RoleName[];
}

export const RouteGuard: React.FC<RouteGuardProps> = ({ roles }) => {
    const { isAuthenticated, user } = useAuth();
    const location = useLocation();

    // 1. Check for authentication
    if (!isAuthenticated) {
        // Redirect to login, preserving the intended destination for a better user experience
        return <Navigate to={PATHS.LOGIN} state={{ from: location }} replace />;
    }

    // 2. Check for authorization (role match)
    // This assumes the `user` object from AuthContext contains a `roles` array
    const isAuthorized = user?.roles.some((userRole) =>
        roles.includes(userRole)
    );

    if (!isAuthorized) {
        // User is authenticated but does not have the required role
        return <Navigate to="/403-unauthorized" replace />;
    }

    // 3. If authenticated and authorized, render the nested routes/component
    return <Outlet />;
};
```

***

### **Group 4: API Integration & Services Layer**.

This section defines the standardized layer for all communication with the backend API. It consists of a centrally configured API client that handles universal concerns like authentication and error handling, and a set of "service" files that encapsulate the logic for interacting with specific API domains. This pattern is a critical best practice that decouples UI components from data-fetching logic.

***

#### **4.1. API Client Configuration (Axios Instance)**

To ensure consistency and simplify API calls, we will create a single, pre-configured instance of Axios. This instance will be used for every outbound request from the frontend and will be responsible for three critical tasks:

1. Setting the base URL for all API calls to `/api/v1`.
2. Automatically attaching the JWT authentication token to the headers of every protected request.
3. Intercepting all API responses to provide a centralized point for global error handling (e.g., for `409 Conflict` errors).

**File Location:**

```
/src/lib/apiClient.ts    # The configured Axios instance
```

**Implementation (`apiClient.ts`):**

```typescript
// src/lib/apiClient.ts
import axios from "axios";

// Create a new Axios instance with a predefined configuration
const apiClient = axios.create({
    baseURL: "/api/v1", // As defined in the API Specification
    headers: {
        "Content-Type": "application/json",
    },
});

// Request Interceptor: This function will run before every request is sent.
apiClient.interceptors.request.use(
    (config) => {
        // Retrieve the auth token from storage (e.g., localStorage)
        const token = localStorage.getItem("accessToken");
        if (token) {
            // If a token exists, add it to the Authorization header
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        // Handle request errors
        return Promise.reject(error);
    }
);

// Response Interceptor: This function will run for every response received.
// This is where global error handling will be implemented in Group 5.
apiClient.interceptors.response.use(
    (response) => {
        // Any status code that lie within the range of 2xx cause this function to trigger
        return response;
    },
    (error) => {
        // Any status codes that falls outside the range of 2xx cause this function to trigger
        // Global error handling logic (e.g., for 401, 403, 409, 500) will be added here.
        return Promise.reject(error);
    }
);

export default apiClient;
```

***

#### **4.2. Service Layer Pattern & Example**

The service layer is a collection of modules that group API functions by their domain or feature. For example, `formsService.ts` will contain all functions for interacting with the `/admin/form-templates` endpoints. This pattern makes the code organized, reusable, and easy to test.

Each function within a service will use the configured `apiClient` and will be responsible for a single API endpoint call, including typing the request and response data.

**Directory Structure:**

```
/src/services/
├── authService.ts
├── formsService.ts
├── evaluationsService.ts
└── ... (other domain-specific services)
```

**Service Implementation Example (`formsService.ts`):**

This example shows a service function for fetching a single form template. Note how it uses the `apiClient` and provides strong typing for the response.

```typescript
// src/services/formsService.ts
import apiClient from "@/lib/apiClient";
import { EvaluationFormTemplate } from "@/types"; // Assumes a global types file

// A function to fetch a single form template by its ID
const getFormById = async (id: string): Promise<EvaluationFormTemplate> => {
    const response = await apiClient.get<EvaluationFormTemplate>(
        `/admin/form-templates/${id}`
    );
    return response.data;
};

// Other functions for creating, updating, etc., would be here
// const createForm = async (formData: NewFormData) => { ... };

export const formsService = {
    getFormById,
    // createForm,
};
```

**Integration with TanStack Query:**

The service functions are not called directly by UI components. Instead, they are consumed by the **TanStack Query custom hooks** we defined in Group 2, as required by the tech stack. This completes the data-fetching pattern.

```typescript
// src/features/forms/hooks/useFetchForm.ts
import { useQuery } from "@tanstack/react-query";
import { formsService } from "@/services/formsService"; // Using our new service

export const useFetchForm = (formId: string) => {
    return useQuery({
        // The query key uniquely identifies this data
        queryKey: ["forms", "detail", formId],
        // The query function is now a call to our service layer
        queryFn: () => formsService.getFormById(formId),
        // Enable the query only when formId is available
        enabled: !!formId,
    });
};
```

***

### **Group 5: Global Error Handling & Logging**

This section establishes a centralized, consistent strategy for managing and reporting errors, ensuring a reliable user experience, effective debugging, and graceful failure as mandated by the project's quality standards.

***

#### **5.1. Global Error Boundary Component**

To prevent the entire application from crashing due to a JavaScript error during rendering (the "white screen of death"), we will implement a global React Error Boundary. This component will wrap the entire application, catch any rendering errors, display a user-friendly fallback UI, and log the error details, ensuring the application always fails gracefully and maintains a professional appearance.

**Implementation (`ErrorBoundary.tsx`):**

```typescript
// src/components/shared/ErrorBoundary.tsx
import React, { Component, ErrorInfo, ReactNode } from "react";
import { logger } from "@/lib/logger"; // Our logging utility

interface Props {
    children: ReactNode;
}

interface State {
    hasError: boolean;
}

class ErrorBoundary extends Component<Props, State> {
    public state: State = {
        hasError: false,
    };

    public static getDerivedStateFromError(_: Error): State {
        // Update state so the next render will show the fallback UI.
        return { hasError: true };
    }

    public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        // Log the error to our logging service for debugging.
        logger.error("Uncaught rendering error:", { error, errorInfo });
    }

    public render() {
        if (this.state.hasError) {
            // Render a user-friendly, non-technical fallback UI.
            return (
                <div
                    role="alert"
                    style={{ padding: "2rem", textAlign: "center" }}
                >
                    <h2>Something went wrong.</h2>
                    <p>
                        We're sorry for the inconvenience. Please try refreshing
                        the page or contacting support if the problem persists.
                    </p>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
```

**Integration:**

The `ErrorBoundary` will be wrapped around the main application router in the entry point file to provide global coverage.

```typescript
// src/main.tsx (or App.tsx)
import React from "react";
import ReactDOM from "react-dom/client";
import AppRouter from "@/routes";
import ErrorBoundary from "@/components/shared/ErrorBoundary";
import { AuthProvider } from "@/context/AuthContext";

ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <ErrorBoundary>
            <AuthProvider>
                <AppRouter />
            </AuthProvider>
        </ErrorBoundary>
    </React.StrictMode>
);
```

***

#### **5.2. API Error Handling (Axios Interceptors)**

This builds directly upon the `apiClient` defined in Group 4. We will enhance the response interceptor to act as a single, centralized hub for handling all API errors consistently across the application. This prevents repetitive error-handling logic and ensures a uniform user experience for API-related issues.

**Updated Implementation (`apiClient.ts`):**

```typescript
// src/lib/apiClient.ts (updated response interceptor)
// ... (imports and apiClient creation from Group 4)

apiClient.interceptors.response.use(
    (response) => response, // Pass through successful responses
    (error) => {
        if (axios.isAxiosError(error) && error.response) {
            const { status } = error.response;

            switch (status) {
                case 401: // Unauthorized
                    // Handle token expiry, trigger a global logout event, and redirect to login.
                    // Example: authService.logout(); window.location.href = '/login';
                    break;
                case 403: // Forbidden
                    // This indicates the user is authenticated but not authorized.
                    // A redirect to a "403 Unauthorized" page should be triggered.
                    // Example: window.location.href = '/403-unauthorized';
                    break;
                case 409: // Conflict
                    // Fulfills the explicit UX requirement for handling concurrency.
                    // Trigger a global event to show the "Content Out of Date" modal.
                    // Example: eventBus.dispatch('show-conflict-modal');
                    break;
                case 503: // Service Unavailable
                    // Fulfills the UX requirement for handling AI service outages.
                    // Show a global toast notification: "A service is temporarily unavailable. Please try again later."
                    // Example: toast.error("Service is temporarily unavailable.");
                    break;
                default:
                    // For all other 4xx and 5xx errors, show a generic error toast.
                    // Example: toast.error("An unexpected error occurred. Please try again.");
                    break;
            }
        }
        // Forward the error so that component-level logic (e.g., in TanStack Query's onError) can still react to it.
        return Promise.reject(error);
    }
);

export default apiClient;
```

***

#### **5.3. Client-Side Logging Strategy**

To facilitate effective debugging without exposing sensitive information or cluttering the console in production, we will implement a simple, environment-aware logging utility.

**Strategy:**

The logger will provide standard methods (`info`, `warn`, `error`). In development, it will output richly formatted messages to the browser console. In production, it will suppress non-critical logs and be configured to forward only critical `error` level logs to a third-party monitoring service (e.g., Sentry, Datadog), which can be integrated in the future.

**Implementation (`logger.ts`):**

```typescript
// src/lib/logger.ts

const isDevelopment = process.env.NODE_ENV === "development";

type LogLevel = "info" | "warn" | "error";

const log = (level: LogLevel, message: string, data?: unknown) => {
    if (isDevelopment) {
        // In development, use standard console methods for easy debugging.
        console[level](`[${level.toUpperCase()}] ${message}`, data || "");
    } else {
        // In production, only log critical errors to a monitoring service.
        if (level === "error") {
            // INTEGRATION POINT: Send the error to a service like Sentry or Datadog.
            // This prevents console noise in production while capturing critical issues.
            // Example: Sentry.captureException(new Error(message), { extra: { data } });
        }
    }
};

export const logger = {
    info: (message: string, data?: unknown) => log("info", message, data),
    warn: (message: string, data?: unknown) => log("warn", message, data),
    error: (message: string, data?: unknown) => log("error", message, data),
};
```

***

### **Group 6: Frontend Testing Strategy**.

This section establishes the comprehensive testing pyramid for the frontend application, a critical component for ensuring code quality, preventing regressions, and validating that the application behaves exactly as specified to meet the project's goals of high data quality and integrity.

***

#### **6.1. Testing Philosophy & Tooling**

Our philosophy is to test application behavior from the user's perspective, not the implementation details. We will follow the principles of the **Testing Pyramid** to achieve a balanced and effective test suite.

```
      / \
     / ▲ \
    / E2E \      <-- Few, slow, high-value tests for critical user flows
   /-----\
  / Integration \  <-- More, medium-speed tests for component interactions
 /---------------\
/  Unit/Component \ <-- Many, fast, isolated tests for individual units
-------------------
```

**Tooling Selection:**

To implement this philosophy, we will use a modern, integrated set of tools that align with our tech stack.

* **Test Runner & Framework:** **Vitest**. Chosen for its speed and seamless integration with our Vite-based development environment.
* **Component Testing:** **React Testing Library (RTL)**. Used with Vitest to test React components in a way that resembles user interaction.
* **End-to-End (E2E) Testing:** **Cypress**. This is a refinement of the initial tech stack. Cypress is the superior choice over Selenium for our modern single-page application as it offers a significantly better developer experience, faster execution, and more reliable tests.
* **API Mocking:** **Mock Service Worker (msw)**. Used to intercept API requests at the network level, providing a highly realistic testing environment for our data-driven components.
* **Accessibility Testing:** **`jest-axe`** (compatible with Vitest). Integrated into component tests to automatically catch accessibility violations and help meet our WCAG 2.1 AA target.

***

#### **6.2. Unit & Component Testing Patterns**

This is the foundation of our pyramid, ensuring that individual components render and behave correctly in isolation.

**Strategy:**

* Each component will have a co-located test file.
* Tests will focus on what the user sees (rendering) and does (interaction).
* Dependencies will be mocked to keep tests isolated and fast.

**File Location:**

```
/src/components/shared/
├── StatCard.tsx
└── StatCard.test.tsx
```

**Implementation Example (`StatCard.test.tsx`):**

```typescript
// src/components/shared/StatCard.test.tsx
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { StatCard } from "./StatCard";

describe("StatCard", () => {
    it("renders the title, value, and description correctly", () => {
        render(
            <StatCard
                title="Total Users"
                value="1,234"
                description="+20% from last month"
            />
        );

        // Assert that the content is visible to the user
        expect(screen.getByText("Total Users")).toBeInTheDocument();
        expect(screen.getByText("1,234")).toBeInTheDocument();
        expect(screen.getByText("+20% from last month")).toBeInTheDocument();
    });
});
```

***

#### **6.3. Integration & End-to-End (E2E) Testing Patterns**

These higher-level tests validate that different parts of our application work together correctly to fulfill user flows.

**Integration Testing:**

**Strategy:** Integration tests will verify the interaction between multiple components, often involving client-side routing and state changes, with API calls mocked using **msw**.

**Integration Test Example (Login Flow):**

```typescript
// src/features/auth/Login.integration.test.tsx
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { describe, it, expect, vi } from "vitest";
import LoginPage from "@/pages/Login";

// Mock the auth service
vi.mock("@/services/authService", () => ({
    authService: {
        login: vi.fn(),
    },
}));

describe("Login Integration", () => {
    it("should allow a user to log in", async () => {
        render(
            <MemoryRouter initialEntries={["/login"]}>
                <LoginPage />
            </MemoryRouter>
        );

        // Simulate user input
        await userEvent.type(screen.getByLabelText(/email/i), "admin@test.com");
        await userEvent.type(
            screen.getByLabelText(/password/i),
            "Password123!"
        );

        // Simulate form submission
        fireEvent.click(screen.getByRole("button", { name: /log in/i }));

        // Assert that the login service was called
        await waitFor(() => {
            expect(authService.login).toHaveBeenCalledWith(
                "admin@test.com",
                "Password123!"
            );
        });
    });
});
```

**End-to-End (E2E) Testing:**

**Strategy:** E2E tests are the final layer of validation, simulating real user scenarios in a browser using **Cypress**. These tests will cover the most critical user flows defined in the UI/UX spec, such as "Student - Evaluation Submission" and "Admin - Form & Period Management".

**E2E Test Example (Cypress - Login Flow):**

```javascript
// cypress/e2e/login.cy.js

describe("Login Flow", () => {
    it("successfully logs in a user and redirects to the dashboard", () => {
        // Intercept the API call and provide a mock response
        cy.intercept("POST", "/api/v1/auth/login", {
            statusCode: 200,
            body: {
                accessToken: "fake-jwt-token",
                user: { id: 1, name: "Admin User", roles: ["Admin"] },
            },
        }).as("loginRequest");

        // Visit the login page
        cy.visit("/login");

        // Fill out and submit the form
        cy.get('input[name="email"]').type("admin@test.com");
        cy.get('input[name="password"]').type("Password123!");
        cy.get('button[type="submit"]').click();

        // Wait for the API call to complete
        cy.wait("@loginRequest");

        // Assert that the user is redirected to the dashboard
        cy.url().should("include", "/dashboard");
        cy.contains("Welcome, Admin User").should("be.visible");
    });
});
```

***
